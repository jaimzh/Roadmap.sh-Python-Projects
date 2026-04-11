import requests
from config import Config
from cache import set_cache_data, get_cached_data
import json

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def fetch_weather(city: str, date1: str=None, date2: str=None):
    if date1 and date2:
        url = f"{BASE_URL}{city}/{date1}/{date2}?key={Config.API_KEY}" 
    elif date1:
        url = f"{BASE_URL}{city}/{date1}?key={Config.API_KEY}"
    else:
        url = f"{BASE_URL}{city}?key={Config.API_KEY}"
    
    #cache steps , check, call api, save cache
    #1. first check if data exists in cache
    cached_data = get_cached_data(url)
    if cached_data: 
        return cached_data
    #2. fetch data from api 
    try:    
        response = requests.get(url)
        response.raise_for_status() #so this throws a status error, that's if it starts from
        data = response.json()
    #save data to cache   
        set_cache_data(url, Config.CACHE_EXPIRATION, data)
        return data
    
    except requests.exceptions.HTTPError as http_err: 
        print("you got an error", http_err) 


if __name__ == "__main__":
    result = fetch_weather("New York")
    print(result)