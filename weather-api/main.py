from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address  # for getting the ip address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from weather_service import fetch_weather
from fastapi import HTTPException
from models import WeatherResponseModel
from constants import WEATHER_API_RESPONSES

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Weather Api",
    summary="Professional Weather Service",
    description="Fetches weather data with caching and rate limiting.",
)
app.state.limiter = limiter


# tbh this is not too necessary but it's just for better docs
def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Ohhhh  Rate Limit Exceeded, wait a bit before you try",
        },
    )


app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Weather Api test"}


@app.get(
    "/weather/{city}",
    response_model= WeatherResponseModel,
    summary="Get Weather for a City",
    description="Fetches weather data. Checks cache first, then API.",
    responses=WEATHER_API_RESPONSES 
        
)
@limiter.limit("5/minute")
async def get_weather(
    request: Request, city: str, date1: str = None, date2: str = None
):
    try:
        result = fetch_weather(city, date1, date2)
        if not result:
            raise HTTPException(
                status_code=404, detail="weather not found for this city "
            )
        return {"city": city, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
