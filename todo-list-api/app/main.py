from fastapi import FastAPI
from app.database import engine
from app.models import db
from app.routes import todo_routes, auth_routes

db.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo-List API")

app.include_router(todo_routes.router)
app.include_router(auth_routes.router)


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI is up and running successfully!"
    }

