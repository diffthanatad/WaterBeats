import faust
import datetime

import config_supplier
import speed_processor as sp
import batch_processor as bp
import device_controller as dc



configurations = config_supplier.get_base_station_configs()
MAX_BATCH_SIZE = int(configurations['max_batch_size'])
HUMIDITY_BATCH_INTERVAL = int(configurations['humidity_interval'])
TEMPERATURE_BATCH_INTERVAL = int(configurations['temperature_interval'])
SOIL_MOISTURE_BATCH_INTERVAL = int(configurations['soil_moisture_interval'])



app = faust.App(
    'base_station',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

def get_timestamp():
    return datetime.datetime.now()

latest_sensor_message = 'No messages'
latest_task_message = 'No messages'

class SensorMessage(faust.Record):
    sensor_id: str
    reading: str
    sensor_type: str = ''
    reading_unit: str = ''
    timestamp: str = ''
    latitude: float = ''
    longitude: float = ''

class HumidityMessage(SensorMessage):
    sensor_type: str = 'humidity sensor'

class TemperatureMessage(SensorMessage):
    sensor_type: str = 'temperature sensor'

class SoilMoistureMessage(SensorMessage):
    sensor_type: str = 'soil moisture sensor'

class TaskMessage(faust.Record):
    actuator_target: str
    state: bool
    intensity: float
    actuator_type: str = ''
    duration: int = -1
    timestamp: str = ''

# defines humidity, temperature, soil moisture topics to receive sensor messages
humidity_stream = app.topic('humidity_stream', value_type=HumidityMessage)
temperature_stream = app.topic('temperature_stream', value_type=TemperatureMessage)
soil_moisture_stream = app.topic('soil_moisture_stream', value_type=SoilMoistureMessage)

humidity_batch = app.topic('humidity_batch', value_type=HumidityMessage)
temperature_batch = app.topic('temperature_batch', value_type=TemperatureMessage)
soil_moisture_batch = app.topic('soil_moisture_batch', value_type=SoilMoistureMessage)

task_stream = app.topic('task_stream', value_type=TaskMessage)

# batch agents
@app.agent(humidity_batch)
async def batch_agent_humidity(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=HUMIDITY_BATCH_INTERVAL):
        bp.store_locally(batch)

@app.agent(temperature_batch)
async def batch_agent_temperature(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=TEMPERATURE_BATCH_INTERVAL):
        bp.store_locally(batch)

@app.agent(soil_moisture_batch)
async def batch_agent_soil_moisture(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=SOIL_MOISTURE_BATCH_INTERVAL):
        bp.store_locally(batch)



def fillSensorMessage(message):
    message.timestamp = get_timestamp()
    sensor_data = dc.getSensorData(message.sensor_id)
    message.reading_unit = sensor_data.reading_unit
    message.latitude = sensor_data.latitude
    message.longitude = sensor_data.longitude

    global latest_sensor_message
    latest_sensor_message = message
    return message

def fillTaskMessage(message):
    message.timestamp = get_timestamp()
    actuator_data = dc.getActuatorData(message.actuator_target)
    message.actuator_type = actuator_data.device_type

    global latest_task_message
    latest_task_message = message
    return message

# streaming agents
@app.agent(humidity_stream, sink=[humidity_batch])
async def stream_agent_humidity(messages):
    async for message in messages:
        print(message)
        message = fillSensorMessage(message)
        await sp.process(message)
        sp.sendToHub(message)
        yield message

@app.agent(temperature_stream, sink=[temperature_batch])
async def stream_agent_temperature(messages):
    async for message in messages:
        print(message)
        message = fillSensorMessage(message)
        await sp.process(message)
        sp.sendToHub(message)
        yield message

@app.agent(soil_moisture_stream, sink=[soil_moisture_batch])
async def stream_agent_soil_moisture(messages):
    async for message in messages:
        message = fillSensorMessage(message)
        await sp.process(message)
        sp.sendToHub(message)
        yield message



# tasks agent
@app.agent(task_stream)
async def tasks_agent(messages):
    async for message in messages:
        message = fillTaskMessage(message)
        newState = 'ON' if message.state else 'OFF'
        print('Task Dispatched: ' + 'Actuator ' + message.actuator_target + ' of type ' 
              + message.actuator_type + ' to be turned ' + newState + ' at ' + str(message.intensity) 
              + ' intensity for ' + str(message.duration) + ' seconds ')



@app.page('/sensor-messages/')
async def update_sensor_message(self, request):
    global latest_sensor_message
    return self.json(latest_sensor_message)

@app.page('/task-messages/')
async def update_task_message(self, request):
    global latest_task_message
    return self.json(latest_task_message)



if __name__ == '__main__':
    app.main()
