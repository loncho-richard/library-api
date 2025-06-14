from sqlmodel import Session, select
from app.models.publisher import Publisher


class PublisherRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, publisher: Publisher) -> Publisher:
        self.db.add(publisher)
        self.db.commit()
        self.db.refresh(publisher)
        return publisher
    
    def get_all(self) -> list[Publisher]:
        return self.db.exec(select(Publisher)).all()
    
    def get_by_id(self, publisher_id: int) -> Publisher | None:
        return self.db.get(Publisher, publisher_id)
    
    def update(self, db_publisher: Publisher, updates: dict) -> Publisher:
        for key, value in updates.items():
            setattr(db_publisher, key, value)
        self.db.commit()
        self.db.refresh(db_publisher)
        return db_publisher
    
    def delete(self, publisher_id: int) -> None:
        publisher = self.db.get(Publisher, publisher_id)
        if publisher:
            self.db.delete(publisher)
            self.db.commit()