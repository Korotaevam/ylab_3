from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

redis = aioredis.from_url('redis://localhost', encoding='utf8', decode_responses=True)
FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
redis.flushdb()  # type: ignore
