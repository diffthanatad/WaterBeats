import math
import random
import time
from asyncio import sleep
import aiohttp
from datetime import datetime

class Simulator:
    def __init__(self, base_station_endpoint: str) -> None:
        self.x = 0
        self.base_station_endpoint = base_station_endpoint

    async def start(self) -> None:
        while True:
            reading = self.generate_data()
            data = {
                "timestamp": datetime.now().isoformat(),
                "soil_moisture": reading,
            }
            await self.send_data(data)
            await sleep(1)

    def generate_data(self):
        self.x += 1
        value = 2 * math.sin(self.x) + 3
        value += 3 * random.random()
        return value

    async def send_data(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_station_endpoint, data=data) as resp:
                if resp.status != 200:
                    # throw an exception
                    raise Exception(
                        f"Error sending data to base station. status code: {resp.status}, response: {resp.text}"
                    )
                else:
                    print(f"Data sent to base station: {data}")
