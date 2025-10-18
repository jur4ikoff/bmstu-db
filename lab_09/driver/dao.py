from base_dao import BaseDAO
from driver.models import Driver
from trip.models import Trip

from database import async_session_maker

from sqlalchemy import select, func, desc


class DriverDAO(BaseDAO):
    model = Driver

    @classmethod
    async def get_top_drivers_stats(cls, limit: int = 5):
        async with async_session_maker() as session:
            query = (
                select(
                    Driver.id,
                    Driver.first_name,
                    Driver.last_name,
                    func.avg(Trip.score).label("avg_score"),
                    func.count(Trip.id).label("trip_count"),
                )
                .join(Trip, Trip.driver_id == Driver.id)
                .group_by(Driver.id, Driver.first_name, Driver.last_name)
                .having(func.count(Trip.id) >= 1)
                .order_by(desc(func.avg(Trip.score)), desc(func.count(Trip.id)))
                .limit(limit)
            )
            result = await session.execute(query)
            rows = result.fetchall()

            return [
                {
                    "driver_id": row.id,
                    "first_name": row.first_name,
                    "last_name": row.last_name,
                    "avg_score": float(row.avg_score),
                    "trip_count": row.trip_count,
                }
                for row in rows
            ]
