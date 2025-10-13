from database.database import async_session_maker

from models.driver.schemes import SDriverScheme
from models.trip.schemes import STripScheme, STripFullScheme, CrTrip, UpdTrip

from models.models import Trip, Driver, Passenger

from config import Colors
from dev import print_result

from sqlalchemy import select, update, delete, func, text

# Если БД не хочет принимать инсерт
# SELECT setval('trip_id_seq', (SELECT MAX(id) FROM trip));


class BaseDao:
    model = None


class TripDao(BaseDao):
    @classmethod
    async def get_trip_info_with_price_more_4000(cls) -> list[STripScheme]:
        """Получить поездки с ценой > 4000"""
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(cls.model.price > 4000)
                .order_by(cls.model.price)
            )
            result = await session.execute(query)
            trips_orm = result.scalars().all()

            trips_pydantic = [STripScheme.model_validate(trip) for trip in trips_orm]
            return trips_pydantic

    @classmethod
    async def get_full_trip_info(cls) -> list[STripFullScheme]:
        stmt = (
            select(
                Trip.id,
                Trip.driver_id,
                Driver.first_name.label("driver_first_name"),
                Driver.last_name.label("driver_second_name"),
                Driver.score.label("driver_score"),
                Trip.passenger_id,
                Passenger.first_name.label("passenger_first_name"),
                Passenger.last_name.label("passenger_second_name"),
                Trip.source_address.label("src_address"),
                Trip.destenation_address.label("dest_address"),
                Trip.price,
                Trip.score,
            )
            .select_from(Trip)
            .join(Driver, Trip.driver_id == Driver.id)
            .join(Passenger, Trip.passenger_id == Passenger.id)
        )
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            rows = result.fetchall()

            trips = []
            for row in rows:
                trip = STripFullScheme(
                    id=row.id,
                    driver_id=row.driver_id,
                    driver_name=f"{row.driver_first_name} {row.driver_second_name}",
                    driver_score=row.driver_score,
                    passenger_id=row.passenger_id,
                    passenger_name=f"{row.passenger_first_name} {row.passenger_second_name}",
                    src_address=row.src_address,
                    dest_address=row.dest_address,
                    price=row.price,
                    score=row.score,
                )
                trips.append(trip)

            return trips

    @classmethod
    async def insert_model(cls, data: CrTrip):
        trip = Trip(**data.model_dump())
        async with async_session_maker() as session:
            session.add(trip)
            await session.commit()
            await session.refresh(trip)  # чтобы получить id и другие поля из БД
            return trip

    @classmethod
    async def update_model(cls, key: int, data):
        query = (
            update(Trip)
            .where(Trip.id == key)
            .values(**data.model_dump(exclude_unset=True))
            .returning(Trip)
        )

        async with async_session_maker() as session:
            result = await session.execute(query)
            updated_trip = result.scalar_one_or_none()
            await session.commit()
            return updated_trip

    @classmethod
    async def delete_model(cls, key: int):
        query = (delete(Trip).where(Trip.id == key)).returning(Trip)
        async with async_session_maker() as session:
            result = await session.execute(query)
            trip = result.scalar_one_or_none()
            await session.commit()
            return trip

    @classmethod
    async def call_procedure(cls, key: int, new_score):
        async with async_session_maker() as session:
            await session.execute(
                text("CALL update_driver_score(:driver_id, :new_score)"),
                {"driver_id": key, "new_score": new_score},
            )
            await session.commit()


# result = await session.execute(stmt)


async def task_3():
    TripDao.model = Trip

    print(f"\n{Colors.BG_GREEN}1. Однотабличный запрос{Colors.RESET}")
    result = await TripDao.get_trip_info_with_price_more_4000()
    print_result(result)

    print(f"\n{Colors.BG_GREEN}2. Многотабличный запрос на выборку{Colors.RESET}")
    result = await TripDao.get_full_trip_info()
    print_result(result, limit=3)

    print(f"\n{Colors.BG_GREEN}3. CRUD запросы{Colors.RESET}")
    insert_data = CrTrip(
        driver_id=1,
        passenger_id=1,
        payment_id=1,
        source_address="test",
        destenation_address="test",
        price=3200,
        score=5,
    )
    print("ВСТАВКА")
    result = await TripDao.insert_model(insert_data)

    print("ОБНОВЛЕНИЕ")
    result = await TripDao.update_model(1, insert_data)

    print("УДАЛЕНИЕ")
    result = await TripDao.delete_model(900)
    print(result)

    print(f"\n{Colors.BG_GREEN}4. Вызов процедуры{Colors.RESET}")
    result = await TripDao.call_procedure(1, 3)
    
