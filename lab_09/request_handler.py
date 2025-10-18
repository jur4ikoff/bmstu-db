from base_dao import BaseDAO
from driver.dao import DriverDAO
from redis_client import redis

class RequestHandler:
    def __init__(self, dao: BaseDAO | None= None):
        self.dao = dao

    async def get_top_drivers_stats():
        pass
