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
    
    key=os.getenv("WEATHER_API_KEY")```


i set up a config file to handle the the getting of the dot.env 

the weather_service.py is all done, and now we need to hook it up the main.py so it works with the outside world

alright so next up we have to hook up the cache so after some installation and what not we now have to set it up so let's see 

we import redis and json to weather servic


