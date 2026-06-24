from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database will live in a single file named 'todo.db' in root folder, physical address of the tododb
DATABASE_URL = "sqlite:///./todo.db"


# the engine is the main guard dog for the db allows connection and saving, it manages low level socket connectoins 
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
#this creates a session think of it like a small time block each time a db task is to be executed,
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creates the Base class that our models/db.py will inherit from, pretty much the only important thing that will be used in another file 
Base = declarative_base()

# This dependency opens a DB connection per request and closes it safely when done, a lil isolated room for db requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()