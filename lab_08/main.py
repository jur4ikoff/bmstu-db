from gen_models import (
    GenDriver,
    GenTrip,
    GenCar,
    GenPassenger,
    GenPayment,
)

from generator import generate_csv

from datetime import datetime

import asyncio
import os

SLEEP_TIME = 4

script_file = os.path.abspath(__file__)
script_dir = os.path.dirname(script_file)


def generate_filename(model_name: str) -> str:
    cur_time = datetime.now()
    date_now = cur_time.date()
    time_now = str(cur_time.time()).split(".")[0]
    return f"{script_dir}/data/{date_now}_{time_now}_{model_name}.csv"


async def generate_files():
    generate_csv(GenCar, generate_filename("car"))
    generate_csv(GenDriver, generate_filename("driver"))
    generate_csv(GenPassenger, generate_filename("passenger"))
    generate_csv(GenPayment, generate_filename("payment"))
    generate_csv(GenTrip, generate_filename("trip"))


async def main():
    # Генерация файлов
    while True:
        await generate_files()
        await asyncio.sleep(SLEEP_TIME)


if __name__ == "__main__":
    asyncio.run(main())
