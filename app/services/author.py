import logging
from sqlmodel import Session
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.models.author import Author
from app.repositories.author import AuthorRespository

logger = logging.getLogger(__name__)

class AuthorService:
    def __init__(self, db: Session):
        self.repo = AuthorRespository(db)

    def create_author(self, data: AuthorCreate) -> AuthorRead:
        logger.info("Creating author with data: %s", data.model_dump())
        author = Author(**data.model_dump())
        return self.repo.create(author)

    def get_authors(self) -> list[AuthorRead]:
        logger.info("Fetching all authors")
        return self.repo.get_all()

    def get_author(self, author_id: int) -> AuthorRead | None:
        logger.info("Getting author with ID: %s", author_id)
        return self.repo.get_by_id(author_id)
    
    def update_author(self, author_id: int, data: AuthorUpdate) -> AuthorRead | None:
        logger.info("Updating author ID %s with data: %s", author_id, data.model_dump(exclude_unset=True))
        author = self.repo.get_by_id(author_id)
        if not author:
            logger.warning("Author not found for update with ID: %s", author_id)
            return None
        return self.repo.update(author, data.model_dump())
    
    def delete_author(self, author_id: int) -> bool:
        logger.info("Deleting author with ID: %s", author_id)
        author = self.repo.get_by_id(author_id)
        if not author:
            logger.warning("Author not found for deletion with ID: %s", author_id)
            return False
        self.repo.delete(author_id)
        logger.info("Author deleted successfully: %s", author_id)
        return True