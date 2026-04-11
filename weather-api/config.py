import os
from dotenv import load_dotenv
load_dotenv()


class Config: 
    API_KEY= os.getenv("WEATHER_API_KEY")
    REDIS_URL= os.getenv("REDIS_URL")
    CACHE_EXPIRATION = 43200 #expires in 12 hours....wait 12 hours?!!
    