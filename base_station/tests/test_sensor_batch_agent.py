import pytest
import random
from base_station_app import batch_agent_sensor
from records import *
from unittest.mock import patch



# Batch agent receives batch messages and calls the batch processor to store each message
@pytest.mark.asyncio()
async def test_batch_agent_sensor_yield(test_app):
    reading = random.randint(10, 30)
    sensor_id, sensor_type, reading_unit  = 'F4:12:FA:83:00:F0_A', 'temperature sensor', 'Celsius'
    timestamp = ''
    latitude, longitude = '51.509865', '-0.118092'
    sensor_message = SensorMessage(sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude)

    with patch('base_station_app.bp') as mock_bp:
        async with batch_agent_sensor.test_context() as agent:
            await agent.put(sensor_message)
            mock_bp.store_locally.assert_called_with([sensor_message])