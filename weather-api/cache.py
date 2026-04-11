import redis 
import json 
from typing import Any, Optional
from config import Config

#commect to Redis
redis_client = redis.from_url(Config.REDIS_URL, decode_responses=True)


#setter for cache data key, val and expiration
def set_cache_data(key:str, expiration:int, val:Any, )-> bool: 
    try: 
        redis_client.setex(name=key, time=expiration, value=json.dumps(val))
        print("Saved data to cache")
        return True
    except redis.RedisError as e: 
        print("We got a redis error", e)
        return False 
        
#getter
def get_cached_data(key:str)->Optional[Any]: 
    try: 
        data = redis_client.get(key)
        if data: 
            print("Ayyy we got some data in cache, that's a hit baby")
            return json.loads(data)
        else: 
            print("we got a cache miss")
            return
        
    except redis.RedisError as e:
        print("We got a redis error", e)
        return None 
        
        

    