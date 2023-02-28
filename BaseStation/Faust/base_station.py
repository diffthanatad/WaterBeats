import faust
import time
import random

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
    return time.strftime('%Y-%m-%d %H:%M:%S')

class SensorMessage(faust.Record):
    sensor_id: str
    reading: str
    sensor_type: str = ''
    reading_unit: str = ''
    timestamp: str = ''

class HumidityMessage(SensorMessage):
    sensor_type: str = 'humidity'

class TemperatureMessage(faust.Record):
    sensor_type: str = 'temperature'

class SoilMoistureMessage(faust.Record):
    sensor_type: str = 'soil-moisture'

# defines humidity, temperature, soil moisture topics to receive sensor messages
humidity_stream = app.topic('humidity_stream', value_type=HumidityMessage)
temperature_stream = app.topic('temperature_stream', value_type=TemperatureMessage)
soil_moisture_stream = app.topic('soil-moisture_stream', value_type=SoilMoistureMessage)

humidity_batch = app.topic('humidity_batch', value_type=HumidityMessage)
temperature_batch = app.topic('temperature_batch', value_type=TemperatureMessage)
soil_moisture_batch = app.topic('soil_moisture_batch', value_type=SoilMoistureMessage)


# batch agents
@app.agent(humidity_batch)
async def batch_agent_humidity(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=HUMIDITY_BATCH_INTERVAL):
        # print('batch agent received humidity data')
        # save to local database
        bp.store_locally(batch)

@app.agent(temperature_batch)
async def batch_agent_temperature(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=TEMPERATURE_BATCH_INTERVAL):
        # print('batch agent received temperature data')
        # save to local database
        bp.store_locally(batch)

@app.agent(soil_moisture_batch)
async def batch_agent_soil_moisture(batches):
    async for batch in batches.take(MAX_BATCH_SIZE, within=SOIL_MOISTURE_BATCH_INTERVAL):
        # print('batch agent received soil moisture data')
        # save to local database
        bp.store_locally(batch)


# streaming agents
@app.agent(humidity_stream, sink=[humidity_batch])
async def stream_agent_humidity(messages):
    async for message in messages:
        message.timestamp = get_timestamp()
        # print('stream agent received humidity data at', message.timestamp)
        yield message
        #sp.calculateActuatorInstruction(message)

@app.agent(temperature_stream, sink=[temperature_batch])
async def stream_agent_temperature(messages):
    async for message in messages:
        message.timestamp = get_timestamp()
        # print('stream agent received temperature data at', raw_data.timestamp)
        yield message
        #sp.calculateActuatorInstruction(message)

@app.agent(soil_moisture_stream, sink=[soil_moisture_batch])
async def stream_agent_soil_moisture(messages):
    async for message in messages:
        message.timestamp = get_timestamp()
        # print('stream agent received soil moisture data at', raw_data.timestamp)
        yield message
        #await sp.calculateActuatorInstruction(message)


# @app.timer(interval=2)
# async def every_2_seconds():
#     randTemp = random.randint(5, 25)
#     message = SoilMoistureMessage('someSensorID', randTemp)
#     print(message)
#     await soil_moisture_readings.send(value=message)