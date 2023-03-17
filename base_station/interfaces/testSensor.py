import asyncio
import json
import math
import random
import aiohttp
from asyncio import sleep

class Sensor:
    def __init__(self, id, end_point):
        self.x = 0
        self.id = id
        self.end_point = end_point
        self.interval = 2

    def generate_data(self):
        self.x += 1
        value = 2 * math.sin(self.x) + 3
        value += 3 * random.random()
        return value

    async def send_data(self, data) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.end_point, json=json.dumps(data)) as resp:
                if resp.status != 200:
                    # throw an exception
                    raise Exception(
                        f"Error sending data to base station. status code: {resp.status}, response: {resp.text}"
                    )
                    return f"Error sending data to base station. status code: {resp.status}, response: {resp.text}"
                else:
                    print(f"Data sent to base station: {data}")
                    return f"Data sent to base station: {data}"

    async def run(self):
        while True:
            reading = self.generate_data()
            data = {
                "sensor_id" : self.id,
                "reading" : reading
                }
            try:
                await self.send_data(data)
            except aiohttp.ClientConnectorError as e:
                print(f"connection is not available: {e}")
            await sleep(self.interval)


if __name__ == '__main__':
    sensor_test = Sensor("F4:12:FA:83:00:F0_B", "http://localhost:23333/sensor_data")
    asyncio.run(sensor_test.run())