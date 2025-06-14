from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.repositories.user import UserRepository
from sqlmodel import Session


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreate) -> UserRead:
        user = User(**data.model_dump())
        return self.repo.create(user)
    
    def get_users(self) -> list[UserRead]:
        return self.repo.get_all()
    
    def get_user(self, user_id: int) -> UserRead | None:
        return self.repo.get_by_id(user_id)

    def update_user(self, user_id: int, data: UserUpdate) -> UserRead | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        return self.repo.update(user, data.model_dump())

    def delete_user(self, user_id: int) -> bool:
        user = self.repo.get_by_id(user_id)
        if not user:
            return False
        self.repo.delete(user_id)
        return True