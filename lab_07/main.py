from models.gen_models import (
    GenDriver,
    GenTrip,
    GenCar,
    GenPassenger,
    GenPayment,
)

from models.sschemes import (
    SCarScheme,
    SRequestTripWithScore,
    SDriverTripStats,
    SMetadata,
    STripsDriverPassengerInfo,
    SScoreBeforeAfterRequest,
)

from database.database import DataBase
from database.data_first import DataFirstDao
from database.task_1 import PyLinqClass
from database.task_2 import PyLinqJson
from generator import generate_csv
from config import Colors

import asyncio
import os

script_file = os.path.abspath(__file__)
script_dir = os.path.dirname(script_file)

DRIVERS_FILE = script_dir + "/data/drivers.csv"
TRIPS_FILE = script_dir + "/data/trips.csv"
PASSENGERS_FILE = script_dir + "/data/passengers.csv"
PAYMENTS_FILE = script_dir + "/data/payments.csv"
CARS_FILE = script_dir + "/data/cars.csv"

# Файлы для второй лабы
DML_FILEDIR = script_dir + "/sql_dml"
DML_OPEATIONS_PATH = script_dir + "/sql_dml/2_lab.sql"

MAX_OPERATIONS = 3


database = DataBase()


def print_menu():
    print(
        "0. Выход\n \
        1. LINQ to Object\n \
        2. LINQ to JSON\n \
        3. LINQ to SQL"
    )


def input_operation():
    operation = 0
    while True:
        try:
            operation = int(input("Введите номер операции: "))
            if operation > MAX_OPERATIONS or operation < 0:
                print(f"ОПЕРАЦИЯ ДОЛЖНА ВХОДИТЬ В ДИАПАЗОН ОТ 0 ДО {MAX_OPERATIONS}")
            else:
                return operation
        except Exception:
            print(f"ОПЕРАЦИЯ ВВЕДЕНА НЕПРАВИЛЬНО")


async def generate():
    print("dropping database")
    try:
        await database.drop_table()
    except Exception as e:
        print("database doesn`t exist")

    print("create tables")
    await database.create_tables()

    generate_csv(GenCar, CARS_FILE)
    generate_csv(GenDriver, DRIVERS_FILE)
    generate_csv(GenPassenger, PASSENGERS_FILE)
    generate_csv(GenPayment, PAYMENTS_FILE)
    generate_csv(GenTrip, TRIPS_FILE)

    print("copying")
    await database.copy_tables()


async def main():
    # Генерация базы данных
    # await generate()
    print_menu()
    operation = input_operation()

    match operation:
        case 1:
            await PyLinqClass.task_1()
        case 2:
            await PyLinqJson.task_2()


if __name__ == "__main__":
    asyncio.run(main())
