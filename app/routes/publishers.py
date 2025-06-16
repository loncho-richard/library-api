from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.publisher import PublisherCreate, PublisherRead, PublisherUpdate
from app.services.publisher import PublisherService
from app.deps import get_publisher_service
from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/publishers", tags=["Publishers"])



@router.post("/", response_model=PublisherRead, status_code=status.HTTP_201_CREATED)
async def create_publisher(publisher: PublisherCreate, current_user: User = Depends(get_current_user), service: PublisherService = Depends(get_publisher_service)):
    return service.create_publisher(publisher)

@router.get("/", response_model=list[PublisherRead])
async def list_publishers(current_user: User = Depends(get_current_user), service: PublisherService = Depends(get_publisher_service)):
    return service.get_publishers()

@router.get("/{publisher_id}", response_model=PublisherRead)
async def get_publisher(publisher_id: int, current_user: User = Depends(get_current_user), service: PublisherService = Depends(get_publisher_service)):
    publisher = service.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

@router.put("/{publisher_id}", response_model=PublisherRead)
async def update_publisher(publisher_id: int, update: PublisherUpdate, current_user: User = Depends(get_current_user), service: PublisherService = Depends(get_publisher_service)):
    publisher = service.update_publisher(publisher_id, update)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

@router.delete("/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publisher(publisher_id: int, current_user: User = Depends(get_current_user), service: PublisherService = Depends(get_publisher_service)):
    if not service.delete_publisher(publisher_id):
        raise HTTPException(status_code=404, detail="Publisher not found")