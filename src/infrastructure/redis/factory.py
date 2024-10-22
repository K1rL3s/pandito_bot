from redis.asyncio import ConnectionPool, Redis

from infrastructure.redis.config import RedisConfig


def create_redis(redis_settings: RedisConfig) -> Redis:
    return Redis(connection_pool=ConnectionPool.from_url(redis_settings.url),)
