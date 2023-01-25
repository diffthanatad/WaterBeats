import asyncio
import pytest
pytest_plugins = ('pytest_asyncio',)
import sys
sys.path.insert(0, "../IoTSimulator")
from simulator import SimpleSimulatorFactory, TemperatureSimulator


# * This is the test case template for testing http requests
@pytest.mark.asyncio
async def test_send_temperature_data():
    simulator = TemperatureSimulator("id", 1, "http://localhost:5000/new_data","sensor")
    data = simulator.create_output_data(10)
    assert await simulator.send_data(data) == f"Data sent to base station: {data}"