So first of all i have to install all the dependencies first: 
- fastapi
- uvicorn 
- requests
- redis
- python-dotenv : so apparently that is for dotenv's in python,  okayyyy 

for now we are installing all this 
```pip install fastapi uvicorn requests redis python-dotenv```


alright then we setup like a basic skeleton in main.py which is just root endpoint to test if my api is working 

Once that is done the next thing we do is now go the weather_service.py and make the function 

so note when it comes to handling dot env 
``` import os
    from dotenv import load_dotenv
    load_dotenv()
    
    key=os.getenv("WEATHER_API_KEY")
```


i set up a config file to handle the the getting of the dot.env 

the weather_service.py is all done, and now we need to hook it up the main.py so it works with the outside world

alright so next up we have to hook up the cache so after some installation and what not we now have to set it up so let's see 

we import redis and json to weather service

so set up redis using docker using well that process was documented on code canvas

but in the code make sure you add the port for redis in your .env as something like REDIS_URL=redis://localhost:(portno)
 
 so we hook that up to out config and then set up cache expiration in out config as well which is literally just the expiration date in seconds so it's just a number to be honest but yeah 


So cache is all done now we do some rate limiting, and when it commes to fast api we do rate limiting in fastapi using slowapi 

`pip install slowapi`

so we set it up in our `main.py`
we import 
```
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address #for getting the ip address
from slowapi.errors import RateLimitExceeded
```

initialize and that's more or less it, tbh the docs offer a simple copy and paste [guide](https://slowapi.readthedocs.io/en/latest/)

now we do better error handling using http exceptions

```from fastapi import HTTPException```
and well hook it up in try except blocks

for better documentation we add details and responsed to endpoints as arguments

now main.py was starting to look a little cluttered  we have to make a models.py...yay my fav part 

now time to add logging

