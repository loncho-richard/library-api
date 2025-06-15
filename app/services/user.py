import logging
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.repositories.user import UserRepository
from sqlmodel import Session

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreate) -> UserRead:
        logger.info("Creating user with data: %s", data.model_dump())
        user = UserCreate(**data.model_dump())
        return self.repo.create(user)
    
    def get_users(self) -> list[UserRead]:
        logger.info("Fetching all users")
        return self.repo.get_all()
    
    def get_user(self, user_id: int) -> UserRead | None:
        logger.info("Getting user with ID: %s", user_id)
        return self.repo.get_by_id(user_id)

    def update_user(self, user_id: int, data: UserUpdate) -> UserRead | None:
        logger.info("Updating user ID %s with data: %s", user_id, data.model_dump(exclude_unset=True))
        user = self.repo.get_by_id(user_id)
        if not user:
            logger.warning("User not found for update with ID: %s", user_id)
            return None
        return self.repo.update(user, data.model_dump())

    def delete_user(self, user_id: int) -> bool:
        logger.info("Deleting user with ID: %s", user_id)
        user = self.repo.get_by_id(user_id)
        if not user:
            logger.warning("User not found for deletion with ID: %s", user_id)
            return False
        self.repo.delete(user_id)
        logger.info("User deleted successfully: %s", user_id)
        return True