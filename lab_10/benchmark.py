import asyncio
import time
from datetime import date
import asyncio
import csv
import random
from sqlalchemy import select, delete, update

from config import Colors

from database import async_session_maker
from driver.dao import DriverDAO
from driver.models import Driver
from trip.models import Trip
from stats import get_stats_from_db, get_stats_from_redis, update_cache

LOGS_PATH = "./time.csv"
HEADERS = ["exp_name", "DB", "Redis"]


async def insert_random_data(update_delay, exp_count, delay):
    print("Вставка")
    """Вставка рандомных данных раз в delay секунд"""
    for _ in range(int(exp_count * delay / update_delay)):
        async with async_session_maker() as session:
            driver = Driver(
                car_id=1,
                first_name=f"Driver{random.randint(1,1000)}",
                last_name="Test",
                experience=5,
                score=4.5,
                date_of_birthday=date(1990, 1, 1),
                document_number=random.randint(100000000, 9999999999),
            )
            session.add(driver)
            await session.flush()

            # Создаём Trip
            trip = Trip(
                driver_id=driver.id,
                passenger_id=1,
                payment_id=1,
                source_address="Moscow",
                destenation_address="SPB",
                price=1000,
                score=5,
            )
            session.add(trip)
            await session.commit()

        duration = await update_cache()
        print(f"Кэш Redis Обновлен за {duration : .4f}s")
        await asyncio.sleep(update_delay)


async def update_random_driver_score(update_delay, exp_count, delay):
    print("Обновление элемента")
    for _ in range(int(exp_count * delay / update_delay)):
        async with async_session_maker() as session:
            query = select(Driver.id).order_by(Driver.id.desc()).limit(1)
            result = await session.execute(query)
            driver_id = result.scalar()
            if driver_id:
                new_score = round(random.uniform(3.0, 5.0), 1)
                await session.execute(
                    update(Driver).where(Driver.id == driver_id).values(score=new_score)
                )
                await session.commit()

    duration = await update_cache()
    print(f"Кэш Redis Обновлен за {duration : .4f}s")
    await asyncio.sleep(update_delay)


async def delete_random_trip(update_delay, exp_count, delay):
    print("Удаление элементов")
    for _ in range(int(exp_count * delay / update_delay)):
        async with async_session_maker() as session:
            query = select(Trip.id).order_by(Trip.id.desc()).limit(1)
            result = await session.execute(query)
            trip_id = result.scalar()
            if trip_id:
                await session.execute(delete(Trip).where(Trip.id == trip_id))
                await session.commit()

    duration = await update_cache()
    print(f"Кэш Redis Обновлен за {duration : .4f}s")
    await asyncio.sleep(update_delay)


class Benchmark:
    def __init__(self, delay=5, exp_count=6, update_delay=10):
        self.delay = delay
        self.exp_count = exp_count
        self.update_delay = update_delay

    async def __run_default_benchmark(self, verbose: bool = True, tag="default"):
        if verbose:
            print(
                f"{Colors.BG_GREEN}Начало теста. Без изменений {self.delay * self.exp_count} секунд...{Colors.RESET}"
            )

        for i in range(self.exp_count):  # 30 сек без изменений
            _, db_time = await get_stats_from_db()
            _, redis_time = await get_stats_from_redis()
            print(f"[{i+1}] DB: {db_time:.4f}s | Redis: {redis_time:.4f}s")
            self.writer.writerow([tag, db_time, redis_time])
            await asyncio.sleep(self.delay)

    async def __run_insert_benchmark(self):
        print(
            f"{Colors.BG_GREEN}Начало теста. ВСТАВКА строк раз в {self.update_delay} секунд...{Colors.RESET}"
        )
        task_1 = asyncio.create_task(
            insert_random_data(self.update_delay, self.exp_count, self.delay)
        )
        task_2 = asyncio.create_task(
            self.__run_default_benchmark(verbose=False, tag="insert")
        )

        await asyncio.gather(task_1, task_2)

    async def __run_update_benchmark(self):
        print(
            f"{Colors.BG_GREEN}Начало теста. Обновление строк раз в {self.update_delay} секунд...{Colors.RESET}"
        )
        task_1 = asyncio.create_task(
            update_random_driver_score(self.update_delay, self.exp_count, self.delay)
        )
        task_2 = asyncio.create_task(
            self.__run_default_benchmark(verbose=False, tag="update")
        )

        await asyncio.gather(task_1, task_2)

    async def __run_delete_benchmark(self):
        print(
            f"{Colors.BG_GREEN}Начало теста. Удаление строк раз в {self.update_delay} секунд...{Colors.RESET}"
        )
        task_1 = asyncio.create_task(
            delete_random_trip(self.update_delay, self.exp_count, self.delay)
        )
        task_2 = asyncio.create_task(
            self.__run_default_benchmark(verbose=False, tag="delete")
        )

        await asyncio.gather(task_1, task_2)

    async def run_benchmark(self):
        file = open(LOGS_PATH, mode="w", encoding="utf-8", newline="")
        self.writer = csv.writer(file, delimiter=";")
        self.writer.writerow(HEADERS)

        await self.__run_default_benchmark()
        await self.__run_insert_benchmark()
        await self.__run_update_benchmark()
        await self.__run_delete_benchmark()

        file.close()
