from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI is up and running successfully!"
    }