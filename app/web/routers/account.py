from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.templates import templates
from app.dependencies import get_async_db, get_current_user_web
from app.models.models import User, UserRole, Teacher, Student, FeeRecord
from app.repositories.account_repository import AccountRepository
from app.services.account_service import AccountService
from app.schemas.account_schemas import TeacherPaymentCreate, FeePaymentCreate
from datetime import datetime

router = APIRouter()

@router.get("/dashboard")
async def account_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    
    # Get dashboard stats
    stats = await service.get_dashboard_stats()
    payments = await service.get_all_payments()
    
    return templates.TemplateResponse("account/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "stats": stats,
        "payments": payments[:10]
    })

@router.get("/record-payment")
async def record_payment_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get teachers for dropdown using ORM
    teachers_result = await db.execute(
        select(Teacher).order_by(Teacher.full_name)
    )
    teachers = teachers_result.scalars().all()
    
    return templates.TemplateResponse("account/record_teacher_payment.html", {
        "request": request,
        "current_user": current_user,
        "teachers": teachers
    })

@router.post("/record-payment")
async def record_payment_action(
    request: Request,
    teacher_id: int = Form(...),
    amount: float = Form(...),
    month: str = Form(...),
    payment_type: str = Form("salary"),
    notes: str = Form(None),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    
    # Use correct import path
    payment_data = TeacherPaymentCreate(
        teacher_id=teacher_id,
        amount=amount,
        month=month,
        payment_type=payment_type,
        notes=notes
    )
    
    await service.record_payment(payment_data, current_user.id)
    
    # Get teachers for the page again
    teachers_result = await db.execute(
        select(Teacher).order_by(Teacher.full_name)
    )
    teachers = teachers_result.scalars().all()
    
    return templates.TemplateResponse("account/record_teacher_payment.html", {
        "request": request,
        "current_user": current_user,
        "teachers": teachers,
        "success": True,
        "message": "Payment recorded successfully!"
    })

@router.get("/fees")
async def fees_list(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    
    fees = await service.get_fee_payments()
    pending = await service.get_pending_fees()
    
    return templates.TemplateResponse("account/fees.html", {
        "request": request,
        "current_user": current_user,
        "fees": fees,
        "pending": pending
    })

@router.get("/fees/record")
async def record_fee_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get students for dropdown
    students_result = await db.execute(
        select(Student).order_by(Student.full_name)
    )
    students = students_result.scalars().all()
    
    return templates.TemplateResponse("account/record_fee.html", {
        "request": request,
        "current_user": current_user,
        "students": students
    })

@router.post("/fees/record")
async def record_fee_action(
    request: Request,
    student_id: int = Form(...),
    fee_type: str = Form(...),
    amount: float = Form(...),
    remarks: str = Form(None),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    
    fee_data = FeePaymentCreate(
        student_id=student_id,
        fee_type=fee_type,
        amount=amount,
        remarks=remarks
    )
    
    await service.record_fee(fee_data, current_user.id)
    
    return RedirectResponse(url="/account/fees", status_code=302)

@router.get("/payments")
async def payments_history(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    
    payments = await service.get_all_payments()
    
    return templates.TemplateResponse("account/payments.html", {
        "request": request,
        "current_user": current_user,
        "payments": payments
    })

@router.get("/reports")
async def financial_reports(
    request: Request,
    year: int = None,
    month: int = None,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = AccountRepository(db)
    service = AccountService(repo)
    
    # Default to current month if not specified
    if not year or not month:
        now = datetime.utcnow()
        year = now.year
        month = now.month
    
    report = await service.get_monthly_report(year, month)
    
    return templates.TemplateResponse("account/reports.html", {
        "request": request,
        "current_user": current_user,
        "report": report,
        "year": year,
        "month": month
    })
@router.get("/profile")
async def account_profile(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return templates.TemplateResponse("account/profile.html", {
        "request": request,
        "current_user": current_user
    })
