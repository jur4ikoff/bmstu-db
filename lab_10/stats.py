from database import async_session_maker
from redis_client import redis_client
from driver.models import Driver
from trip.models import Trip
from driver.dao import DriverDAO
from request_handler import RequestHandler

import json
import time
from typing import List, Dict, Any

CACHE_TTL = 4

request_handler = RequestHandler()


async def get_stats_from_db() -> List[Dict[str, Any]]:
    start = time.perf_counter()
    data = await request_handler.default_get_top_drivers_stats()
    duration = time.perf_counter() - start
    return data, duration


async def get_stats_from_redis() -> List[Dict[str, Any]]:
    start = time.perf_counter()
    data = await request_handler.redis_get_top_drivers_stats()
    duration = time.perf_counter() - start
    return data, duration


async def update_cache(cache_key: str = "driver_stats_v1"):
    start = time.perf_counter()
    data, _ = await get_stats_from_db()
    await redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
    duration = time.perf_counter() - start
    return duration
