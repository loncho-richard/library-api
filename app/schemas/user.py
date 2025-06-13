from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    name: str
    email: str
    join_date: date | None = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int