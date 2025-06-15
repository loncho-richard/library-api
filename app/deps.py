from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from app.services.book import BookService
from app.services.author import AuthorService
from app.services.loan import LoanService
from app.services.publisher import PublisherService
from app.services.user import UserService


def get_book_service(db: Session = Depends(get_session)) -> BookService:
    return BookService(db)


def get_author_service(db: Session = Depends(get_session)) -> AuthorService:
    return AuthorService(db)


def get_loan_service(db: Session = Depends(get_session)) -> LoanService:
    return LoanService(db)


def get_publisher_service(db: Session = Depends(get_session)) -> PublisherService:
    return PublisherService(db)


def get_user_service(db: Session = Depends(get_session)) -> UserService:
    return UserService(db)