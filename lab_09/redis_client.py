import json
from typing import List, Dict, Any
from redis.asyncio import Redis


# Глобальный клиент Redis (лучше инициализировать один раз в приложении)
redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)

