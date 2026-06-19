from fastapi import FastAPI
import services
import api

app = FastAPI(
    title="Blogging Platform API",
    summary="Core Blog Management Service",
    description="Provides secure CRUD operations and fuzzy database searching for blog posts."
)

services.init_db()



app.include_router(api.router)


@app.get("/")
def health_check():
    return {"status": "healthy", "message": "FastAPI is up and running successfully!"}
