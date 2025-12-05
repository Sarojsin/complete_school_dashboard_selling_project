# Authority Routes - Complete Implementation
# Replace the existing authority routes with these versions

# ========== STUDENT ROUTES ==========

@app.get("/authority/students")
async def authority_students(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.student_repository import StudentRepository
    from repositories.user_repository import UserRepository
    from models.models import UserRole
    
    if search:
        students_data = StudentRepository.search(db, search)
    else:
        students_data = StudentRepository.get_all(db)
    
    # Format students for template
    formatted_students = []
    for s in students_data:
        formatted_students.append({
            "id": s.id,
            "full_name": s.user.full_name if s.user else "N/A",
            "email": s.user.email if s.user else "N/A",
            "student_id": s.student_id,
            "grade_level": s.grade_level,
            "section": s.section or "N/A",
            "date_of_birth": s.date_of_birth.strftime('%Y-%m-%d') if s.date_of_birth else "N/A",
            "phone": s.phone or "N/A",
            "avatar": f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random",
            "gpa": "N/A",
            "roll_number": s.student_id,
            "fee_status": "paid",
            "attendance": 0,
            "status": "active"
        })
        
    return templates.TemplateResponse("authority/students.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "students": formatted_students,
        "search_query": search
    })

@app.post("/authority/students/add")
async def authority_add_student_post(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from fastapi import Form
    from datetime import datetime
    from repositories.student_repository import StudentRepository
    from repositories.user_repository import UserRepository
    from models.models import UserRole
    import string
    import random
    
    form = await request.form()
    
    # Generate credentials
    first_name = form.get("first_name", "").lower().strip()
    last_name = form.get("last_name", "").lower().strip()
    base_username = f"{first_name}.{last_name}"
    
    # Ensure unique username
    username = base_username
    counter = random.randint(100, 999)
    while UserRepository.get_by_username(db, username):
        username = f"{base_username}{counter}"
        counter += 1
    
    # Generate secure password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    # Create user
    user_data = {
        "username": username,
        "email": form.get("email"),
        "full_name": f"{form.get('first_name')} {form.get('last_name')}",
        "password_hash": UserRepository.get_password_hash(password),
        "role": UserRole.STUDENT
    }
    user = UserRepository.create(db, user_data)
    
    # Create student profile
    student_data = {
        "user_id": user.id,
        "student_id": form.get("student_id"),
        "grade_level": form.get("grade_level"),
        "section": form.get("section"),
        "date_of_birth": datetime.strptime(form.get("date_of_birth"), '%Y-%m-%d').date() if form.get("date_of_birth") else None,
        "phone": form.get("phone"),
        "address": form.get("address"),
        "parent_id": None
    }
    StudentRepository.create(db, student_data)
    
    return RedirectResponse(url=f"/authority/students?success_message=Student created! Username: {username}, Password: {password}", status_code=303)

# ========== TEACHER ROUTES ==========

@app.get("/authority/teachers")
async def authority_teachers(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.teacher_repository import TeacherRepository
    
    if search:
        teachers_data = TeacherRepository.search(db, search)
    else:
        teachers_data = TeacherRepository.get_all(db)
    
    # Format teachers for template
    formatted_teachers = []
    for t in teachers_data:
        formatted_teachers.append({
            "id": t.id,
            "full_name": t.user.full_name if t.user else "N/A",
            "email": t.user.email if t.user else "N/A",
            "employee_id": t.employee_id,
            "department": t.department or "N/A",
            "specialization": t.specialization or "N/A",
            "phone": t.phone or "N/A",
            "hire_date": t.hire_date.strftime('%Y-%m-%d') if t.hire_date else "N/A",
            "avatar": f"https://ui-avatars.com/api/?name={t.user.full_name.replace(' ', '+') if t.user else 'User'}&background=random",
            "courses_taught": 0,
            "students": 0,
            "status": "active"
        })
        
    return templates.TemplateResponse("authority/teachers.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "teachers": formatted_teachers,
        "search_query": search
    })

# ========== COURSE ROUTES ==========

@app.get("/authority/courses")
async def authority_courses(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.course_repository import CourseRepository
    
    if search:
        courses_data = CourseRepository.search(db, search)
    else:
        courses_data = CourseRepository.get_all(db)
    
    # Format courses for template
    formatted_courses = []
    for c in courses_data:
        formatted_courses.append({
            "id": c.id,
            "code": c.course_code,
            "name": c.course_name,
            "description": c.description,
            "credits": c.credits,
            "grade_level": c.grade_level,
            "semester": c.semester,
            "instructor": c.teacher.user.full_name if c.teacher and c.teacher.user else "Unassigned",
            "instructor_avatar": f"https://ui-avatars.com/api/?name={c.teacher.user.full_name if c.teacher and c.teacher.user else 'Unassigned'}&background=random",
            "teacher_id": c.teacher_id,
            "student_count": 0,
            "class_count": 0,
            "avg_grade": 0,
            "department": "Science",
            "department_color": "primary",
            "status": "active"
        })
    
    return templates.TemplateResponse("authority/courses.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "courses": formatted_courses,
        "search_query": search
    })
