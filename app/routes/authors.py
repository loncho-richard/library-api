from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.services.author import AuthorService
from app.deps import get_author_service
from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, current_user: User = Depends(get_current_user), service: AuthorService = Depends(get_author_service)):
    return service.create_author(author)


@router.get("/", response_model=list[AuthorRead])
def list_authors(current_user: User = Depends(get_current_user), service: AuthorService = Depends(get_author_service)):
    return service.get_authors()


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, current_user: User = Depends(get_current_user), service: AuthorService = Depends(get_author_service)):
    author = service.get_author(author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not founds")
    return author


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, update: AuthorUpdate, current_user: User = Depends(get_current_user), service: AuthorService = Depends(get_author_service)):
    updated = service.update_author(author_id, update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return updated


@router.delete("/{author_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, current_user: User = Depends(get_current_user), service: AuthorService = Depends(get_author_service)):
    if not service.delete_author(author_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")