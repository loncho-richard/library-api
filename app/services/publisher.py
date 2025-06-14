from app.schemas.publisher import PublisherCreate, PublisherRead, PublisherUpdate
from app.models.publisher import Publisher
from app.repositories.publisher import PublisherRepository
from sqlmodel import Session


class PublisherService:
    def __init__(self, db: Session):
        self.repo = PublisherRepository(db)

    def create_publisher(self, data: PublisherCreate) -> PublisherRead:
        publisher = Publisher(**data.model_dump())
        return self.repo.create(publisher)
    
    def get_publishers(self) -> list[PublisherRead]:
        return self.repo.get_all()
    
    def get_publisher(self, publisher_id: int) -> PublisherRead | None:
        return self.repo.get_by_id(publisher_id)
    
    def update_publisher(self, publisher_id: int, data: PublisherUpdate) -> PublisherRead | None:
        publisher = self.repo.get_by_id(publisher_id)
        if not publisher:
            return None
        return self.repo.update(publisher, data.model_dump())
    
    def delete_publisher(self, publisher_id: int) -> bool:
        publisher = self.repo.get_by_id(publisher_id)
        if not publisher:
            return False
        self.repo.delete(publisher_id)
        return True