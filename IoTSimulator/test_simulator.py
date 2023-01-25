from simulator import SimpleSimulatorFactory, TemperatureSimulator

def test_simulator_factory():
    simulator = SimpleSimulatorFactory.create("temperature", "id", 1, "http://localhost:23333/new_data")
    data = simulator.create_output_data(11.4)
    assert "temperature" in data
    assert data["temperature"] == 11.4

def test_temperature_simulator_has_temp_in_data():
    simulator = TemperatureSimulator("id", 1, "http://localhost:23333/new_data")
    data = simulator.create_output_data(10)
    assert data["sensor_id"] == "id"
    assert data["temperature"] == 10
