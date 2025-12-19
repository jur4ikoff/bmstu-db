from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy import text, func
from sqlalchemy import String, Date, Integer, ForeignKey, Time
from sqlalchemy import select, extract, func, case
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
    declared_attr,
)

import asyncio
from datetime import date


class Settings:
    DB_HOST: str = "localhost"
    DB_PORT: str = "5430"
    DB_NAME: str = "postgres_db"
    DB_USER: str = "postgres_user"
    DB_PASSWORD: str = "postgres_password"


settings = Settings()


def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"


class Driver(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)

    routes: Mapped[list["Route"]] = relationship("Route", back_populates="driver")


class Route(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    driver_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("driver.id"), nullable=False
    )
    trip_date: Mapped[Date] = mapped_column(
        Date, nullable=True
    )  # В таблице указано как NULLABLE
    trip_time: Mapped[Time] = mapped_column(
        Time, nullable=True
    )  # В таблице указано как NULLABLE
    day_of_week: Mapped[str] = mapped_column(String(20), nullable=True)
    event_type: Mapped[int] = mapped_column(Integer, nullable=True)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="routes")


async def func_1_sql(session):
    query = """SELECT region
            FROM driver
            GROUP BY region
            HAVING COUNT(*) = COUNT(CASE WHEN EXTRACT(MONTH FROM birth_date) = 6 THEN 1 END);"""

    result = await session.execute(text(query))
    return result.all()


async def func_1_orm(session):
    stmt = (
        select(Driver.region)
        .group_by(Driver.region)
        .having(
            func.count()
            == func.count(case((func.extract("month", Driver.birth_date) == 6, 1)))
        )
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def func_2_sql(sesson):
    query = """SELECT r.driver_id, d.full_name
                FROM route r
                JOIN driver d ON r.driver_id = d.id
                WHERE (r.trip_date, r.trip_time) = (
                SELECT MAX(trip_date), MAX(trip_time)
                FROM route
                WHERE trip_date = (
                    SELECT MAX(trip_date)
                    FROM route
                ));"""

    result = await sesson.execute(text(query))
    return result.all()


async def func_2_orm(session):
    max_date_query = select(func.max(Route.trip_date)).scalar_subquery()
    max_datetime_query = (
        select(
            func.max(Route.trip_date).label("max_date"),
            func.max(Route.trip_time).label("max_time"),
        )
        .where(Route.trip_date == max_date_query)
        .subquery()
    )

    stmt = (
        select(Route.driver_id, Driver.full_name)
        .join(Driver, Route.driver_id == Driver.id)
        .join(
            max_datetime_query,
            (Route.trip_date == max_datetime_query.c.max_date)
            & (Route.trip_time == max_datetime_query.c.max_time),
        )
    )

    result = await session.execute(stmt)
    return result.all()


async def func_3_sql(sesson):
    query = """WITH last_routes_2025 AS (
    SELECT 
        driver_id,
        MAX(trip_date) AS last_trip_date
    FROM route
    WHERE EXTRACT(YEAR FROM trip_date) = 2025
    GROUP BY driver_id
    )
    SELECT d.id, d.full_name, d.region,  lr.last_trip_date
    FROM driver d
    JOIN last_routes_2025 lr ON d.id = lr.driver_id
    WHERE d.region = 'Moscow'
    AND lr.last_trip_date <= '2025-10-17';"""

    result = await sesson.execute(text(query))
    return result.all()


async def func_3_orm(session):
    subq = (
        select(Route.driver_id, func.max(Route.trip_date).label("last_trip_date"))
        .where(extract("year", Route.trip_date) == 2025)
        .group_by(Route.driver_id)
        .subquery()
    )

    stmt = (
        select(Driver.id, Driver.full_name, subq.c.last_trip_date)
        .join(subq, Driver.id == subq.c.driver_id)
        .where(Driver.region == "Moscow")
        .where(subq.c.last_trip_date <= date(2025, 10, 17))
    )

    result = await session.execute(stmt)
    return result.all()


async def main():
    async with async_session_maker() as session:
        # print(await func_1_sql(session))
        # print(await func_1_orm(session))

        # print(await func_2_sql(session))
        print(await func_2_orm(session))

        # print(await func_3_sql(session))
        # print(await func_3_orm(session))


if __name__ == "__main__":
    asyncio.run(main())
