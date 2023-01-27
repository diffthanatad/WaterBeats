from edge_data_processor import data_buffer_connection
import asyncio
import pytest
pytest_plugins = ('pytest_asyncio')

@pytest.mark.asyncio
async def test_send_data():
    data_buffer = data_buffer_connection()
    data = {"sensorId": "1", "timestamp": "1", "sensorType": "temperature", "data": "10"}
    assert await data_buffer.send_data(data) == f"Data sent to DataBuffer: {data}"
