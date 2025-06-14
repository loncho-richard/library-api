from sqlmodel import Session, select
from app.models.loan import Loan


class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan
    
    def get_all(self) -> list[Loan]:
        return self.db.exec(select(Loan)).all()
    
    def get_by_id(self, loan_id: int) -> Loan | None:
        return self.db.get(Loan, loan_id)

    def update(self, db_loan: Loan, updates: dict) -> Loan:
        for key, value in updates.items():
            setattr(db_loan, key, value)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan

    def delete(self, loan_id: int) -> None:
        loan = self.db.get(Loan, loan_id)
        if loan:
            self.db.delete(loan)
            self.db.commit()