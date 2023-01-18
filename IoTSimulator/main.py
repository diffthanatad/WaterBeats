import asyncio
from argparse import ArgumentParser
from simulator import SimpleSimulatorFactory, Simulator


async def main():
    parser = ArgumentParser()
    parser.add_argument("--id", type=str, required=True, help="sensor id")
    parser.add_argument(
        "--interval", type=int, default=3, help="The interval between two data sending"
    )
    parser.add_argument(
        "--target", type=str, required=True, help="URL of the IoT base station"
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="Type of the sensor (temperature, soil_moisture, water_level, water_pollution)",
    )
    args = parser.parse_args()
    simulator = SimpleSimulatorFactory.create(
        args.type, args.id, args.interval, args.target
    )
    await simulator.start()


if __name__ == "__main__":
    asyncio.run(main())
