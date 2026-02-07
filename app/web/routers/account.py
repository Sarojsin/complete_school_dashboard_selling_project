from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.templates import templates
from app.dependencies import get_async_db, get_current_user_web
from app.models.models import User, UserRole, Teacher
from app.repositories.account_repository import AccountRepository
from app.services.account_service import AccountService

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
    payments = await service.get_all_payments()
    stats = await service.get_account_stats()
    
    return templates.TemplateResponse("account/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "payments": payments[:10],
        "stats": stats
    })

@router.get("/record-payment")
async def record_payment_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.ACCOUNT_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    teachers = await db.execute("SELECT id, name FROM teachers")
    
    return templates.TemplateResponse("account/record_teacher_payment.html", {
        "request": request,
        "current_user": current_user,
        "teachers": teachers.fetchall()
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
    
    from schemas.account_schemas import TeacherPaymentCreate
    payment_data = TeacherPaymentCreate(
        teacher_id=teacher_id,
        amount=amount,
        month=month,
        payment_type=payment_type,
        notes=notes
    )
    
    await service.record_payment(payment_data, current_user.id)
    
    return templates.TemplateResponse("account/record_teacher_payment.html", {
        "request": request,
        "current_user": current_user,
        "success": True,
        "message": "Payment recorded successfully!"
    })