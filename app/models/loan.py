from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from .book import Book
from .user import User


class Loan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    loan_date: date = Field(default_factory=date.today)
    due_date: date
    return_date: date | None = None

    book: Book = Relationship(back_populates="loans")
    user: User = Relationship(back_populates="loans")