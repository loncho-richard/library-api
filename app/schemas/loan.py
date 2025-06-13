from pydantic import BaseModel
from datetime import date


class LoanBase(BaseModel):
    book_id: int
    user_id: int
    due_date: date


class LoanCreate(LoanBase):
    pass


class LoanRead(LoanBase):
    id: int
    loan_date: date
    return_date: date | None = None
    book_title: str
    user_name: str