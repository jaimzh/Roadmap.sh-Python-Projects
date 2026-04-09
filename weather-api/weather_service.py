import requests
import os
from dotenv import load_dotenv
from config import Config
load_dotenv()
    
api_key=os.getenv("WEATHER_API_KEY")

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def fetch_weather(location: str, date1: str=None, date2: str=None):
    if date1 and date2:
        url = f"{BASE_URL}{location}/{date1}/{date2}?key={Config.API_KEY}" 
    elif date1:
        url = f"{BASE_URL}{location}/{date1}?key={Config.API_KEY}"
    else:
        url = f"{BASE_URL}{location}?key={Config.API_KEY}"
    
    try:    
        response = requests.get(url)
        response.raise_for_status() #so this throws a status error, that's if it starts from
        return response.json()
    except requests.exceptions.HTTPError as http_err: 
        print("you got an error".format(http_err)) 


if __name__ == "__main__":
    result = fetch_weather("New York")
    print(result)