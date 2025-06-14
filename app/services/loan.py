from app.schemas.loan import LoanCreate, LoanRead, LoanUpdate
from app.models.loan import Loan
from app.repositories.loan import LoanRepository
from app.repositories.book import BookRepository
from app.repositories.user import UserRepository
from sqlmodel import Session


class LoanService:
    def __init__(self, db: Session):
        self.loan_repo = LoanRepository(db)
        self.book_repo = BookRepository(db)
        self.user_repo = UserRepository(db)

    def create_loan(self, data: LoanCreate) -> LoanRead:
        loan = Loan(**data.model_dump())
        created = self.loan_repo.create(loan)
        book = self.book_repo.get_by_id(created.book_id)
        user = self.user_repo.get_by_id(created.user_id)
        return LoanRead(
            **created.model_dump(),
            book_title=book.title if book else "",
            user_name=user.name if user else ""
        )
    
    def get_loans(self) -> list[LoanRead]:
        loans = self.loan_repo.get_all()
        results = []
        for loan in loans:
            book = self.book_repo.get_by_id(loan.book_id)
            user = self.user_repo.get_by_id(loan.user_id)
            results.append(LoanRead(
                **loan.model_dump(),
                book_title=book.title if book else "",
                user_name=user.name if user else ""
            ))
        return results
    
    def get_loan(self, loan_id: int) -> LoanRead | None:
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            return None
        book = self.book_repo.get_by_id(loan.book_id)
        user = self.user_repo.get_by_id(loan.user_id)
        return LoanRead(
            **loan.model_dump(),
            book_title=book.title if book else "",
            user_name=user.name if user else ""
        )
    
    def update_loan(self, loan_id: int, data: LoanUpdate) -> LoanRead | None:
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            return None
        updated = self.loan_repo.update(loan, data.dict(exclude_unset=True))
        book = self.book_repo.get_by_id(updated.book_id)
        user = self.user_repo.get_by_id(updated.user_id)
        return LoanRead(
            **updated.model_dump(),
            book_title=book.title if book else "",
            user_name=user.name if user else ""
        )
    
    def delete_loan(self, loan_id: int) -> bool:
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            return False
        self.loan_repo.delete(loan_id)
        return True