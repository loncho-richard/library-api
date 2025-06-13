from sqlmodel import Session
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.models.author import Author
from app.repositories.author import AuthorRespository


class AuthorService:
    def __init__(self, db: Session):
        self.repo = AuthorRespository(db)

    def create_author(self, data: AuthorCreate) -> AuthorRead:
        author = Author(**data.model_dump())
        return self.repo.create(author)

    def get_authors(self) -> list[AuthorRead]:
        return self.repo.get_all()

    def get_author(self, author_id: int) -> AuthorRead | None:
        return self.repo.get_by_id(author_id)
    
    def update_author(self, author_id: int, data: AuthorUpdate) -> AuthorRead | None:
        author = self.repo.get_by_id(author_id)
        if not author:
            return None
        return self.repo.update(author, data.model_dump())
    
    def delete_author(self, author_id: int) -> bool:
        author = self.repo.get_by_id(author_id)
        if not author:
            return False
        self.repo.delete(author_id)
        return True