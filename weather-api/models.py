from pydantic import BaseModel
from typing import Any, Optional 


class WeatherResponseModel(BaseModel):
    city: str
    data: Any
    message: Optional[str] = None 
    