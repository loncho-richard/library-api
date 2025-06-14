from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.models.book import Book
from app.repositories.book import BookRepository
from app.repositories.author import AuthorRespository
from app.repositories.publisher import PublisherRepository
from sqlmodel import Session


class BookService:
    def __init__(self, db: Session):
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRespository(db) 
        self.publisher_repo = PublisherRepository(db)
    
    def create_book(self, data: BookCreate) -> BookRead:
        book = Book(**data.model_dump())
        created = self.book_repo.create(book)
        author = self.author_repo.get_by_id(created.author_id)
        publisher = self.publisher_repo.get_by_id(created.publisher_id)
        return BookRead(
            **created.model_dump(),
            author_name=author.name if author else None,
            publisher_name=publisher.name if publisher else None,
            is_available=len(created.loans) == 0,
            due_data=None   
        )
    
    def get_books(self) -> list[BookRead]:
        books = self.book_repo.get_all()
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
        book = self.book_repo.get_by_id(book_id)
        if not book:
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
        book = self.book_repo.get_by_id(book_id)
        if not book:
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
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False
        self.book_repo.delete(book_id)
        return True