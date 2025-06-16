from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.loan import LoanCreate, LoanRead, LoanUpdate
from app.services.loan import LoanService
from app.deps import get_loan_service
from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
async def create_loan(loan: LoanCreate, current_user: User = Depends(get_current_user), service: LoanService = Depends(get_loan_service)):
    return service.create_loan(loan)


@router.get("/", response_model=list[LoanRead])
async def list_loans(current_user: User = Depends(get_current_user), service: LoanService = Depends(get_loan_service)):
    return service.get_loans()


@router.get("{loan_id}", response_model=LoanRead)
async def get_loan(loan_id: int, current_user: User = Depends(get_current_user), service: LoanService = Depends(get_loan_service)):
    loan = service.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    return loan


@router.put("/{loan_id}", response_model=LoanRead)
async def update_loan(loan_id: int, update: LoanUpdate, current_user: User = Depends(get_current_user), service: LoanService = Depends(get_loan_service)):
    loan = service.update_loan(loan_id, update)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    return loan


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loan(loan_id: int, current_user: User = Depends(get_current_user), service: LoanService = Depends(get_loan_service)):
    if not service.delete_loan(loan_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not founds")