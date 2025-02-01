from typing import AsyncGenerator

from redis.asyncio import ConnectionPool, Redis


pool = ConnectionPool.from_url(
    "redis://@redis",
    decode_responses=True,
    max_connections=10
)


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    async with Redis.from_pool(pool) as client:
        yield client
