from models import Driver, Trip, Car, Passenger, Payment
from generator import generate_csv

from dotenv import load_dotenv
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

from database.database import DataBase
database = DataBase()

async def generate():
    print("dropping database")
    try:
        await database.drop_table()
    except Exception as e:
        print("database doesn`t exist")

    print("create tables")
    await database.create_tables()

    generate_csv(Car, CARS_FILE)
    generate_csv(Driver, DRIVERS_FILE)
    generate_csv(Passenger, PASSENGERS_FILE)
    generate_csv(Payment, PAYMENTS_FILE)
    generate_csv(Trip, TRIPS_FILE)

    print("copying")
    await database.copy_tables()

async def dml_operations(filedir: str):
    files = os.listdir(filedir)

    for file in files:
        if ".sql" in file: 
            await database.dml_run(file)


async def main():
    # Создание базы данных - первая лаба
    # await generate()

    # Запуск dml, вторая лаба
    await dml_operations(DML_FILEDIR)


if __name__ == "__main__":
    asyncio.run(main())
