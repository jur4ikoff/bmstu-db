from database.database import async_session_maker

from models.driver.schemes import SDriverScheme
from models.trip.schemes import STripScheme

from models.driver.models import *
from models.trip.models import Trip

from dev import print_result

from config import Colors

from sqlalchemy import select

class BaseDao:
    model = None

class TripDao(BaseDao):
    @classmethod
    async def first_query(cls):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(cls.model.driver_id > 970)
            result = await session.execute(stmt)
            trips_orm = result.scalars().all()
            
            trips_pydantic = [STripScheme.model_validate(trip) for trip in trips_orm]
            return trips_pydantic


async def task_3():
    print(f"{Colors.BG_GREEN}Однотабличный запрос{Colors.RESET}")
    TripDao.model = Trip

    result = await TripDao.first_query()
    print_result(result)
