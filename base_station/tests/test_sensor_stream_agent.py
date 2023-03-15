import pytest
import random
import asyncio
import datetime
from base_station_app import stream_agent_sensor
from records import *



def get_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp

# Stream agent sensor gets sensor metadata, correctly fills in the full sensor message and sends to sink
@pytest.mark.asyncio()
async def test_stream_agent_sensor_yield(test_app):
    async with stream_agent_sensor.test_context() as agent:
        sensor_message = SensorMessage('30:AE:A4:14:C2:90_A', 15)
        event = await agent.put(sensor_message)
        actual_output = agent.results[event.message.offset]
        actual_output.timestamp = '' # don't compare timestamps
        expected_output = SensorMessage('30:AE:A4:14:C2:90_A', 15, 'temperature sensor', 'Celsius', '', '51.509865', '-0.118092')
        assert actual_output == expected_output

# Stream agent sensor is able to finish processing 1000 messages sent concurrently with minimal delay
@pytest.mark.asyncio()
async def test_stream_agent_sensor_performance(test_app):
    async with stream_agent_sensor.test_context() as agent:
        messages = []
        NUM_MESSAGES = 1000
        for _ in range(NUM_MESSAGES):
            reading = random.randint(10, 30)
            sensor_message = SensorMessage('F4:12:FA:83:00:F0_A', reading) # temperature message
            messages.append(sensor_message)

        async def send_message(sensor_message):
            await agent.put(sensor_message)

        start_time = get_timestamp()
        await asyncio.gather(*map(send_message, messages))
        finish_time = get_timestamp()
        process_time = finish_time - start_time
        print(f'Processing {NUM_MESSAGES} sensor messages took {process_time.total_seconds()} seconds')
        assert process_time < datetime.timedelta(milliseconds = 1000)