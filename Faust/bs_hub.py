# receives all raw messages from connected sensors.
# performs pre-processing and dispatches new messages to cold storage -> main pc -> cloud storage
# performs pre-processing and dispatches new messages for processing sensor data into actuator instructions

import faust
import time
import random

import config_supplier
import speed_processor as sp
import batch_processor as bp



app = faust.App(
    'base_station_hub',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

def get_timestamp():
  return time.strftime('%Y-%m-%d %H:%M:%S')

class HumidityReading(faust.Record):
  sensor_id: str
  reading_value: str
  timestamp: str = 'default'

class TemperatureReading(faust.Record):
  sensor_id: str
  reading_value: str
  timestamp: str = 'default'

class SoilMoistureReading(faust.Record):
  sensor_id: str
  reading_value: str
  timestamp: str = 'default'

class ActuatorInstruction(faust.Record):
    actuator_id: str
    state: str
    timestamp: str = 'default'

# defines humidity, temperature, soil moisture topics to receive sensor messages
humidity_readings = app.topic('humidity', value_type=HumidityReading)
temperature_readings = app.topic('temperature', value_type=TemperatureReading)
soil_moisture_readings = app.topic('soil-moisture', value_type=SoilMoistureReading)

actuator_instructions = app.topic('actuator', value_type=ActuatorInstruction)

# humidity_batch = app.topic('humidity_batch', value_type=HumidityReading)
# temperature_batch = app.topic('temperature_batch', value_type=TemperatureReading)
# soil_moisture_batch = app.topic('soil_moisture_batch', value_type=SoilMoistureReading)

configurations = config_supplier.get_base_station_configs()
MAX_BATCH_SIZE = int(configurations['max_batch_size'])
HUMIDITY_BATCH_INTERVAL = int(configurations['humidity_interval'])
TEMPERATURE_BATCH_INTERVAL = int(configurations['temperature_interval'])
SOIL_MOISTURE_BATCH_INTERVAL = int(configurations['soil_moisture_interval'])



# batch agents
@app.agent()
async def batch_agent_humidity(humidity_data):
    async for raw_data in humidity_data.take(MAX_BATCH_SIZE, within=HUMIDITY_BATCH_INTERVAL):
        print('batch agent received humidity data')
        # save to local database
        bp.store_locally(raw_data, 'humidity')

@app.agent()
async def batch_agent_temperature(temperature_data):
    async for raw_data in temperature_data.take(MAX_BATCH_SIZE, within=TEMPERATURE_BATCH_INTERVAL):
        print('batch agent received temperature data')
        # save to local database
        bp.store_locally(raw_data, 'temperature')

@app.agent()
async def batch_agent_soil_moisture(soil_moisture_data):
    async for raw_data in soil_moisture_data.take(MAX_BATCH_SIZE, within=SOIL_MOISTURE_BATCH_INTERVAL):
        print('batch agent received soil moisture data')
        # save to local database
        bp.store_locally(raw_data, 'soil_moisture')


# streaming agents
@app.agent(humidity_readings, sink=[batch_agent_humidity])
async def stream_agent_humidity(humidity_raw_data):
    async for raw_data in humidity_raw_data:
        if raw_data.timestamp == 'default':
            raw_data.timestamp = get_timestamp()
        print('stream agent received humidity data at', raw_data.timestamp)
        yield raw_data
        sp.calculateActuatorInstruction(raw_data)

@app.agent(temperature_readings, sink=[batch_agent_temperature])
async def stream_agent_temperature(temperature_raw_data):
    async for raw_data in temperature_raw_data:
        if raw_data.timestamp == 'default':
            raw_data.timestamp = get_timestamp()
        print('stream agent received temperature data at', raw_data.timestamp)
        yield raw_data
        sp.calculateActuatorInstruction(raw_data)

@app.agent(soil_moisture_readings, sink=[batch_agent_soil_moisture])
async def stream_agent_soil_moisture(soil_moisture_raw_data):
    async for raw_data in soil_moisture_raw_data:
        if raw_data.timestamp == 'default':
            raw_data.timestamp = get_timestamp()
        print('stream agent received soil moisture data at', raw_data.timestamp)
        yield raw_data
        await sp.calculateActuatorInstruction(raw_data)
        


# actuator instruction agent
@app.agent(actuator_instructions)
async def actuator_agent(instructions):
    async for instruction in instructions:
        print('Actuator agent received new instruction')
        print(instruction)


#
# @app.timer(interval=2)
# async def every_2_seconds():
#     randTemp = random.randint(5, 25)
#     message = SoilMoistureReading('someSensorID', randTemp)
#     print(message)
#     await soil_moisture_readings.send(value=message)