from benchmark import Benchmark

import asyncio


async def main():
    benchmark = Benchmark(delay=1, exp_count=8, update_delay=4)
    await benchmark.run_benchmark()


if __name__ == "__main__":
    asyncio.run(main())
