from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book import BookService
from app.database import get_session


router = APIRouter(prefix="/books", tags=["Books"])


def get_service(db: Session = Depends(get_session)) -> BookService:
    return BookService(db)


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, service: BookService = Depends(get_service)):
    return service.create_book(book)


@router.get("/", response_model=list[BookRead])
async def list_books(service: BookService = Depends(get_service)):
    return service.get_books()


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, service: BookService = Depends(get_service)):
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, update: BookUpdate, service: BookService = Depends(get_service)):
    book = service.update_book(book_id, update)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, service: BookService = Depends(get_service)):
    if not service.delete_book(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")