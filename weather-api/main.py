from fastapi import FastAPI
from weather_service import fetch_weather


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Weather Api test"}

@app.get("/weather/{city}")
async def get_weather(city: str, date1: str = None, date2: str = None): 
    result = fetch_weather(city, date1, date2)
    return result