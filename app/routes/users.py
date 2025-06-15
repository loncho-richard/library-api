from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import UserService
from app.deps import get_user_service 
from app.core.security import get_current_user


router = APIRouter(prefix="/user", tags=["Users"])



@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)


@router.get("/", response_model=list[UserRead])
async def list_users(current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    return service.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, current_user: User = Depends(get_current_user),  service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, update: UserUpdate, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    user = service.update_user(user_id, update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: User = Depends(get_current_user),  service: UserService = Depends(get_user_service)):
    if not service.delete_user(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")