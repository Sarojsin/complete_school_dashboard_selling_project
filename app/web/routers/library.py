from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.templates import templates
from app.dependencies import get_async_db, get_current_user_web
from app.models.models import User, UserRole, Student
from app.repositories.library_repository import LibraryRepository
from app.services.library_service import LibraryService

router = APIRouter()

@router.get("/dashboard")
async def library_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    loans = await service.get_all_loans()
    overdue = await service.get_overdue_loans()
    
    return templates.TemplateResponse("library/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "loans": loans[:10],
        "overdue_count": len(overdue)
    })

@router.get("/issue-book")
async def issue_book_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    students = await db.execute("SELECT id, name FROM students")
    
    return templates.TemplateResponse("library/issue_book.html", {
        "request": request,
        "current_user": current_user,
        "students": students.fetchall()
    })

@router.post("/issue-book")
async def issue_book_action(
    request: Request,
    student_id: int = Form(...),
    book_title: str = Form(...),
    book_author: str = Form(...),
    book_isbn: str = Form(None),
    due_days: int = Form(15),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    
    from schemas.library_schemas import BookLoanCreate
    loan_data = BookLoanCreate(
        student_id=student_id,
        book_title=book_title,
        book_author=book_author,
        book_isbn=book_isbn,
        due_days=due_days
    )
    
    await service.issue_book(loan_data)
    
    return templates.TemplateResponse("library/issue_book.html", {
        "request": request,
        "current_user": current_user,
        "success": True,
        "message": "Book issued successfully!"
    })
