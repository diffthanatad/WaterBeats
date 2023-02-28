import asyncio
import time
from enum import Enum
import math
import random
from asyncio import sleep
import aiohttp
from datetime import datetime

import websockets


class SimpleSimulatorFactory:
    """
    This is a simple factory class that creates a simulator based on the sensor type.
    """

    def create(
        sensor_type: str,
        id: str,
        interval: int,
        base_station_endpoint: str,
        # device_type: str,
        # actuator_type: str,
        longitude: str,
        latitude: str,
        unit : str
    ) -> "Simulator":
        # if device_type == "sensor":
        if sensor_type == "temperature":
            simulator = TemperatureSimulator(
                id, interval, base_station_endpoint,longitude,latitude, unit
            )
        elif sensor_type == "soil_moisture":
            simulator = SoilMoistureSimulator(
                id, interval, base_station_endpoint, longitude, latitude, unit
            )
        elif sensor_type == "water_level":
            simulator = WaterLevelSimulator(
                id, interval, base_station_endpoint, longitude, latitude, unit
            )
        elif sensor_type == "water_pollution":
            simulator = WaterPollutionSimulator(
                id, interval, base_station_endpoint, longitude, latitude, unit
            )
        else:
            raise Exception(f"Unknown sensor type: {sensor_type}")
        # elif device_type == "actuator":
        #     if actuator_type == "water_sprinkler":
        #         simulator = WaterSprinklerSimulator(
        #             id, interval, base_station_endpoint, device_type
        #         )
        #     elif actuator_type == "water_pump":
        #         simulator = WaterPumpSimulator(
        #             id, interval, base_station_endpoint, device_type
        #         )
        #     else:
        #         raise Exception(f"Unknown actuator type: {actuator_type}")
        # else:
        #     raise Exception(f"Unknown device type: {device_type}")
        return simulator


class Simulator:
    def __init__(
        self, id: str, interval: int, base_station_endpoint: str, longitude: str, latitude: str, unit: str
    ) -> None:
        """
        This is the base class for all the simulators.
        """
        self.x = 0
        self.id = id
        self.interval = interval
        self.longitude = longitude
        self.latitude = latitude
        self.base_station_endpoint = base_station_endpoint
        self.unit = unit

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
            # "timestamp": datetime.now().isoformat(),
            "timestamp" : time.time_ns(),
            "longitude": self.longitude,
            "latitude" : self.latitude,
            "unit" : self.unit
        }

    def generate_data(self):
        self.x += 1
        value = 2 * math.sin(self.x) + 3
        value += 3 * random.random()
        return value

    async def send_data(self, data) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_station_endpoint, json=data) as resp:
                if resp.status != 200:
                    # throw an exception
                    raise Exception(
                        f"Error sending data to base station. status code: {resp.status}, response: {resp.text}"
                    )
                    return f"Error sending data to base station. status code: {resp.status}, response: {resp.text}"
                else:
                    print(f"Data sent to base station: {data}")
                    return f"Data sent to base station: {data}"

    # async def start(self) -> None:
    #     if self.device_type == "sensor":
    #         await self.start_sensor()
    #     else:
    #         await self.start_actuator()

    async def start_actuator(self) -> None:
        print("testing:", self.base_station_endpoint)
        async with websockets.connect(self.base_station_endpoint) as ws:
            while True:
                raw_text: str = await ws.recv()
                asyncio.get_event_loop().create_task(self.handle_message(raw_text))


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


class SprinklerStatus(Enum):
    ON = 1
    OFF = 2


class WaterSprinklerSimulator(Simulator):
    def __init__(
        self, id: str, interval: int, base_station_endpoint: str, device_type: str
    ) -> None:
        super().__init__(id, interval, base_station_endpoint, device_type)
        self.sprinkler = SprinklerStatus.OFF

    async def handle_message(self, raw_text: str) -> str:
        print(f"Received message: {raw_text}")
        if raw_text == "on":
            self.sprinkler = SprinklerStatus.ON
            print("Turning on the sprinkler")
            return "Turning on the sprinkler"
        elif raw_text == "off":
            self.sprinkler = SprinklerStatus.OFF
            print("Turning off the sprinkler")
            return "Turning off the sprinkler"


class WaterPumpSimulator(Simulator):
    async def handle_message(self, raw_text: str) -> None:
        # TODO:
        print(f"Executing {raw_text}")
