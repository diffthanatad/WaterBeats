import time
import faust
import datetime

import config_supplier as cs
import stream_processor as sp
import batch_processor as bp
import device_controller as dc
import rule_engine as re

from records import *



configurations = cs.get_configs()
MAX_BATCH_SIZE = int(configurations['max_batch_size'])
SENSOR_BATCH_INTERVAL = int(configurations['sensor_interval'])

app = faust.App(
    'base_station',
    broker='kafka://localhost:9092',
    value_serializer='json',
)
 
def get_timestamp():
    return datetime.datetime.now()

# fills sensor messages with metadata such as location and type of emitting sensor
def fill_sensor_message(message):
    message.timestamp = get_timestamp()
    sensor = dc.get_device(message.sensor_id)
    message.sensor_type = sensor.sensor_type
    message.reading_unit = sensor.reading_unit
    message.latitude = sensor.latitude
    message.longitude = sensor.longitude

    global latest_sensor_message
    latest_sensor_message = message
    return message

def fill_task_message(message):
    message.timestamp = get_timestamp()
    actuator = dc.get_device(message.actuator_target)
    message.actuator_type = actuator.actuator_type

    global latest_task_message
    latest_task_message = message
    return message

latest_sensor_message = 'No messages'
latest_task_message = 'No messages'

# defines topics/channels
sensor_stream = app.topic('sensor_stream', value_type=SensorMessage)
sensor_batch = app.topic('sensor_batch', value_type=SensorMessage)
task_stream = app.topic('task_stream', value_type=TaskMessage)
rule_stream = app.topic('rule_stream', value_type=RuleMessage)
time_stream = app.topic('time_stream', value_type=TimeMessage)

### batch agents
# sensor messages
@app.agent(sensor_batch)
async def batch_agent_sensor(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=SENSOR_BATCH_INTERVAL):
        bp.store_locally(batch)
        yield batch

### streaming agents
# sensor messages
@app.agent(sensor_stream, sink=[sensor_batch])
async def stream_agent_sensor(messages):
    async for message in messages:
        message = fill_sensor_message(message)
        await sp.process_sensor_message(message)
        #await sp.send_to_hub(message)
        yield message

# task messages
@app.agent(task_stream)
async def tasks_agent(messages):
    async for message in messages:
        message = fill_task_message(message)
        #await sp.send_task_to_server(message)
        newState = 'ON' if message.state else 'OFF'
        print('Task Dispatched: ' + 'Actuator ' + message.actuator_target + ' of type ' 
              + message.actuator_type + ' to be turned ' + newState + ' at ' + str(message.intensity) 
              + ' intensity for ' + str(message.duration) + ' seconds ')
        yield message

# rule messages
@app.agent(rule_stream)
async def rules_agent(messages):
    async for message in messages:
        if ((message.sensor_condition_message == None) and (message.time_condition_message == None)):
            await task_stream.send(value=(message.task_message))
        else:
            re.load_rule(message)
            re.store_rule(message)
        yield message

# time messages
@app.agent(time_stream)
async def time_agent(messages):
    async for message in messages:
        await sp.process_time_message(message)
        yield message



# execute task every interval -> sends time message
@app.timer(interval = 60.0)
async def send_time_message():
    timestamp = str(get_timestamp().replace(second = 0, microsecond = 0))
    time_message = TimeMessage(timestamp)
    await time_stream.send(value=(time_message))



### simple development web view
# latest sensor message
@app.page('/sensor-messages/')
async def update_sensor_message(self, request):
    global latest_sensor_message
    return self.json(latest_sensor_message)

# latest task message
@app.page('/task-messages/')
async def update_task_message(self, request):
    global latest_task_message
    return self.json(latest_task_message)



# Faust -> python executable
if __name__ == '__main__':
    app.main()
