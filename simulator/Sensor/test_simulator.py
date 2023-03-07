from simulator import SimpleSimulatorFactory, TemperatureSimulator, SoilMoistureSimulator, WaterLevelSimulator, WaterPollutionSimulator
import asyncio
import pytest
pytest_plugins = ('pytest_asyncio',)

def test_simulator_factory():
    simulator = SimpleSimulatorFactory.create("temperature", "id", 1, "http://localhost:23333/new_data","sensor","acutator")
    data = simulator.create_output_data(11.4)
    assert "temperature" in data
    assert data["temperature"] == 11.4

def test_temperature_simulator_has_temp_in_data():
    simulator = TemperatureSimulator("id", 1, "http://localhost:23333/new_data","sensor")
    data = simulator.create_output_data(10)
    assert data["sensor_id"] == "id"
    assert data["temperature"] == 10

@pytest.mark.asyncio
async def test_send_temperature_data():
    simulator = TemperatureSimulator(1, 1, "http://localhost:5500/new_data","sensor")
    data = simulator.create_output_data(10)
    assert await simulator.send_data(data) == f"Data sent to base station: {data}"

@pytest.mark.asyncio
async def test_send_soilmoisture_data():
    simulator = SoilMoistureSimulator(57, 1, "http://localhost:5500/new_data","sensor")
    data = simulator.create_output_data(10)
    assert await simulator.send_data(data) == f"Data sent to base station: {data}"
    
@pytest.mark.asyncio
async def test_send_waterlevel_data():
    simulator = WaterLevelSimulator(120, 1, "http://localhost:5500/new_data","sensor")
    data = simulator.create_output_data(10)
    assert await simulator.send_data(data) == f"Data sent to base station: {data}"
    
@pytest.mark.asyncio
async def test_send_waterpollution_data():
    simulator = WaterPollutionSimulator(22, 1, "http://localhost:5500/new_data","sensor")
    data = simulator.create_output_data(10)
    assert await simulator.send_data(data) == f"Data sent to base station: {data}"