# Weather API

Python sample solution for the Weather API challenge from roadmap.sh.

This project is a FastAPI-based Weather API that fetches weather data from the Visual Crossing Weather API based on a city name and optional date range. The API supports caching using Redis to minimize API requests and improve performance. It also includes rate limiting and comprehensive logging to ensure reliability and prevent abuse.

## Features

- **Fetch Weather Data:** Retrieve weather data by location (city name) with an optional date range.
- **Caching:** Uses Redis to cache weather data for 12 hours, reducing external API calls and improving response times.
- **Rate Limiting:** Limits API requests to 5 per minute per client to prevent abuse.
- **Logging:** Tracks API requests, cache hits/misses, and errors in both the console and a persistent log file.
- **Error Handling:** Handles cases such as invalid locations, third-party API failures, and internal server errors.

## Technologies Used

- **FastAPI:** Modern Python web framework for building APIs.
- **Requests:** Python library for making HTTP requests to the third-party weather API.
- **Redis:** In-memory data structure store used for caching.
- **SlowAPI:** Library used for rate limiting API requests.
- **Visual Crossing Weather API:** External API used to fetch weather data.
- **Python-dotenv:** Library used for managing environment variables.

## API Usage

### Base URL

The API is hosted locally at: `http://localhost:8000`

### Example Request

```bash
curl "http://localhost:8000/weather/New York?date1=2024-10-10"
```

### Path Parameters

- `city` (required): The city name for which to retrieve weather data.

### Query Parameters

- `date1` (optional): The start date for which to retrieve weather data in `yyyy-MM-dd` format.
- `date2` (optional): The end date for which to retrieve weather data in `yyyy-MM-dd` format.

### Response

The API returns weather data in JSON format.

```json
{
  "city": "New York",
  "data": {
    "address": "New York",
    "resolvedAddress": "New York, NY, United States",
    "latitude": 40.7128,
    "longitude": -74.006,
    "timezone": "America/New_York",
    "days": [
      {
        "datetime": "2024-10-10",
        "temp": 15.0,
        "conditions": "Clear",
        "description": "Clear conditions throughout the day."
      }
    ]
  }
}
```

## Installation

### Prerequisites

- Python 3.10+
- Redis: Ensure that Redis is installed and running locally or via Docker.
- Visual Crossing Weather API Key: Sign up and obtain an API key from Visual Crossing.

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/weather-api.git
   cd weather-api
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables:** Create a `.env` file and add your credentials:

   ```
   WEATHER_API_KEY=your_visual_crossing_api_key
   REDIS_URL=redis://localhost:6379
   ```

5. **Run Redis:** Make sure Redis is running locally. If using Docker:

   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

6. **Run the App:**

   ```bash
   uvicorn main:app --reload
   ```

7. **Test the API:** Use curl or visit the auto-generated documentation at `http://localhost:8000/docs`.

## Rate Limiting

The API limits requests to 5 requests per minute per client. If this limit is exceeded, the API will return a `429 Too Many Requests` response.

## Caching

Redis is used to cache weather data for 12 hours. If a request is made for the same location and date range within this timeframe, the cached data will be returned instead of making a new API call to the external service.

## Logging

The application logs all requests, cache hits/misses, and errors. Logs are displayed in the terminal and saved to a `weather_app.log` file for persistent tracking.

## Error Handling

The API includes error handling for the following scenarios:

- **Invalid Location:** Returns a 404 error if the location cannot be found.
- **Service Unavailable:** Returns a 500 error if the third-party API is down or unreachable.
- **Rate Limit Exceeded:** Returns a 429 error if the client sends too many requests.
