from database.database import async_session_maker
from config import Colors

from dev import print_result

from sqlalchemy import text
import json
import decimal
from datetime import date
from typing import List, Dict, Any
from py_linq import Enumerable

JSON_PATH = "data/drivers.json"
JSON_UPDATE_PATH = "data/update_drivers.json"
LIMIT = 4


class PyLinqJson:
    @classmethod
    async def __fetch_data_as_json(cls) -> List[Dict[str, Any]]:
        async with async_session_maker() as session:
            query = """
            SELECT 
                id,
                car_id,
                first_name,
                last_name,
                experience,
                score,
                date_of_birthday,
                address,
                document_number
            FROM Driver
            """
            result = await session.execute(text(query))
            rows = result.fetchall()

            columns = result.keys()
            data = []
            for row in rows:
                row_dict = {}
                for col, val in zip(columns, row):
                    if isinstance(val, date):
                        val = val.isoformat()
                    if isinstance(val, decimal.Decimal):
                        val = float(val)
                    row_dict[col] = val
                data.append(row_dict)
            return data

    @classmethod
    def __linq_read(cls, json_data: List[Dict]) -> List[Dict]:
        """Найти водителей с опытом > 5 лет и рейтингом > 4.0"""
        enumerable = Enumerable(json_data)
        result = (
            enumerable.where(lambda d: d["experience"] > 5 and d["score"] > 4.0)
            .select(
                lambda d: {
                    "name": f"{d['first_name']} {d['last_name']}",
                    "experience": d["experience"],
                    "score": d["score"],
                }
            )
            .to_list()
        )
        return result

    @classmethod
    def __linq_update(cls, json_data: List[Dict]) -> List[Dict]:
        """Увеличить рейтинг всех водителей на 0.1 (но не больше 5.0)"""
        updated = []
        for item in json_data:
            new_score = min(5.0, item["score"] + 0.1)
            updated_item = {**item, "score": new_score}
            updated.append(updated_item)
        return updated

    @classmethod
    def __linq_add(cls, json_data: List[Dict]) -> List[Dict]:
        """Добавить нового водителя в список"""
        new_driver = {
            "id": max(d["id"] for d in json_data) + 1 if json_data else 1,
            "car_id": 999,
            "first_name": "New",
            "last_name": "Driver",
            "experience": 0,
            "score": 5.0,
            "date_of_birthday": "2000-01-01",
            "address": "New Address",
            "document_number": 1234567890,
        }
        return json_data + [new_driver]

    @classmethod
    async def task_2(cls):
        print(f"{Colors.BG_GREEN}Загрузка данных из базы{Colors.RESET}")
        json_data = await PyLinqJson.__fetch_data_as_json()

        with open(JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

        print(
            f"\n{Colors.BG_GREEN}1. Чтение водителей с опытом >5 лет и рейтингом >4.0:{Colors.RESET}"
        )
        read_result = PyLinqJson.__linq_read(json_data)
        print_result(read_result)
        # res = json.dumps(read_result, indent=2, ensure_ascii=False)

        print(f"\n{Colors.BG_GREEN}2. Обновить рейтинг у всех на +0.1{Colors.RESET}")
        updated_data = PyLinqJson.__linq_update(json_data)
        print_result(updated_data)
        # print(json.dumps(updated_data[:2], indent=2, ensure_ascii=False))

        print(f"\n{Colors.BG_GREEN}3. Добавление нового водителя{Colors.RESET}")
        data_with_new = PyLinqJson.__linq_add(updated_data)
        print(
            f"Новый водитель: {data_with_new[-1]['first_name']} {data_with_new[-1]['last_name']}"
        )

        with open(JSON_UPDATE_PATH, "w", encoding="utf-8") as f:
            json.dump(data_with_new, f, indent=2, ensure_ascii=False)
        print(f"\n{Colors.BG_GREEN}Финальный JSON сохранен в {JSON_UPDATE_PATH}{Colors.RESET}")
