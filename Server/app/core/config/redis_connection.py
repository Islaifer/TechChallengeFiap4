from app.core.config import settings
import redis.asyncio as redis

redis_connection = None
def get_redis_connection():
    global redis_connection
    if settings.USE_REDIS and redis_connection is None:
        redis_connection = redis.from_url(settings.REDIS_URL, decode_responses=True)

    return redis_connection