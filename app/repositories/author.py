from sqlmodel import Session, select
from app.models.author import Author


class AuthorRespository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, author: Author) -> Author:
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author
    
    def get_all(self) -> list[Author]:
        return self.db.exec(select(Author)).all()
    
    def get_by_id(self, author_id: int) -> Author | None:
        return self.db.get(Author, author_id)
    
    def update(self, db_author: Author, updates: dict) -> Author:
        for key, value in updates.items():
            setattr(db_author, key, value)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author
    
    def delete(self, author_id: int) -> None:
        author = self.db.get(Author, author_id)
        if author:
            self.db.delete(author)
            self.db.commit()