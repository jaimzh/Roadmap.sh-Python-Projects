WEATHER_API_RESPONSES  = {
    200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "city": "New York",
                        "data": {"temp": 25, "conditions": "Clear"},
                    }
                }
            },
        },
        404: {
            "description": "City Not Found",
            "content": {
                "application/json": {
                    "example": {"detail": "Weather not found for this city"}
                }
            },
        },
        429: {
            "description": "Rate Limit Exceeded",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Ohhhh Rate Limit Exceeded, wait a bit before you try"
                    }
                }
            },
        },
    }
