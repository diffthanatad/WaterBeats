import pytest
from unittest.mock import Mock, patch
import time
import random
from base_station_app import app, stream_agent_sensor, sensor_batch
from records import *

import datetime


def get_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp

@pytest.mark.asyncio()
@pytest.fixture(scope='module')
def event_loop():
    yield app.loop

@pytest.fixture()
def test_app(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app

@pytest.mark.asyncio()
async def test_stream_agent_sensor(test_app):
    async with stream_agent_sensor.test_context() as agent:
        sensor_message = SensorMessage('30:AE:A4:14:C2:90_A', 15)
        event = await agent.put(sensor_message)
        actual_output = agent.results[event.message.offset]
        actual_output.timestamp = ''
        expected_output = SensorMessage('30:AE:A4:14:C2:90_A', 15, 'temperature sensor', 'Celsius', '', '51.509865', '-0.118092')
        assert actual_output == expected_output

@pytest.mark.asyncio()
async def test_sensor_stream(test_app):
    async with stream_agent_sensor.test_context() as agent:
        for _ in range(5):
            time.sleep(1)
            for _ in range(50):
                reading = random.randint(10, 30)
                humidity_msg = SensorMessage('F4:12:FA:83:00:F0_A', reading)
                input_time = get_timestamp().replace(microsecond = 0)
                event = await agent.put(humidity_msg)
                output_time = agent.results[event.message.offset].timestamp.replace(microsecond = 0)
                time_difference = output_time - input_time
                assert time_difference <= datetime.timedelta(seconds = 2)