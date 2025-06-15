from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    name: str
    email: str
    join_date: date | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None