from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_async_db, get_current_user
from app.models.models import User, UserRole
from app.repositories.account_repository import AccountRepository
from app.services.account_service import AccountService
from app.schemas.account_schemas import TeacherPaymentCreate, TeacherPaymentResponse

router = APIRouter(prefix="/api/account", tags=["Account"])

@router.post("/payments", response_model=TeacherPaymentResponse)
async def record_teacher_payment(
    payment_data: TeacherPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Only Account Section can record payments")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    return await service.record_payment(payment_data, current_user.id)

@router.get("/payments", response_model=List[TeacherPaymentResponse])
async def get_all_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Only Account Section can view all payments")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    return await service.get_all_payments()

@router.get("/payments/teacher/{teacher_id}", response_model=List[TeacherPaymentResponse])
async def get_teacher_payments(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    # Teachers can view their own payments
    if current_user.role == UserRole.TEACHER and current_user.id != teacher_id:
        raise HTTPException(status_code=403, detail="Can only view own payments")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    return await service.get_teacher_payments(teacher_id)

@router.get("/stats", response_model=dict)
async def get_account_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Only Account Section can view stats")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    return await service.get_account_stats()
