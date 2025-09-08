# В будущем можно сделать нормально, но пока пусть будет базовая модель, которая будет храниться в базе  
from datetime import date


class Driver:
    driver_id: int
    car_id: int
    first_name: str
    last_name: str 
    patronymic: str
    experience: str
    score: str
    date_of_birthday: date
    adress: str
    document_number: str

    def __str__(self):
        return f"id={self.driver_id}, name={self.first_name + " " + self.last_name + " " +self.patronymic}, expirience={self.experience}, date_of_birthday={self.date_of_birthday}"


class Trip:
    trip_id: int
    driver_id: int
    passenger_id: int
    payment_id: int
    source_adress: str
    destenation_adress: str
    price: int
    score: int

class Passanger:
    passanger_id: int
    first_name: str
    last_name: str
    patronymic: str
    date_of_birthday: date
    adress: str

class Payment:
    payment_id: int
    invoice: int
    status: str


class Car:
    vin_number: int
    registration_plate: str
    brand: str
    model: str
    mileage: int



driver = Driver()
driver.id = 0
driver.first_name = "test"
driver.last_name = "test"
driver.patronymic = "test"
driver.experience = 2
driver.date_of_birthday = "2025-09-08"

print(driver)