# Лабораторная работа номер 6
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy import text
from models.schemes import SelectCarScheme, SelectRequestTripWithScore

from config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class DataFirstDao:
    @classmethod
    async def get_cars_above_avg_mileage(cls, limit: int = 10):
        """
        1. Выполнить скалярный запрос
        Получить список машин, с пробегом выше среднего
        """

        request: str = text(
            f"SELECT * FROM Car \
            WHERE mileage > (SELECT AVG(mileage) FROM Car) \
            ORDER BY mileage ASC\
            limit {limit}"
        )
        async with async_session_maker() as session:
            result = await session.execute(request)
            response = [SelectCarScheme(**row._asdict()) for row in result.fetchall()]
            return response

        return None

    @classmethod
    async def join_request(cls, limit: int = 10):
        """
        2. Выполнить запрос с несколькими соединениями (JOIN)
        """

        request: str = text(
            f"SELECT t.id, p.first_name as passenger_name, \
            d.first_name as driver_name, \
            t.price, t.score as trip_score, d.score as driver_score \
            FROM Trip t \
            JOIN Passenger p ON t.passenger_id = p.id  \
            JOIN Driver d ON t.driver_id = d.id \
            WHERE d.score > 4.5 \
            ORDER BY id ASC \
            LIMIT {limit}"
        )
        async with async_session_maker() as session:
            result = await session.execute(request)
            response = [
                SelectRequestTripWithScore(**row._asdict()) for row in result.fetchall()
            ]
            return response

        return None
