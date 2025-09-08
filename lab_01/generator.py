"""
Программа для генерации случайных тестовых данных для таблиц
"""

from models import Driver, Trip, Car, Passanger, Payment
from config import last_name_list, first_name_list, random_adresses, cars_dict

import random
from datetime import datetime, timedelta
from string import ascii_letters

# Нужно для того чтобы не повторять id

driver_count = 1
trip_count = 1
passanger_count = 1
payment_count = 1
generated_cars = set()
using_cars = set()
cars_id_index = 0


class DataGenerator:
    def __init__(self):
        pass

    @classmethod
    def generate_birth_date(cls, min_age=18, max_age=65):
        """Генерирует случайную дату рождения для возраста от min_age до max_age"""
        today = datetime.now()
        max_birth_date = today - timedelta(days=(min_age * 365))
        min_birth_date = today - timedelta(days=(max_age * 365))

        delta = max_birth_date - min_birth_date
        random_days = random.randint(0, delta.days)

        return (min_birth_date + timedelta(days=random_days)).date()

    @classmethod
    def generate_vin_numbrer(cls):
        lenn = 10
        string = ""

        for i in range(lenn):
            string += random.choice(ascii_letters)

        return string

    @classmethod
    def generate_plate(cls):
        """Генерация номернх знаков в формате А111АА11"""
        plate: str = ""

        plate += random.choice(ascii_letters)
        plate += str(random.randint(100, 999))
        plate += random.choice(ascii_letters)
        plate += random.choice(ascii_letters)

        plate += str(random.randint(10, 99))

        return plate

    @classmethod
    def generate_driver(cls) -> Driver:
        global driver_count, trip_count, passanger_count, payment_count, generated_cars, cars_id_index

        driver: Driver = Driver()

        driver.driver_id = driver_count
        driver_count += 1

        driver.car_id = random.randint(0, 1000)
        driver.first_name = first_name_list[random.randint(0, len(first_name_list) - 1)]
        driver.last_name = last_name_list[random.randint(0, len(last_name_list) - 1)]

        driver.experience = random.randint(0, 50)
        driver.score = random.randint(300, 501) / 100
        driver.date_of_birthday = DataGenerator.generate_birth_date()

        driver.adress = random_adresses[random.randint(0, len(random_adresses) - 1)]
        driver.document_number = random.randint(0, 1000000)

        return driver

    @classmethod
    def generate_trip(cls) -> Trip:
        trip = Trip()
        global trip_count

        trip.trip_id = trip_count
        trip_count += 1

        trip.driver_id = random.randint(0, 10000)
        trip.passenger_id = random.randint(0, 10000)
        trip.payment_id = random.randint(0, 1000)
        trip.source_adress = random_adresses[
            random.randint(0, len(random_adresses) - 1)
        ]
        trip.destenation_adress = random_adresses[
            random.randint(0, len(random_adresses) - 1)
        ]
        trip.price = random.randint(1000, 5000)
        trip.score = random.randint(2, 5)

        return trip

    @classmethod
    def generate_passanger(cls) -> Passanger:
        passanger = Passanger()

        driver.first_name = first_name_list[random.randint(0, len(first_name_list) - 1)]
        driver.last_name = last_name_list[random.randint(0, len(last_name_list) - 1)]

        driver.date_of_birthday = DataGenerator.generate_birth_date()
        driver.adress = random_adresses[random.randint(0, len(random_adresses) - 1)]

        return passanger

    @classmethod
    def generate_payment(cls) -> Payment:
        payment = Payment()

        payment.payment_id = random.randint(0, 1000)
        payment.invoice = random.randint(1000000, 9999999)
        payment.status = True

        return payment

    @classmethod
    def generate_car(cls) -> Car:
        car = Car()

        car.vin_number = DataGenerator.generate_vin_numbrer()
        car.registration_plate = DataGenerator.generate_plate()

        models = list(cars_dict.keys())
        car.brand = models[random.randint(0, len(models) - 1)]
        car.model = cars_dict[car.brand][random.randint(0, len(cars_dict[car.brand]))]
        car.mileage = random.randint(0, 1000000)

        return car


if __name__ == "__main__":
    car = DataGenerator.generate_car()
    print(car)
