from sqlmodel import Session, select
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all(self) -> list[User]:
        return self.db.exec(select(User)).all()
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def update(self, db_user: User, updates: dict) -> User:
        for key, value in updates.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> None:
        user = self.db.get(User, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()