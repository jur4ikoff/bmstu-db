from models import Driver, Trip, Car, Passenger, Payment
import os
import csv

script_file = os.path.abspath(__file__)
script_dir = os.path.dirname(script_file)

DRIVERS_FILE = script_dir + "/data/drivers.csv"
TRIPS_FILE = script_dir + "/data/trips.csv"
PASSENGERS_FILE = script_dir + "/data/passengers.csv"
PAYMENTS_FILE = script_dir + "/data/payments.csv"
CARS_FILE = script_dir + "/data/cars.csv"

GENERATE_COUNT = 1000


def generate_csv(model, filename: str):
    """Функция для генерации csv файлов"""
    if os.path.exists(filename):
        os.remove(filename)

    with open(file=filename, mode="w", newline="", encoding="utf-8") as file:
        for i in range(GENERATE_COUNT + 1):
            if i == 0:
                line = model.headers()
            else:
                generate_model = model.generate()
                line = generate_model.to_list()

            writer = csv.writer(file, delimiter=";")
            writer.writerow(line)


def main():
    generate_csv(Driver, DRIVERS_FILE)
    generate_csv(Trip, TRIPS_FILE)
    generate_csv(Passenger, PASSENGERS_FILE)
    generate_csv(Payment, PAYMENTS_FILE)
    generate_csv(Car, CARS_FILE)


if __name__ == "__main__":
    main()
