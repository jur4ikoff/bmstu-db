# В будущем можно сделать нормально, но пока пусть будет базовая модель, которая будет храниться в базе
from dataset import last_name_list, first_name_list, random_adresses, cars_dict

from datetime import datetime, timedelta, date
from string import ascii_letters
import random


def generate_birth_date(min_age=18, max_age=65):
    """Генерирует случайную дату рождения для возраста от min_age до max_age"""
    today = datetime.now()
    max_birth_date = today - timedelta(days=(min_age * 365))
    min_birth_date = today - timedelta(days=(max_age * 365))

    delta = max_birth_date - min_birth_date
    random_days = random.randint(0, delta.days)

    return (min_birth_date + timedelta(days=random_days)).date()


class Driver:
    driver_id: int
    car_id: int
    first_name: str
    last_name: str
    experience: str
    score: str
    date_of_birthday: date
    adress: str
    document_number: int

    def __str__(self):
        return (
            f"id={self.driver_id}, car_id={self.car_id}, first_name={self.first_name}, "
            f"last_name={self.last_name}, experience={self.experience}, score={self.score}, "
            f"date_of_birthday={self.date_of_birthday}, adress={self.adress}, document_number={self.document_number}"
        )

    @classmethod
    def generate(cls):
        driver: Driver = Driver()

        driver.driver_id = random.randint(0, 10000)
        driver.car_id = random.randint(0, 10000)

        driver.first_name = first_name_list[random.randint(0, len(first_name_list) - 1)]
        driver.last_name = last_name_list[random.randint(0, len(last_name_list) - 1)]

        driver.experience = random.randint(0, 50)
        driver.score = random.randint(300, 501) / 100
        driver.date_of_birthday = generate_birth_date()

        driver.adress = random_adresses[random.randint(0, len(random_adresses) - 1)]
        driver.document_number = random.randint(0, 1000000)

        return driver

    @classmethod
    def headers(cls):
        res = [
            "driver_id",
            "car_id",
            "first_name",
            "last_name",
            "experience",
            "score",
            "date_of_birthday",
            "adress",
            "document_number",
        ]
        return res

    def to_list(self):
        res = [
            self.driver_id,
            self.car_id,
            self.first_name,
            self.last_name,
            self.experience,
            self.score,
            self.date_of_birthday,
            self.adress,
            self.document_number,
        ]

        return res


class Trip:
    trip_id: int
    driver_id: int
    passenger_id: int
    payment_id: int
    source_adress: str
    destenation_adress: str
    price: int
    score: int

    @classmethod
    def generate(cls):
        trip = Trip()
        global trip_count

        trip.trip_id = random.randint(0, 100000)

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

    def __str__(self):
        return (
            f"id={self.trip_id}, driver_id={self.driver_id}, passenger_id={self.passenger_id}, "
            f"payment_id={self.payment_id}, src_adress={self.source_adress}, "
            f"dest_adress={self.source_adress}, price={self.price}, score={self.score}"
        )

    @classmethod
    def headers(cls):
        res = [
            "trip_id",
            "driver_id",
            "passenger_id",
            "payment_id",
            "source_adress",
            "destenation_adress",
            "price",
            "score",
        ]
        return res

    def to_list(self):
        res = [
            self.trip_id,
            self.driver_id,
            self.passenger_id,
            self.payment_id,
            self.source_adress,
            self.destenation_adress,
            self.price,
            self.score,
        ]

        return res


class Passenger:
    passenger_id: int
    first_name: str
    last_name: str
    date_of_birthday: date
    adress: str

    @classmethod
    def generate(cls):
        passenger = Passenger()

        passenger.passenger_id = random.randint(0, 10000)
        passenger.first_name = first_name_list[
            random.randint(0, len(first_name_list) - 1)
        ]
        passenger.last_name = last_name_list[random.randint(0, len(last_name_list) - 1)]

        passenger.date_of_birthday = generate_birth_date()
        passenger.adress = random_adresses[random.randint(0, len(random_adresses) - 1)]

        return passenger

    def __str__(self):
        return (
            f"id={self.passenger_id}, first_name={self.first_name}, last_name={self.last_name}, "
            f"date_of_birthday={self.date_of_birthday}, adress={self.adress}, "
        )

    @classmethod
    def headers(cls):
        res = ["passenger_id", "first_name", "last_name", "date_of_birthday", "adress"]
        return res

    def to_list(self):
        res = [
            self.passenger_id,
            self.first_name,
            self.last_name,
            self.date_of_birthday,
            self.adress,
        ]

        return res


class Payment:
    payment_id: int
    invoice: int
    status: bool

    @classmethod
    def generate(cls):
        payment = Payment()

        payment.payment_id = random.randint(0, 1000)
        payment.invoice = random.randint(1000000, 9999999)
        payment.status = True

        return payment

    @classmethod
    def headers(cls):
        res = ["payment_id", "invoice", "status"]
        return res

    def to_list(self):
        res = [
            self.payment_id,
            self.invoice,
            self.status,
        ]

        return res

    def __str__(self):
        return f"id={self.payment_id}, invoice={self.invoice}, status={self.status}"


class Car:
    vin_number: int
    registration_plate: str
    brand: str
    model: str
    mileage: int

    @classmethod
    def generate_vin_numbrer(cls):
        lenn = 10
        string = ""

        for _ in range(lenn):
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
    def generate(cls):
        car = Car()

        car.vin_number = cls.generate_vin_numbrer()
        car.registration_plate = cls.generate_plate()

        models = list(cars_dict.keys())
        car.brand = models[random.randint(0, len(models) - 1)]
        car.model = cars_dict[car.brand][
            random.randint(0, len(cars_dict[car.brand]) - 1)
        ]
        car.mileage = random.randint(0, 1000000)

        return car

    @classmethod
    def headers(cls):
        res = ["vin_number", "registration_plate", "brand", "model", "mileage"]
        return res

    def to_list(self):
        res = [
            self.vin_number,
            self.registration_plate,
            self.brand,
            self.model,
            self.mileage,
        ]

        return res

    def __str__(self):
        return f"vin={self.vin_number}, plate={self.registration_plate}, brand={self.brand}, model={self.model}, mileage={self.mileage}"
