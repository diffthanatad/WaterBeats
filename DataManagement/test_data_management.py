import pytest
import time
import random
import aiohttp

@pytest.mark.asyncio
async def test_insert_sensor_data_api():
    json_data = {
        "sensor_id": f"tempsensor_{str(random.randint(1,100))}",
        "sensor_type": "temperature",
        "data": 26.4,
        "status": "on",
        "unit": "C",
        "longitude": 2134.1234124,
        "latitude": 321444.12341234,
        "timestamp": time.time_ns()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5555/sensor_data', json=json_data) as resp:
            assert resp.status == 200

@pytest.mark.asyncio
async def test_insert_sensor_data_api_missing_data():
    json_data = {
        "sensor_id": f"sensor_{str(random.randint(1,100))}",
        "sensor_type": "temperature",
        "data": 26.4,
        "status": "on",
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
        "sensor_id": f"sensor_{str(random.randint(1,100))}",
        "sensor_type": "temperature",
        "data": random.uniform(-10, 1000),
        "status": "on",
        "unit": "C",
        "longitude": random.uniform(-1000, 1000),
        "latitude": random.uniform(-1000, 1000),
        "timestamp": time.time_ns()
    }
    for i in range(10):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:5555/sensor_data', json=json_data) as resp:
                assert resp.status == 200
        time.sleep(2)

@pytest.mark.asyncio
async def test_insert_actuator_data_api():
    json_data = {
        "actuator_id": f"actuator_{str(random.randint(5,100))}",
        "actuator_type": "test_type",
        "status": "off",
        "longitude": random.uniform(-1000, 1000),
        "latitude": random.uniform(-1000, 1000),
        "timestamp": time.time_ns()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5555/actuator_data', json=json_data) as resp:
            assert resp.status == 200

@pytest.mark.asyncio
async def test_insert_actuator_data_api_missing_data():
    json_data = {
        "actuator_id": f"actuator_{str(random.randint(5,100))}",
        "actuator_type": "test_type",
        "status": "off",
        "longitude": random.uniform(-1000, 1000),
        "timestamp": time.time_ns()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5555/actuator_data', json=json_data) as resp:
            assert resp.status == 400

@pytest.mark.asyncio
async def test_insert_actuator_data_api_2_interval():
    json_data = {
        "actuator_id": f"actuator_{str(random.randint(5,100))}",
        "actuator_type": "test_type",
        "status": "on",
        "longitude": random.uniform(-1000, 1000),
        "latitude": random.uniform(-1000, 1000),
        "timestamp": time.time_ns()
    }
    for i in range(10):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:5555/actuator_data', json=json_data) as resp:
                assert resp.status == 200
        time.sleep(2)