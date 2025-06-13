from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.services.author import AuthorService
from app.database import get_session


router = APIRouter(prefix="/authors", tags=["Authors"])


def get_service(db: Session = Depends(get_session)) -> AuthorService:
    return AuthorService(db)


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, service: AuthorService = Depends(get_service)):
    return service.create_author(author)


@router.get("/", response_model=list[AuthorRead])
def list_authors(service: AuthorService = Depends(get_service)):
    return service.get_authors()


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, service: AuthorService = Depends(get_service)):
    author = service.get_author(author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not founds")
    return author


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, update: AuthorUpdate, service: AuthorService = Depends(get_service)):
    updated = service.update_author(author_id, update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return updated


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, service: AuthorService = Depends(get_service)):
    if not service.delete_author(author_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")