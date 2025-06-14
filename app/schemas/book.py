from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: int
    author_id: int
    publisher_id: int


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    author_name: str
    publisher_name: str
    is_available: bool
    due_date: date | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = None
    publication_year: int | None = None
    author_id: int | None = None
    publisher_id: int | None = None