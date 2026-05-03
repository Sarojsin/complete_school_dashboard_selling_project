from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from backup.core.templates import templates
from backup.dependencies import get_async_db, get_current_user_web
from backup.models.models import User, UserRole, Student
from backup.repositories.library_repository import LibraryRepository
from backup.services.library_service import LibraryService
from backup.schemas.library_schemas import BookLoanCreate, BookCreate
from backup.models.library_models import Book, BookLoan
from datetime import date

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
    
    # Get dashboard stats
    stats = await service.get_dashboard_stats()
    loans = await service.get_all_loans()
    overdue = await service.get_overdue_loans()
    
    return templates.TemplateResponse("library/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "stats": stats,
        "loans": loans[:10],
        "overdue_count": len(overdue),
        "today": date.today()
    })

@router.get("/issue-book")
async def issue_book_page(
    request: Request,
    grade: str = None,
    section: str = None,
    search: str = None,
    book_id: int = None,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Build student query with filters
    query = select(Student)
    
    # Apply filters
    if grade:
        query = query.where(Student.grade_level == grade)
    if section:
        query = query.where(Student.section == section)
    if search:
        query = query.where(
            or_(
                Student.full_name.ilike(f"%{search}%"),
                Student.student_id.ilike(f"%{search}%")
            )
        )
    
    query = query.order_by(Student.full_name)
    students_result = await db.execute(query)
    students = students_result.scalars().all()
    
    # Get unique grades and sections for filter dropdowns
    grades_result = await db.execute(
        select(Student.grade_level).distinct().order_by(Student.grade_level)
    )
    available_grades = [g[0] for g in grades_result.all() if g[0]]
    
    sections_result = await db.execute(
        select(Student.section).distinct().order_by(Student.section)
    )
    available_sections = [s[0] for s in sections_result.all() if s[0]]
    
    # Get available books from catalog
    books_result = await db.execute(
        select(Book).where(Book.available_copies > 0).order_by(Book.title)
    )
    available_books = books_result.scalars().all()
    
    # Get selected book details if book_id is provided
    selected_book = None
    if book_id:
        book_result = await db.execute(
            select(Book).where(Book.id == book_id)
        )
        selected_book = book_result.scalar_one_or_none()
    
    return templates.TemplateResponse("library/issue_book.html", {
        "request": request,
        "current_user": current_user,
        "students": students,
        "available_books": available_books,
        "selected_book_id": book_id,
        "selected_book": selected_book,
        "filters": {
            "grade": grade,
            "section": section,
            "search": search
        },
        "available_grades": available_grades,
        "available_sections": available_sections
    })

@router.post("/issue-book")
async def issue_book_action(
    request: Request,
    student_id: int = Form(...),
    book_id: int = Form(None),
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
    
    # Use correct import path
    loan_data = BookLoanCreate(
        student_id=student_id,
        book_id=book_id,
        book_title=book_title,
        book_author=book_author,
        book_isbn=book_isbn,
        due_days=due_days
    )
    
    await service.issue_book(loan_data)
    
    # Get data for the page again with default filters
    students_result = await db.execute(
        select(Student).order_by(Student.full_name)
    )
    students = students_result.scalars().all()
    
    # Get unique grades and sections for filter dropdowns
    grades_result = await db.execute(
        select(Student.grade_level).distinct().order_by(Student.grade_level)
    )
    available_grades = [g[0] for g in grades_result.all() if g[0]]
    
    sections_result = await db.execute(
        select(Student.section).distinct().order_by(Student.section)
    )
    available_sections = [s[0] for s in sections_result.all() if s[0]]
    
    # Get available books from catalog
    books_result = await db.execute(
        select(Book).where(Book.available_copies > 0).order_by(Book.title)
    )
    available_books = books_result.scalars().all()
    
    return templates.TemplateResponse("library/issue_book.html", {
        "request": request,
        "current_user": current_user,
        "students": students,
        "available_books": available_books,
        "filters": {"grade": None, "section": None, "search": None},
        "available_grades": available_grades,
        "available_sections": available_sections,
        "success": True,
        "message": "Book issued successfully!"
    })

@router.get("/return-book")
async def return_book_page(
    request: Request,
    search: str = None,
    grade: str = None,
    section: str = None,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Build query for active loans with student info
    query = (
        select(BookLoan, Student)
        .join(Student, BookLoan.student_id == Student.id)
        .where(BookLoan.status == "borrowed")
    )
    
    # Apply filters
    if search:
        query = query.where(
            or_(
                Student.full_name.ilike(f"%{search}%"),
                Student.student_id.ilike(f"%{search}%"),
                BookLoan.book_title.ilike(f"%{search}%")
            )
        )
    if grade:
        query = query.where(Student.grade_level == grade)
    if section:
        query = query.where(Student.section == section)
    
    query = query.order_by(BookLoan.due_date)
    result = await db.execute(query)
    rows = result.all()
    
    # Combine loan and student data
    loans = []
    for row in rows:
        loan = row[0]
        student = row[1]
        loan.student = student  # Attach student to loan object
        loans.append(loan)
    
    # Get unique grades and sections for filter dropdowns
    grades_result = await db.execute(
        select(Student.grade_level).distinct().order_by(Student.grade_level)
    )
    available_grades = [g[0] for g in grades_result.all() if g[0]]
    
    sections_result = await db.execute(
        select(Student.section).distinct().order_by(Student.section)
    )
    available_sections = [s[0] for s in sections_result.all() if s[0]]
    
    return templates.TemplateResponse("library/return_book.html", {
        "request": request,
        "current_user": current_user,
        "loans": loans,
        "today": date.today(),
        "filters": {
            "search": search,
            "grade": grade,
            "section": section
        },
        "available_grades": available_grades,
        "available_sections": available_sections
    })

@router.post("/return-book/{loan_id}")
async def return_book_action(
    loan_id: int,
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    
    await service.return_book(loan_id)
    
    return RedirectResponse(url="/library/return-book", status_code=302)

@router.get("/overdue")
async def overdue_books(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get overdue loans with student info
    from datetime import datetime
    today_date = datetime.utcnow().date()
    
    # First get all active loans
    result = await db.execute(
        select(BookLoan, Student)
        .join(Student, BookLoan.student_id == Student.id)
        .where(BookLoan.status == "borrowed")
        .order_by(BookLoan.due_date)
    )
    rows = result.all()
    
    # Filter overdue in Python to avoid SQLAlchemy date comparison issues
    overdue = []
    for row in rows:
        loan = row[0]
        student = row[1]
        if loan.due_date and loan.due_date < today_date:
            loan.student = student  # Attach student to loan object
            overdue.append(loan)
    
    return templates.TemplateResponse("library/overdue.html", {
        "request": request,
        "current_user": current_user,
        "overdue": overdue,
        "today": today_date
    })

@router.get("/history/{student_id}")
async def student_history(
    student_id: int,
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get student info
    student_result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    
    history = await service.get_student_history(student_id)
    
    return templates.TemplateResponse("library/history.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "history": history
    })

@router.get("/books")
async def book_catalog(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    
    if search:
        books = await service.search_books(search)
    else:
        books = await service.get_all_books()
    
    return templates.TemplateResponse("library/books.html", {
        "request": request,
        "current_user": current_user,
        "books": books,
        "search": search
    })

@router.get("/books/add")
async def add_book_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return templates.TemplateResponse("library/add_book.html", {
        "request": request,
        "current_user": current_user
    })

@router.post("/books/add")
async def add_book_action(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(None),
    category: str = Form(None),
    total_copies: int = Form(1),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    
    book_data = BookCreate(
        title=title,
        author=author,
        isbn=isbn,
        category=category,
        total_copies=total_copies
    )
    
    await service.add_book(book_data)
    
    return RedirectResponse(url="/library/books", status_code=302)
@router.get("/profile")
async def library_profile(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return templates.TemplateResponse("library/profile.html", {
        "request": request,
        "current_user": current_user
    })
