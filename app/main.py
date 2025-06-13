from fastapi import FastAPI
from app.database import create_db_and_tables
from app.initial_data import seed_database
import os


app = FastAPI(
    title="Library API",
    version="1.0.0",
    description="API for administrate the library"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_database()