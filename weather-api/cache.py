import redis 
import json 
from config import Config

#commect to Redis
redis_client = redis.from_url(Config.REDIS_URL)