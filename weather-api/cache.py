import redis
import json
from typing import Any, Optional
from config import Config

import logging

logger = logging.getLogger(__name__)
# commect to Redis
redis_client = redis.from_url(Config.REDIS_URL, decode_responses=True)


# setter for cache data key, val and expiration
def set_cache_data(
    key: str,
    expiration: int,
    val: Any,
) -> bool:
    try:
        redis_client.setex(name=key, time=expiration, value=json.dumps(val))
        logger.info(f"Cache Saved: key-{key}, value-{val}" )  # print("Saved data to cache")

        return True
    except redis.RedisError as e:
        logger.error( f"Error accessing cache: {str(e)}")  # print("We got a redis error", e)
        return False


# getter
def get_cached_data(key: str) -> Optional[Any]:
    try:
        data = redis_client.get(key)
        if data:
            logger.info( f"Cache hit for key: {key}")  # print("Ayyy we got some data in cache, that's a hit baby")
            return json.loads(data)
        else:
            logger.info(f"Cache miss for key: {key}")  # print("we got a cache miss")
            return

    except redis.RedisError as e:
        logger.error(f"Error accessing cache: {str(e)}")  # print("We got a redis error", e)
        return None
