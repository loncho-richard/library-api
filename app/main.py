import logging
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.initial_data import seed_database

from app.routes.books import router as books_router
from app.routes.authors import router as authors_router
from app.routes.publishers import router as publishers_router
from app.routes.users import router as users_router
from app.routes.loans import router as loans_router
from app.routes.system import router as system_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Library API",
    version="1.0.0",
    description="API for administrate the library"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_database()


app.include_router(books_router)
app.include_router(authors_router)
app.include_router(publishers_router)
app.include_router(users_router)
app.include_router(loans_router)
app.include_router(system_router)