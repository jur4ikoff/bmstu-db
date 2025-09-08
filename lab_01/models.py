# В будущем можно сделать нормально, но пока пусть будет базовая модель, которая будет храниться в базе
from datetime import date


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


class Trip:
    trip_id: int
    driver_id: int
    passenger_id: int
    payment_id: int
    source_adress: str
    destenation_adress: str
    price: int
    score: int

    def __str__(self):
        return (
            f"id={self.trip_id}, driver_id={self.driver_id}, passenger_id={self.passenger_id}, "
            f"payment_id={self.payment_id}, src_adress={self.source_adress}, "
            f"dest_adress={self.source_adress}, price={self.price}, score={self.score}"
        )


class Passanger:
    passanger_id: int
    first_name: str
    last_name: str
    date_of_birthday: date
    adress: str

    def __str__(self):
        return (
            f"id={self.passanger_id}, first_name={self.first_name}, last_name={self.last_name}, "
            f"date_of_birthday={self.date_of_birthday}, adress={self.adress}, "
        )


class Payment:
    payment_id: int
    invoice: int
    status: bool

    def __str__(self):
        return f"id={self.payment_id}, invoice={self.invoice}, status={self.status}"


class Car:
    vin_number: int
    registration_plate: str
    brand: str
    model: str
    mileage: int

    def __str__(self):
        return f"vin={self.vin_number}, plate={self.registration_plate}, brand={self.brand}, model={self.model}, mileage={self.mileage}"
