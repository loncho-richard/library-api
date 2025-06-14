from sqlmodel import Session, select
from app.models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def get_all(self) -> list[Book]:
        return self.db.exec(select(Book)).all()
    
    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)
    
    def update(self, db_book: Book, updates: dict) -> Book:
        for key, value in updates.items():
            setattr(db_book, key, value)
            self.db.commit()
            self.db.refresh(db_book)
            return db_book
        
    def delete(self, book_id: int) -> None:
        book = self.db.get(Book, book_id)
        if book:
            self.db.delete(book)
            self.db.commit()