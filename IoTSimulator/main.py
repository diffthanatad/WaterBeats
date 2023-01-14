import asyncio
from simulator import Simulator

async def main():
    simulator = Simulator("http://localhost:23333/new_data")
    await simulator.start()

if __name__ == "__main__":
    asyncio.run(main())
