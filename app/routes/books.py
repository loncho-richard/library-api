from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book import BookService
from app.deps import get_book_service
import csv
from io import StringIO
from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, current_user: User = Depends(get_current_user), service: BookService = Depends(get_book_service)):
    return service.create_book(book)


@router.get("/", response_model=list[BookRead])
async def list_books(limit: int = 100, offset: int = 0, current_user: User = Depends(get_current_user), service: BookService = Depends(get_book_service)):
    return service.get_books(limit=limit, offset=offset)


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, current_user: User = Depends(get_current_user), service: BookService = Depends(get_book_service)):
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, update: BookUpdate, current_user: User = Depends(get_current_user), service: BookService = Depends(get_book_service)):
    book = service.update_book(book_id, update)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, current_user: User = Depends(get_current_user), service: BookService = Depends(get_book_service)):
    if not service.delete_book(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.post("/upload-csv")
async def upload_books_csv(file: UploadFile = File(...), current_user: User = Depends(get_current_user), service: BookService = Depends(get_book_service)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode("utf-8")))
    
    created = []
    errors = []

    for i, row in enumerate(reader, start=1):
        try:
            data = BookCreate(
                title=row["title"],
                isbn=row["isbn"],
                publication_year=int(row["publication_year"]),
                author_id=int(row["author_id"]),
                publisher_id=int(row["publisher_id"]),
            )
            book = service.create_book(data)
            created.append(book)
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")
    
    return {"created": created, "errors": errors}