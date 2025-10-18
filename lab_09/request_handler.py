from base_dao import BaseDAO
from driver.dao import DriverDAO
from redis_client import redis_client


import json
from typing import List, Dict, Any


class RequestHandler:
    def __init__(self, dao: BaseDAO | None = None):
        self.dao = dao

    @classmethod
    async def redis_get_top_drivers_stats(
        cls, cache_key: str = "driver_stats_v1", cache_ttl=4
    ) -> List[Dict[str, Any]]:
        """
        Возвращает статистику: из Redis, если есть; иначе из БД + сохраняет в Redis.
        """

        # Получаем из кэша
        cached_data = await redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        print("При запросе к redis, запрашиваются данные из БД")
        result = await DriverDAO.get_top_drivers_stats(5)

        await redis_client.setex(cache_key, cache_ttl, json.dumps(result))
        return result

    @classmethod
    async def default_get_top_drivers_stats(cls) -> List[Dict[str, Any]]:
        """
        Возвращает статистику: из Redis, если есть; иначе из БД + сохраняет в Redis.
        """
        return await DriverDAO.get_top_drivers_stats(5)
