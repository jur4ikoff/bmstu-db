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

from database.database import DataBase


async def generate():
    print("create database")
    database = DataBase()
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


async def main():
    await generate()


if __name__ == "__main__":
    asyncio.run(main())
