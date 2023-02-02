import asyncio
from argparse import ArgumentParser
from sprinkler import Sprinkler
from pump import Pump


async def main():
    parser = ArgumentParser()
    parser.add_argument("--id", type=str, required=True, help="sensor / actuator id")
    parser.add_argument(
        "--interval", type=int, default=3, help="The interval between two data sending"
    )
    parser.add_argument(
        "--target", type=str, required=True, help="URL of the IoT base station"
    )

    parser.add_argument(
        "--actuator_type",
        type=str,
        help="Type of the actuator (water_sprinkler, water_pump)",
    )

    args = parser.parse_args()
    if args.actuator_type == "water_sprinkler":
        actuator = Sprinkler(args.id, args.target)
    elif args.actuator_type == "water_pump":
        actuator = Pump(args.id, args.target)
    await actuator.receive_commands()


if __name__ == "__main__":
    asyncio.run(main())
