from fastapi import FastAPI
from app.database import engine
from app.models import db

db.Base.metadat.create_all(bind=engine)

app = FastAPI()



@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI is up and running successfully!"
    }

