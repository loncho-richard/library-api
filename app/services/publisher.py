import logging
from app.schemas.publisher import PublisherCreate, PublisherRead, PublisherUpdate
from app.models.publisher import Publisher
from app.repositories.publisher import PublisherRepository
from sqlmodel import Session

logger = logging.getLogger(__name__)

class PublisherService:
    def __init__(self, db: Session):
        self.repo = PublisherRepository(db)

    def create_publisher(self, data: PublisherCreate) -> PublisherRead:
        logger.info("Creating publisher with data: %s", data.model_dump())
        publisher = Publisher(**data.model_dump())
        return self.repo.create(publisher)
    
    def get_publishers(self) -> list[PublisherRead]:
        logger.info("Fetching all publishers")
        return self.repo.get_all()
    
    def get_publisher(self, publisher_id: int) -> PublisherRead | None:
        logger.info("Getting publisher with ID: %s", publisher_id)
        return self.repo.get_by_id(publisher_id)
    
    def update_publisher(self, publisher_id: int, data: PublisherUpdate) -> PublisherRead | None:
        logger.info("Updating publisher ID %s with data: %s", publisher_id, data.model_dump(exclude_unset=True))
        publisher = self.repo.get_by_id(publisher_id)
        if not publisher:
            logger.warning("Publisher not found for update with ID: %s", publisher_id)
            return None
        return self.repo.update(publisher, data.model_dump())
    
    def delete_publisher(self, publisher_id: int) -> bool:
        logger.info("Deleting publisher with ID: %s", publisher_id)
        publisher = self.repo.get_by_id(publisher_id)
        if not publisher:
            logger.warning("Publisher not found for deletion with ID: %s", publisher_id)
            return False
        self.repo.delete(publisher_id)
        logger.info("Publisher deleted successfully: %s", publisher_id)
        return True