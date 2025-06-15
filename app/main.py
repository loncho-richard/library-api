import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.initial_data import seed_database
from app.core.config import settings

from app.routes.books import router as books_router
from app.routes.authors import router as authors_router
from app.routes.publishers import router as publishers_router
from app.routes.users import router as users_router
from app.routes.loans import router as loans_router
from app.routes.system import router as system_router
from app.routes.auth import router as auth_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Library API",
    version="1.0.0",
    description="API for administrate the library"
)

@app.on_event("startup")
def on_startup():
    seed_database()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(books_router)
app.include_router(authors_router)
app.include_router(publishers_router)
app.include_router(users_router)
app.include_router(loans_router)
app.include_router(system_router)
app.include_router(auth_router)