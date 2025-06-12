from sqlmodel import SQLModel, Field, Relationship
from datetime import date


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    birth_date: date | None = None
    nationality: str | None = None

    books: list["Book"] = Relationship(back_populates="author")