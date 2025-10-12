"""
LINQ to Object. Создать не менее пять запросов с использованием всех
ключевых слов выражения запроса. Object - коллекция объектов, структура
которых полностью соответствует одной из таблиц БД, реализованной в
первой лабораторной работе
"""

from models.drivers import SDriverScheme
from models.trip import STripScheme

from datetime import date

from collections import defaultdict
from config import Colors

from py_linq import Enumerable
import pandas as pd

LIMIT = 5

DRIVER_DATA_PATH = "data/drivers.csv"
TRIP_DATA_PATH = "data/trips.csv"

driver_columns = [
    "id",
    "car_id",
    "first_name",
    "last_name",
    "experience",
    "score",
    "date_of_birthday",
    "address",
    "document_number",
]
trip_columns = [
    "id",
    "driver_id",
    "passenger_id",
    "payment_id",
    "source_address",
    "destenation_address",
    "price",
    "score",
]


class PyLinqClass:
    @classmethod
    def read_csv(cls, path_to_csv, scheme, header, column_names):
        df = pd.read_csv(path_to_csv, delimiter=";", header=header, names=column_names)
        drivers = [scheme(**row) for row in df.to_dict(orient="records")]
        return drivers

    @classmethod
    def print_result(cls, result):
        for i in range(min(len(result), LIMIT)):
            print(result[i])

    @classmethod
    async def query_1_where_select(cls, drivers):
        """Найти водителей со стажем > 10 лет и вывести их ФИО и стаж"""
        result = (
            drivers.where(lambda d: d.experience > 10)
            .select(lambda d: f"{d.first_name} {d.last_name} ({d.experience} лет)")
            .to_list()
        )
        return result

    @classmethod
    async def query_2_order_by_take_skip(cls, drivers):
        """Получить 2 водителя с наивысшим рейтингом, пропустив первого (топ-2–3)"""
        result = (
            drivers.order_by(lambda x: -x.score)  # сортировка по убыванию
            .skip(1)
            .take(2)
            .select(lambda x: {"id": x.id, "score": x.score})
            .to_list()
        )
        return result

    @classmethod
    async def query_3_group_by(cls, trips):
        """Сгруппировать поездки по driver_id и посчитать количество поездок на водителя"""
        groups = defaultdict(list)
        for trip in trips:
            groups[trip.driver_id].append(trip)

        result = [
            {"driver_id": driver_id, "trip_count": len(trips_list)}
            for driver_id, trips_list in groups.items()
        ]
        return result

    @classmethod
    async def query_4_any_all(cls, drivers) -> bool:
        """Комбинированая проверка: есть ли водители младше 25? Все ли водители имеют рейтинг > 3.0?"""
        any_young = drivers.any(
            lambda d: (date.today().year - d.date_of_birthday.year) < 25
        )
        all_high_score = drivers.all(lambda d: d.score > 3.0)
        return {"any_young": any_young, "all_high_score": all_high_score}

    @classmethod
    async def query_5_youngest_drivers(cls, drivers):
        """Получить 3 самых молодых водителя (по дате рождения)"""
        current_year = date.today().year

        result = (
            drivers
            .select(lambda d: {
                "id": d.id,
                "first_name": d.first_name,
                "last_name": d.last_name,
                "age": current_year - d.date_of_birthday.year,
                "date_of_birthday": d.date_of_birthday
            })
            .order_by(lambda x: x["age"])
            .take(3)
            .to_list()
        )

        return result


    @classmethod
    async def task_1(cls):
        drivers = Enumerable(
            PyLinqClass.read_csv(DRIVER_DATA_PATH, SDriverScheme, None, driver_columns)
        )
        trips = Enumerable(
            PyLinqClass.read_csv(TRIP_DATA_PATH, STripScheme, None, trip_columns)
        )

        print(
            f"\n{Colors.BG_GREEN}2. Получить 2 водителя с наивысшим рейтингом, пропустив первого{Colors.RESET}"
        )
        result = await PyLinqClass.query_1_where_select(drivers)
        PyLinqClass.print_result(result)

        print(f"\n{Colors.BG_GREEN}2. Вывод топ 2 и 3 водителей{Colors.RESET}")
        result = await PyLinqClass.query_2_order_by_take_skip(drivers)
        PyLinqClass.print_result(result)

        print(f"\n{Colors.BG_GREEN}3. Количество поездок на водителя{Colors.RESET}")
        result = await PyLinqClass.query_3_group_by(trips)
        PyLinqClass.print_result(result)

        print(
            f"\n{Colors.BG_GREEN}4. Комбинированная проверка, Есть ли водители < 25 и Все ли с рейтингом > 3{Colors.RESET}"
        )
        result = await PyLinqClass.query_4_any_all(drivers)
        print(result)

        print(
            f"\n{Colors.BG_GREEN}5. Получить 3 самых молодых водителя{Colors.RESET}"
        )
        result = await PyLinqClass.query_5_youngest_drivers(drivers)
        PyLinqClass.print_result(result)
