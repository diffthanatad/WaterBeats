import pytest
import random
import batch_processor
from records import *
from unittest.mock import call, patch, mock_open
from pathlib import Path



# Batch processor decomposes sensor message and writes data to the correct local file in the correct format
@pytest.mark.asyncio()
async def test_batch_processor_writes_to_disk(test_app):

    batch = []
    expected_calls = []

    sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude = (
        'F4:12:FA:83:00:F0_A', random.randint(10, 30), 'temperature sensor', 'Celsius', '', '51.509865', '-0.118092')
    temperature_sensor_message = SensorMessage(sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude)
    expected_calls.append(call(f'{sensor_id},{reading},{sensor_type},{reading_unit},{timestamp},{latitude},{longitude}\r\n'))
    batch.append(temperature_sensor_message)

    sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude = (
        'F4:12:FA:83:00:F0_B', random.randint(10, 30), 'humidity sensor', 'Percent', '', '51.509865', '-0.118092')
    humidity_sensor_message = SensorMessage(sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude)
    expected_calls.append(call(f'{sensor_id},{reading},{sensor_type},{reading_unit},{timestamp},{latitude},{longitude}\r\n'))
    batch.append(humidity_sensor_message)

    sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude = (
        'F4:12:FA:83:00:F0_C', random.randint(10, 30), 'soil moisture sensor', 'Percent', '', '51.509865', '-0.118092')
    soil_moisture_sensor_message = SensorMessage(sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude)
    expected_calls.append(call(f'{sensor_id},{reading},{sensor_type},{reading_unit},{timestamp},{latitude},{longitude}\r\n'))
    batch.append(soil_moisture_sensor_message)

    mocked_open = mock_open()
    with patch("batch_processor.open", mocked_open, create=True):
        batch_processor.store_locally(batch)

    script_location = Path(__file__).absolute().parent
    cold_store_file = script_location / '../local_data/sensor_data_cold_store.csv'

    mocked_open.assert_called_with(cold_store_file, 'a', newline='', encoding='utf8')
    mocked_open.return_value.write.assert_has_calls(expected_calls)