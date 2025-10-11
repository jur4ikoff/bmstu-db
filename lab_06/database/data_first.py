# Лабораторная работа номер 6
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy import text
from models.schemes import (
    SelectCarScheme,
    SelectRequestTripWithScore,
    SelectDriverTripStats,
    SelectMetadata,
    SelectTripsDriverPassengerInfo,
    SScoreBeforeAfterRequest,
)

from typing import Any
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

    @classmethod
    async def cte_request(cls, limit: int = 10):
        request: str = text(
            f"WITH DriverTripStats AS ( \
	        SELECT d.id, d.first_name || ' ' || d.last_name as name, \
		    d.experience, d.score, COUNT(t.id) as trip_count \
	        FROM Driver d \
	        INNER JOIN Trip t ON t.driver_id = d.id \
	        GROUP BY d.id \
	        ORDER BY trip_count DESC \
            LIMIT {limit}) \
            \
            SELECT * FROM DriverTripStats \
            WHERE experience > 20 \
            LIMIT 10"
        )

        async with async_session_maker() as session:
            result = await session.execute(request)
            response = [
                SelectDriverTripStats(**row._asdict()) for row in result.fetchall()
            ]
            return response

        return None

    @classmethod
    async def metadata(cls):
        request = text(
            """
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name IN ('car', 'driver', 'passenger', 'trip', 'payment')
            ORDER BY table_name, ordinal_position
            """
        )

        async with async_session_maker() as session:
            result = await session.execute(request)
            response = [SelectMetadata(**row._asdict()) for row in result.fetchall()]
            return response

        return None

    @classmethod
    async def driver_avg_age(cls):
        request = text(
            "CREATE OR REPLACE FUNCTION calculate_avg_driver_age() \
            RETURNS NUMERIC AS $$ \
            DECLARE \
                avg_age NUMERIC; \
            BEGIN \
                SELECT AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birthday))) \
                INTO avg_age \
                FROM Driver; \
                \
                RETURN ROUND(avg_age, 2); \
            END; \
            $$ LANGUAGE plpgsql;"
        )

        async with async_session_maker() as session:
            await session.execute(request)
            await session.commit()

        request_2 = text("SELECT calculate_avg_driver_age() AS average_driver_age;")
        async with async_session_maker() as session:
            result = await session.execute(request_2)
            await session.commit()

        return result.scalar()

    @classmethod
    async def get_trips_by_price(cls, low: int, high: int):
        function_request = text(
            f"CREATE OR REPLACE FUNCTION get_trips_by_price_range(min_price INTEGER DEFAULT 0, max_price INTEGER DEFAULT 1000) \
                                RETURNS TABLE( \
                                trip_id INTEGER, \
                        driver_name VARCHAR, \
                        passenger_name VARCHAR, \
                        source_addr VARCHAR, \
                        dest_addr VARCHAR, \
                        trip_price INTEGER \
                    ) AS $$ \
                    BEGIN \
                        RETURN QUERY \
                        SELECT \
                            t.id, (d.first_name || ' ' || d.last_name)::VARCHAR, (p.first_name || ' ' || p.last_name)::VARCHAR, t.source_address, \
                            t.destenation_address, t.price \
                        FROM Trip t \
                        JOIN Driver d ON t.driver_id = d.id \
                        JOIN Passenger p ON t.passenger_id = p.id \
                        WHERE t.price BETWEEN min_price AND max_price \
                        ORDER BY t.price DESC; \
                    END; \
                    $$ LANGUAGE plpgsql;"
        )

        async with async_session_maker() as session:
            await session.execute(function_request)
            await session.commit()

        request = text(f"SELECT * FROM get_trips_by_price_range({low}, {high});")
        async with async_session_maker() as session:
            result = await session.execute(request)
            response = [
                SelectTripsDriverPassengerInfo(**row._asdict())
                for row in result.fetchall()
            ]
            return response
        return None

    @classmethod
    async def call_procedure(
        cls, driver_id: int, score: float
    ) -> SScoreBeforeAfterRequest:
        result_dict = dict()

        create_procedure_request = text(
            "CREATE OR REPLACE PROCEDURE update_driver_score(driver_id_param INTEGER, new_score NUMERIC) \
            AS $$ \
            BEGIN \
                UPDATE Driver  \
                SET score = new_score  \
                WHERE id = driver_id_param; \
                RAISE NOTICE 'Счет водителя % обновлен до %', driver_id_param, new_score; \
            END; \
            $$ LANGUAGE plpgsql;"
        )

        score_requst = text(
            f"SELECT score FROM Driver \
                              WHERE id={driver_id}"
        )
        request = text(f"CALL update_driver_score({driver_id}, {score})")

        async with async_session_maker() as session:
            # Создаем процедуру
            await session.execute(create_procedure_request)
            await session.commit()

            # До изменений
            before = await session.execute(score_requst)
            result_dict["before"] = before.scalar_one_or_none()

            await session.execute(request)
            await session.commit()

            after = await session.execute(score_requst)
            result_dict["after"] = after.scalar_one_or_none()

        result: SScoreBeforeAfterRequest = SScoreBeforeAfterRequest(**result_dict)
        return result

    @classmethod
    async def call_system_function(cls):
        request = text("SELECT version();")

        async with async_session_maker() as session:
            result = await session.execute(request)

        return result.all()

    @classmethod
    async def cretion_table(cls):
        request = text(
            "CREATE TABLE IF NOT EXISTS Review ( \
            id SERIAL PRIMARY KEY, \
            trip_id INTEGER NOT NULL, \
            passenger_id INTEGER NOT NULL, \
            driver_id INTEGER NOT NULL, \
            rating SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 5), \
            comment TEXT, \
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
            FOREIGN KEY (trip_id) REFERENCES Trip(id) ON DELETE CASCADE, \
            FOREIGN KEY (passenger_id) REFERENCES Passenger(id) ON DELETE CASCADE, \
            FOREIGN KEY (driver_id) REFERENCES Driver(id) ON DELETE CASCADE \
);"
        )

        async with async_session_maker() as session:
            await session.execute(request)
            await session.commit()

    @classmethod
    async def insert_to_reviews(
        cls, trip_id, passenger_id, driver_id, rating, comment=None
    ):
        request = text(
            """
            INSERT INTO Review (trip_id, passenger_id, driver_id, rating, comment)
            VALUES (:trip_id, :passenger_id, :driver_id, :rating, :comment)
            """
        )

        async with async_session_maker() as session:
            await session.execute(
                request,
                {
                    "trip_id": trip_id,
                    "passenger_id": passenger_id,
                    "driver_id": driver_id,
                    "rating": rating,
                    "comment": comment,
                },
            )
            await session.commit()
