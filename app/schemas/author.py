from pydantic import BaseModel
from datetime import date


class AuthorBase(BaseModel):
    name: str
    birth_date: date | None = None
    nationality: str | None = None

class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int


class AuthorUpdate(AuthorBase):
    pass