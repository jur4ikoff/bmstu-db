"""
LINQ to Object. Создать не менее пять запросов с использованием всех
ключевых слов выражения запроса. Object - коллекция объектов, структура
которых полностью соответствует одной из таблиц БД, реализованной в
первой лабораторной работе
"""
from models.drivers import SDriverScheme
from py_linq import Enumerable
import pandas as pd

DRIVER_DATA_PATH = "data/drivers.csv"
columns = ["id", "car_id", "first_name", "last_name", "experience", "score", "date_of_birthday", "address", "document_number"]

class PyLinqClass:
    @classmethod
    async def read_csv(cls):
        df = pd.read_csv(DRIVER_DATA_PATH, delimiter=";", header=None, names=columns)
        drivers = [SDriverScheme(**row) for row in df.to_dict(orient="records")]
        return drivers