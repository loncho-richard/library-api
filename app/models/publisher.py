from sqlmodel import SQLModel, Field, Relationship


class Publisher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    founding_year: int | None = None

    books: list["Book"] = Relationship(back_populates="publisher")