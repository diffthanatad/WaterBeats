from data_buffer_connection import data_buffer_connection
import pytest
import asyncio
pytest_plugins = ('pytest_asyncio')

data_buffer = data_buffer_connection()
data = {"sensorId": 1, "timestamp": 1, "sensorType": "temperature", "data": "10"}
@pytest.mark.asyncio
async def test_send_data():
    assert await data_buffer.send_data(data) == f"Data sent to DataBuffer: {data}"

@pytest.mark.asyncio
async def test_get_data():
    assert await data_buffer.get_data(1, 1) == {"data": 10.0, "sensorId": "1", "sensorType": "temperature", "timestamp": "1"}

@pytest.mark.asyncio
async def test_delete_data():
    assert await data_buffer.delete_data(1, 1) == f"Data deleted from DataBuffer"

@pytest.mark.asyncio
async def test_get_data_history():
    data2 = {"sensorId": "1", "timestamp": 2, "sensorType": "temperature", "data": "20"}
    data3 = {"sensorId": "1", "timestamp": 3, "sensorType": "temperature", "data": "30"}
    await data_buffer.send_data(data)
    await data_buffer.send_data(data2)
    await data_buffer.send_data(data3)
    assert await data_buffer.get_data_history("3") == [{"data": 10.0, "sensorId": "1", "sensorType": "temperature", "timestamp": 1}, {"data": 20.0, "sensorId": "1", "sensorType": "temperature", "timestamp": 2}, {"data": 30.0, "sensorId": "1", "sensorType": "temperature", "timestamp": 3}]
        
@pytest.mark.asyncio
async def test_delete_data_history():
    assert await data_buffer.delete_data_history("3") == f"Data history deleted from DataBuffer"