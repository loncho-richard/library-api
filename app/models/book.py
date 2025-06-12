from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from .author import Author
from .publisher import Publisher


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    isbn: str = Field(unique=True, index=True)
    publication_year: int

    author_id: int = Field(foreign_key="author.id")
    publisher_id: int = Field(foreign_key="publisher.id")

    author: Author = Relationship(back_populates="books")
    publisher: Publisher = Relationship(back_populates="books")
    loans: list["Loan"] = Relationship(back_populates="book")