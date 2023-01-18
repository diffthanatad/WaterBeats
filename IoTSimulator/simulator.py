import math
import random
from asyncio import sleep
import aiohttp
from datetime import datetime


class SimpleSimulatorFactory:
    def create(
        sensor_type: str, id: str, interval: int, base_station_endpoint: str, device_type: str, actuator_type: str,
    ) -> "Simulator":
        print(sensor_type, id, interval, base_station_endpoint, device_type, actuator_type)
        if device_type == "sensor":
            if sensor_type == "temperature":
                simulator = TemperatureSimulator(id, interval, base_station_endpoint, device_type)
            elif sensor_type == "soil_moisture":
                simulator = SoilMoistureSimulator(id, interval, base_station_endpoint, device_type)
            elif sensor_type == "water_level":
                simulator = WaterLevelSimulator(id, interval, base_station_endpoint, device_type)
            elif sensor_type == "water_pollution":
                simulator = WaterPollutionSimulator(id, interval, base_station_endpoint, device_type)
            else:
                raise Exception(f"Unknown sensor type: {sensor_type}")
        elif device_type == "actuator":
            if actuator_type == "water_sprinkler":
                simulator = WaterSprinklerSimulator(id, interval, base_station_endpoint, device_type)
            elif actuator_type == "water_pump":
                simulator = WaterPumpSimulator(id, interval, base_station_endpoint, device_type)
            else:
                raise Exception(f"Unknown actuator type: {actuator_type}")
        return simulator


class Simulator:
    def __init__(self, id: str, interval: int, base_station_endpoint: str, device_type: str) -> None:
        self.x = 0
        self.id = id
        self.interval = interval
        self.base_station_endpoint = base_station_endpoint
        self.device_type = device_type

    async def start_sensor(self) -> None:
        while True:
            reading = self.generate_data()
            data = self.create_output_data(reading)
            try:
                await self.send_data(data)
            except aiohttp.ClientConnectorError as e:
                print(f"connection is not available: {e}")
            await sleep(self.interval)

    def create_output_data(self, _reading):
        return {
            "sensor_id": self.id,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_data(self):
        self.x += 1
        value = 2 * math.sin(self.x) + 3
        value += 3 * random.random()
        return value

    async def send_data(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_station_endpoint, json=data) as resp:
                if resp.status != 200:
                    # throw an exception
                    raise Exception(
                        f"Error sending data to base station. status code: {resp.status}, response: {resp.text}"
                    )
                else:
                    print(f"Data sent to base station: {data}")
    
    async def start(self) -> None:
        if self.device_type == "sensor":
            await self.start_sensor()
        else:
            self.start_actuator()
    
    def start_actuator(self) -> None:
        print("start_actuator(self) - waiting for the instruction from IoT Base Station")


class TemperatureSimulator(Simulator):
    def create_output_data(self, reading):
        data = super().create_output_data(reading)
        data["temperature"] = reading
        return data


class SoilMoistureSimulator(Simulator):
    def create_output_data(self, reading):
        data = super().create_output_data(reading)
        data["soil_moisture"] = reading
        return data


class WaterLevelSimulator(Simulator):
    def create_output_data(self, reading):
        data = super().create_output_data(reading)
        data["water_level"] = reading
        return data


class WaterPollutionSimulator(Simulator):
    def create_output_data(self, reading):
        data = super().create_output_data(reading)
        data["water_pollution"] = reading
        return data

class WaterSprinklerSimulator(Simulator):
    def create_output_data(self, reading):
        data = super().create_output_data(reading)
        data["temperature"] = reading
        return data

class WaterPumpSimulator(Simulator):
    def create_output_data(self, reading):
        data = super().create_output_data(reading)
        data["soil_moisture"] = reading
        return data