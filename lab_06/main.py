from models.gen_models import (
    GenDriver,
    GenTrip,
    GenCar,
    GenPassenger,
    GenPayment,
)

from models.schemes import (
    SelectCarScheme,
    SelectRequestTripWithScore,
    SelectDriverTripStats,
    SelectMetadata,
    SelectTripsDriverPassengerInfo,
    SScoreBeforeAfterRequest,
)

from database.database import DataBase
from database.data_first import DataFirstDao
from generator import generate_csv
from config import Colors

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

MAX_OPERATIONS = 10


database = DataBase()


def print_menu():
    print(
        "0. Выход\n \
        1. Выполнить скалярный запрос\n \
        2. Выполнить запрос с несколькими соединениями (JOIN)\n \
        3. Выполнить запрос с ОТВ(CTE) и оконными функциями\n \
        4. Выполнить запрос к метаданным\n \
        5. Вызвать скалярную функцию (написанную в третьей лабораторной работе) \n \
        6. Вызвать многооператорную или табличную функцию (написанную в третьей \n \
        7. Вызвать хранимую процедуру (написанную в третьей лабораторной работе) \n \
        8. Вызвать системную функцию или процедуру; \n \
        9. Создать таблицу в базе данных, соответствующую тематике БД \n \
        10. Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY\n"
    )


def input_operation():
    operation = 0
    while True:
        try:
            operation = int(input("Введите номер операции: "))
            if operation > MAX_OPERATIONS or operation < 0:
                print(f"ОПЕРАЦИЯ ДОЛЖНА ВХОДИТЬ В ДИАПАЗОН ОТ 0 ДО {MAX_OPERATIONS}")
            else:
                return operation
        except Exception:
            print(f"ОПЕРАЦИЯ ВВЕДЕНА НЕПРАВИЛЬНО")


async def generate():
    print("dropping database")
    try:
        await database.drop_table()
    except Exception as e:
        print("database doesn`t exist")

    print("create tables")
    await database.create_tables()

    generate_csv(GenCar, CARS_FILE)
    generate_csv(GenDriver, DRIVERS_FILE)
    generate_csv(GenPassenger, PASSENGERS_FILE)
    generate_csv(GenPayment, PAYMENTS_FILE)
    generate_csv(GenTrip, TRIPS_FILE)

    print("copying")
    await database.copy_tables()


def print_result(result: list):
    for el in result:
        print(el)


async def task_1():
    limit = 10
    print(
        f"{Colors.GREEN}Машины с пробегом больше среднего, лимит {limit}{Colors.RESET}"
    )
    result: list[SelectCarScheme] = await DataFirstDao.get_cars_above_avg_mileage(
        limit=limit
    )
    print_result(result)


async def task_2():
    limit = 10
    print(
        f"{Colors.GREEN}Вывод поездок, где оценка водителя больше 4.5, лимит {limit}{Colors.RESET}"
    )
    result: list[SelectRequestTripWithScore] = await DataFirstDao.join_request(
        limit=limit
    )
    print_result(result)


async def task_3():
    limit = 10
    print(
        f"{Colors.GREEN}Сортировка водителей по количеству поездок{limit}{Colors.RESET}"
    )

    result: list[SelectDriverTripStats] = await DataFirstDao.cte_request(limit=limit)
    print_result(result)


async def task_4():
    print(f"{Colors.GREEN}Запрос к метаданным{Colors.RESET}")

    result: list[SelectMetadata] = await DataFirstDao.metadata()
    print_result(result)


async def task_5():
    print(f"{Colors.GREEN}Вызов функции, которая считает средний возраст{Colors.RESET}")
    result = await DataFirstDao.driver_avg_age()
    print(f"Средний возраст водителей: {result}")


async def task_6():
    low = 4200
    high = 4500
    print(f"{Colors.GREEN}Вывод поездок ценой от {low} до {high}{Colors.RESET}")
    result: list[SelectTripsDriverPassengerInfo] = (
        await DataFirstDao.get_trips_by_price(low, high)
    )
    print_result(result)


async def task_7():
    driver_id = 4
    new_score = 2
    print(
        f"{Colors.GREEN}Обновление рейтингра Driver(id={driver_id}) Score={new_score}{Colors.RESET}"
    )
    result: SScoreBeforeAfterRequest = await DataFirstDao.call_procedure(
        driver_id, new_score
    )
    print(result)


async def task_8():
    print(f"{Colors.GREEN}Вызов системной функции, информация о версии{Colors.RESET}")
    result = await DataFirstDao.call_system_function()
    print(result)


async def task_9():
    print(f"{Colors.GREEN}Создание таблицы в базе данных{Colors.RESET}")
    await DataFirstDao.cretion_table()
    print(f"{Colors.GREEN}Таблица успешно создана{Colors.RESET}")


async def task_10():
    driver_id = 4
    trip_id = 4
    passenger_id = 4
    score = 2
    comment = "test"
    print(
        f"{Colors.GREEN}Вставка оценки в таблицу Review(driver_id={driver_id}), trip_id={trip_id}, passenger_id={passenger_id}, score={score}, comment={comment}{Colors.RESET}"
    )
    await DataFirstDao.insert_to_reviews(
        trip_id, passenger_id, driver_id, score, comment
    )


async def main():
    # Генерация базы данных
    # await generate()
    print_menu()
    operation = input_operation()

    match operation:
        case 1:
            await task_1()
        case 2:
            await task_2()
        case 3:
            await task_3()
        case 4:
            await task_4()
        case 5:
            await task_5()
        case 6:
            await task_6()
        case 7:
            await task_7()
        case 8:
            await task_8()
        case 9:
            await task_9()
        case 10:
            await task_10()


if __name__ == "__main__":
    asyncio.run(main())
