import logging
from app.schemas.loan import LoanCreate, LoanRead, LoanUpdate
from app.models.loan import Loan
from app.repositories.loan import LoanRepository
from app.repositories.book import BookRepository
from app.repositories.user import UserRepository
from sqlmodel import Session

logger = logging.getLogger(__name__)

class LoanService:
    def __init__(self, db: Session):
        self.loan_repo = LoanRepository(db)
        self.book_repo = BookRepository(db)
        self.user_repo = UserRepository(db)

    def create_loan(self, data: LoanCreate) -> LoanRead:
        logger.info("Creating loan with data: %s", data.model_dump())
        loan = Loan(**data.model_dump())
        created = self.loan_repo.create(loan)
        book = self.book_repo.get_by_id(created.book_id)
        user = self.user_repo.get_by_id(created.user_id)
        logger.info("Loan created with ID: %s", created.id)
        return LoanRead(
            **created.model_dump(),
            book_title=book.title if book else "",
            user_name=user.name if user else ""
        )
    
    def get_loans(self) -> list[LoanRead]:
        logger.info("Fetching all loans")
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
        logger.info("Getting loan with ID: %s", loan_id)
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            logger.warning("Loan not found with ID: %s", loan_id)
            return None
        book = self.book_repo.get_by_id(loan.book_id)
        user = self.user_repo.get_by_id(loan.user_id)
        return LoanRead(
            **loan.model_dump(),
            book_title=book.title if book else "",
            user_name=user.name if user else ""
        )
    
    def update_loan(self, loan_id: int, data: LoanUpdate) -> LoanRead | None:
        logger.info("Updating loan ID %s with data: %s", loan_id, data.model_dump(exclude_unset=True))
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            logger.warning("Loan not found for update with ID: %s", loan_id)
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
        logger.info("Deleting loan with ID: %s", loan_id)
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            logger.warning("Loan not found for deletion with ID: %s", loan_id)
            return False
        self.loan_repo.delete(loan_id)
        logger.info("Loan deleted successfully: %s", loan_id)
        return True