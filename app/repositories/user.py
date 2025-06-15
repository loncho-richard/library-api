from sqlmodel import Session, select
from app.models.user import User
from app.core.hashing import get_password_hash
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_all(self) -> list[User]:
        return self.db.exec(select(User)).all()
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.exec(select(User).where(User.email == email)).first()
    
    def update(self, user: User, user_update: UserUpdate) -> User:
        update_data = user_update.model_dump(exclude_unset=True, exclude={"password"})

        if user_update.password:
            update_data["hashed_password"] = get_password_hash(user_update.password)

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> None:
        user = self.db.get(User, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()