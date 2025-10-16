# В будущем можно сделать нормально, но пока пусть будет базовая модель, которая будет храниться в базе
from dataset import last_name_list, first_name_list, random_adresses, cars_dict

from datetime import datetime, timedelta, date
from string import ascii_uppercase, digits
import random


def generate_birth_date(min_age=18, max_age=65):
    """Генерирует случайную дату рождения для возраста от min_age до max_age"""
    today = datetime.now()
    max_birth_date = today - timedelta(days=(min_age * 365))
    min_birth_date = today - timedelta(days=(max_age * 365))

    delta = max_birth_date - min_birth_date
    random_days = random.randint(0, delta.days)

    return (min_birth_date + timedelta(days=random_days)).date()


class GenDriver:
    id: int
    car_id: int
    first_name: str
    last_name: str
    experience: int
    score: str
    date_of_birthday: date
    address: str
    document_number: int

    def __str__(self):
        return (
            f"id={self.id}, car_id={self.car_id}, first_name={self.first_name}, "
            f"last_name={self.last_name}, experience={self.experience}, score={self.score}, "
            f"date_of_birthday={self.date_of_birthday}, adress={self.address}, document_number={self.document_number}"
        )

    @classmethod
    def generate(cls, primary_key: int, secondary_key: list):
        """secondary_key - Массив, из которого будут брать данные для FK"""

        driver: GenDriver = GenDriver()
        driver.id = primary_key

        car_id_index = random.randint(0, len(secondary_key) - 1)
        driver.car_id = secondary_key.pop(car_id_index)

        driver.first_name = first_name_list[random.randint(0, len(first_name_list) - 1)]
        driver.last_name = last_name_list[random.randint(0, len(last_name_list) - 1)]

        driver.experience = random.randint(0, 50)
        driver.score = random.randint(300, 501) / 100
        driver.date_of_birthday = generate_birth_date()

        driver.address = random_adresses[random.randint(0, len(random_adresses) - 1)]
        driver.document_number = random.randint(100000000, 9999999999)

        return driver

    def to_list(self):
        res = [
            self.car_id,
            self.first_name,
            self.last_name,
            self.experience,
            self.score,
            self.date_of_birthday,
            self.address,
            self.document_number,
        ]
        return res

    @classmethod
    def headers(cls):
        return [
            "car_id",
            "first_name",
            "last_name",
            "experience",
            "score",
            "date_of_birthday",
            "address",
            "document_number",
        ]


class GenTrip:
    id: int
    driver_id: int
    passenger_id: int
    payment_id: int
    source_address: str
    destenation_address: str
    price: int
    score: int

    @classmethod
    def generate(cls, id: int, payment_id: list):
        trip = GenTrip()
        global trip_count

        trip.id = id

        trip.driver_id = random.randint(1, 1000)
        trip.passenger_id = random.randint(1, 1000)

        payment_id_index = random.randint(0, len(payment_id) - 1)
        trip.payment_id = payment_id.pop(payment_id_index)

        trip.source_address = random_adresses[
            random.randint(0, len(random_adresses) - 1)
        ]
        trip.destenation_address = random_adresses[
            random.randint(0, len(random_adresses) - 1)
        ]
        trip.price = random.randint(1000, 5000)
        trip.score = random.randint(2, 5)

        return trip

    def __str__(self):
        return (
            f"id={self.id}, driver_id={self.driver_id}, passenger_id={self.passenger_id}, "
            f"payment_id={self.payment_id}, src_adress={self.source_address}, "
            f"dest_adress={self.source_address}, price={self.price}, score={self.score}"
        )

    def to_list(self):
        res = [
            self.driver_id,
            self.passenger_id,
            self.payment_id,
            self.source_address,
            self.destenation_address,
            self.price,
            self.score,
        ]
        return res

    @classmethod
    def headers(cls):
        return [
            "driver_id",
            "passenger_id",
            "payment_id",
            "source_address",
            "destenation_address",
            "price",
            "score",
        ]


class GenPassenger:
    id: int
    first_name: str
    last_name: str
    date_of_birthday: date
    address: str

    @classmethod
    def generate(cls, primary_key=None):
        passenger = GenPassenger()

        if primary_key:
            passenger.id = primary_key
        else:
            passenger.id = random.randint(0, 1000000)
        passenger.first_name = first_name_list[
            random.randint(0, len(first_name_list) - 1)
        ]
        passenger.last_name = last_name_list[random.randint(0, len(last_name_list) - 1)]

        passenger.date_of_birthday = generate_birth_date()
        passenger.address = random_adresses[random.randint(0, len(random_adresses) - 1)]

        return passenger

    def __str__(self):
        return (
            f"id={self.id}, first_name={self.first_name}, last_name={self.last_name}, "
            f"date_of_birthday={self.date_of_birthday}, adress={self.address}, "
        )

    def to_list(self):
        res = [
            self.first_name,
            self.last_name,
            self.date_of_birthday,
            self.address,
        ]
        return res

    @classmethod
    def headers(cls):
        return [
            "first_name",
            "last_name",
            "date_of_birthday",
            "address",
        ]


class GenPayment:
    id: int
    invoice: int
    status: bool

    @classmethod
    def generate(cls, primary_key: int):
        payment = GenPayment()
        payment.id = primary_key

        payment.invoice = random.randint(100000, 999999)
        payment.status = True

        return payment

    def to_list(self):
        res = [
            self.invoice,
            self.status,
        ]
        return res

    @classmethod
    def headers(cls):
        return [
            "invoice",
            "status",
        ]

    def __str__(self):
        return f"id={self.id}, invoice={self.invoice}, status={self.status}"


class GenCar:
    id: int
    vin_number: int
    registration_plate: str
    brand: str
    model: str
    mileage: int

    @classmethod
    def generate_vin_numbrer(cls, primary_key=None):
        lenn = 10
        string = ""

        for _ in range(lenn):
            string += random.choice(ascii_uppercase + digits)

        return string

    @classmethod
    def generate_plate(cls):
        """Генерация номернх знаков в формате А111АА11"""
        plate: str = ""

        plate += random.choice(ascii_uppercase)
        plate += str(random.randint(100, 999))
        plate += random.choice(ascii_uppercase)
        plate += random.choice(ascii_uppercase)

        plate += str(random.randint(10, 99))

        return plate

    @classmethod
    def generate(cls, primary_key=None):
        car = GenCar()

        if primary_key:
            car.id = primary_key
        else:
            car.id = random.randint(1, 100000)

        car.vin_number = cls.generate_vin_numbrer()
        car.registration_plate = cls.generate_plate()

        models = list(cars_dict.keys())
        car.brand = models[random.randint(0, len(models) - 1)]
        car.model = cars_dict[car.brand][
            random.randint(0, len(cars_dict[car.brand]) - 1)
        ]
        car.mileage = random.randint(0, 1000000)

        return car

    def to_list(self):
        res = [
            self.vin_number,
            self.registration_plate,
            self.brand,
            self.model,
            self.mileage,
        ]
        return res

    @classmethod
    def headers(cls):
        return [
            "vin_number",
            "registration_plate",
            "brand",
            "model",
            "mileage",
        ]

    def __str__(self):
        return f"vin={self.vin_number}, plate={self.registration_plate}, brand={self.brand}, model={self.model}, mileage={self.mileage}"
