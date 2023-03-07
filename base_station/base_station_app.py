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
def fillSensorMessage(message):
    message.timestamp = get_timestamp()
    sensor = dc.getDevice(message.sensor_id)
    message.sensor_type = sensor.sensor_type
    message.reading_unit = sensor.reading_unit
    message.latitude = sensor.latitude
    message.longitude = sensor.longitude

    global latest_sensor_message
    latest_sensor_message = message
    return message

def fillTaskMessage(message):
    message.timestamp = get_timestamp()
    actuator = dc.getDevice(message.actuator_target)
    message.actuator_type = actuator.actuator_type

    global latest_task_message
    latest_task_message = message
    return message

def jsonMessage(message):
    return {
        "sensor_id" : message.sensor_id,
        "sensor_type" : message.sensor_type,
        "data" : message.reading,
        "unit" : message.reading_unit,
        "longitude" : message.longitude,
        "latitude" : message.latitude,
        "timestamp" : time.time_ns(), # This is just temporary used
    }

latest_sensor_message = 'No messages'
latest_task_message = 'No messages'

# defines topics/channels
sensor_stream = app.topic('sensor_stream', value_type=SensorMessage)
sensor_batch = app.topic('sensor_batch', value_type=SensorMessage)
task_stream = app.topic('task_stream', value_type=TaskMessage)
rule_stream = app.topic('rule_stream', value_type=RuleMessage)

### batch agents
# sensor messages
@app.agent(sensor_batch)
async def batch_agent_sensor(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=SENSOR_BATCH_INTERVAL):
        bp.store_locally(batch)

### streaming agents
# sensor messages
@app.agent(sensor_stream, sink=[sensor_batch])
async def stream_agent_sensor(messages):
    async for message in messages:
        message = fillSensorMessage(message)
        await sp.processSensorMessage(message)
        #await sp.sendToHub(jsonMessage(message))
        yield message

# task messages
@app.agent(task_stream)
async def tasks_agent(messages):
    async for message in messages:
        message = fillTaskMessage(message)
        newState = 'ON' if message.state else 'OFF'
        print('Task Dispatched: ' + 'Actuator ' + message.actuator_target + ' of type ' 
              + message.actuator_type + ' to be turned ' + newState + ' at ' + str(message.intensity) 
              + ' intensity for ' + str(message.duration) + ' seconds ')

# rule messages
@app.agent(rule_stream)
async def rules_agent(messages):
    async for message in messages:
        if message.condition_message == None:
            await task_stream.send(value=(message.task_message))
        else:
            re.loadRule(message)
            re.storeRule(message)



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
