import asyncio
import random
from simulator import SimpleSimulatorFactory

longitude = random.uniform(-1000,1000)
latitude = random.uniform(-1000,1000)
unit = "C"
sensor = SimpleSimulatorFactory.create("temperature","2023",2,"http://localhost:23333/new_data",longitude,latitude, unit)

if __name__ == '__main__':
    asyncio.run(sensor.start_sensor())