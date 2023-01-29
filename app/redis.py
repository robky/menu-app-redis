import redis
from app.config import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_SERVER,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


def get_redis():
    return redis.Redis(connection_pool=pool)
