from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine


DATABASE_URL = "sqlite:///./library.db"

engine: Engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)