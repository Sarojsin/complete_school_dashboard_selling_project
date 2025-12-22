import os

def fix_main_py():
    main_py = "main.py"
    if not os.path.exists(main_py):
        print(f"Error: {main_py} not found")
        return

    with open(main_py, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the old block for teacher_create_assignment GET
    old_get_route = """@app.get("/teacher/assignments/create")
async def teacher_create_assignment(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/create_assignment.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user
    })"""

    # Define the new block for teacher_create_assignment GET
    new_get_route = """@app.get("/teacher/assignments/create")
async def teacher_create_assignment(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from models.models import Course 
    courses = db.query(Course).all()
    return templates.TemplateResponse("teacher/create_assignment.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": courses
    })"""

    updated_content = content.replace(old_get_route, new_get_route)

    if updated_content != content:
        with open(main_py, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("Updated teacher_create_assignment in main.py")
    else:
        print("teacher_create_assignment GET route not found for replacement")

if __name__ == "__main__":
    fix_main_py()
