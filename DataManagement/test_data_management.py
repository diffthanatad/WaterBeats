from data_management import DataManagement, insert_sensor_data
from create_token import find_waterbeats_buckets, create_token_for_bucket
import pytest
import time
import random
import aiohttp

WB_bucket = find_waterbeats_buckets()
WB_token = create_token_for_bucket(WB_bucket["id"],WB_bucket["orgID"])
WB_datamanagement = DataManagement(WB_bucket["id"], WB_bucket["orgID"], WB_token, "http://localhost:8086")

def test_insert_sensor_data():
    sensor_id = "1"
    sensor_type = "test_type"
    sensor_data = random.uniform(-10, 1000)
    unit = "test_unit"
    longitude = random.uniform(-1000, 1000)
    latitude = random.uniform(-1000, 1000)
    timestamp = time.time_ns()
    response = insert_sensor_data(WB_datamanagement, sensor_id, sensor_type, sensor_data, unit, longitude, latitude, timestamp)
    assert response == "Data inserted"

@pytest.mark.asyncio
async def test_insert_sensor_data_api():
    json_data = {
        "sensor_id": "2",
        "sensor_type": "temperature",
        "data": 26.4,
        "unit": "C",
        "longitude": 2134.1234124,
        "latitude": 321444.12341234,
        "timestamp": 1675774426146000000
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5555/sensor_data', json=json_data) as resp:
            assert resp.status == 200
            
@pytest.mark.asyncio
async def test_insert_sensor_data_api_missing_data():
    json_data = {
        "sensor_id": "3",
        "sensor_type": "temperature",
        "data": 26.4,
        "unit": "C",
        "longitude": 2134.1234124,
        "latitude": 321444.12341234
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5555/sensor_data', json=json_data) as resp:
            assert resp.status == 400
            
@pytest.mark.asyncio
async def test_insert_sensor_data_api_2_interval():
    json_data = {
        "sensor_id": str(random.randint(5,100)),
        "sensor_type": "temperature",
        "data": random.uniform(-10, 1000),
        "unit": "C",
        "longitude": random.uniform(-1000, 1000),
        "latitude": random.uniform(-1000, 1000),
        "timestamp": time.time_ns()
    }
    for i in range(10):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:5555/sensor_data', json=json_data) as resp:
                print(resp.text)
                assert resp.status == 200
        print(i)
        time.sleep(2)