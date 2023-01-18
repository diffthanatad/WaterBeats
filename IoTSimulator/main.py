import asyncio
from argparse import ArgumentParser
from simulator import Simulator


async def main():
    parser = ArgumentParser()
    parser.add_argument("--id", type=str, required=True, help="sensor id")
    parser.add_argument(
        "--freq", type=int, default=1, help="The data sampling rate in seconds"
    )
    parser.add_argument(
        "--target", type=str, required=True, help="URL of the IoT base station"
    )
    args = parser.parse_args()
    simulator = Simulator(args.id, args.freq, args.target)
    await simulator.start()


if __name__ == "__main__":
    asyncio.run(main())
