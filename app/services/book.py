import logging
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.models.book import Book
from app.repositories.book import BookRepository
from app.repositories.author import AuthorRespository
from app.repositories.publisher import PublisherRepository
from sqlmodel import Session

logger = logging.getLogger(__name__)

class BookService:
    def __init__(self, db: Session):
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRespository(db) 
        self.publisher_repo = PublisherRepository(db)
    
    def create_book(self, data: BookCreate) -> BookRead:
        if self.book_repo.get_by_isbn(data.isbn):
            raise ValueError("A book with this ISBN already exists.")
        
        logger.info("Creating book with data: %s", data.model_dump())
        book = Book(**data.model_dump())
        created = self.book_repo.create(book)
        author = self.author_repo.get_by_id(created.author_id)
        publisher = self.publisher_repo.get_by_id(created.publisher_id)
        logger.info("Book created with ID: %s", created.id)
        return BookRead(
            **created.model_dump(),
            author_name=author.name if author else None,
            publisher_name=publisher.name if publisher else None,
            is_available=len(created.loans) == 0,
            due_data=None   
        )
    
    def get_books(self, limit: int = 100, offset: int = 0) -> list[BookRead]:
        logger.info("Fetching books with limit=%s offset=%s", limit, offset)
        books = self.book_repo.get_all()[offset:offset + limit]
        results = []
        for book in books:
            author = self.author_repo.get_by_id(book.author_id)
            publisher = self.publisher_repo.get_by_id(book.publisher_id)
            loan = next((l for l in book.loans if l.return_date is None), None)
            results.append(BookRead(
                **book.model_dump(),
                author_name=author.name if author else None,
                publisher_name=publisher.name if publisher else None,
                is_available=loan is None,
                due_date=loan.due_date if loan else None
            ))
        return results
    
    def get_book(self, book_id: int) -> BookRead | None:
        logger.info("Getting book with ID: %s", book_id)
        book = self.book_repo.get_by_id(book_id)
        if not book:
            logger.warning("Book not found with ID: %s", book_id)
            return None
        author = self.author_repo.get_by_id(book.author_id)
        publisher = self.publisher_repo.get_by_id(book.publisher_id)
        loan = next((l for l in book.loans if l.return_date is None), None)
        return BookRead(
            **book.model_dump(),
            author_name=author.name if author else None,
            publisher_name=publisher.name if publisher else None,
            is_available=loan is None,
            due_date=loan.due_date if loan else None
        )

    def update_book(self, book_id: int, data: BookUpdate) -> BookRead | None:
        logger.info("Updating book ID %s with data: %s", book_id, data.model_dump(exclude_unset=True))
        book = self.book_repo.get_by_id(book_id)
        if not book:
            logger.warning("Book not found for update with ID: %s", book_id)
            return None
        updated = self.book_repo.update(book, data.model_dump(exclude_unset=True))
        author = self.author_repo.get_by_id(updated.author_id)
        publisher = self.publisher_repo.get_by_id(updated.publisher_id)
        loan = next((l for l in updated.loans if l.return_date is None), None)
        return BookRead(
            **updated.model_dump(),
            author_name=author.name if author else None,
            publisher_name=publisher.name if publisher else None,
            is_available=loan is None,
            due_date=loan.due_date if loan else None
        )
    
    def delete_book(self, book_id: int) -> bool:
        logger.info("Deleting book with ID: %s", book_id)
        book = self.book_repo.get_by_id(book_id)
        if not book:
            logger.warning("Book not found for deletion with ID: %s", book_id)
            return False
        self.book_repo.delete(book_id)
        logger.info("Book deleted successfully: %s", book_id)
        return True