from sqlmodel import SQLModel, Field, Relationship
from datetime import date


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    join_date: date = Field(default_factory=date.today)

    loans: list["Loan"] = Relationship(back_populates="user")