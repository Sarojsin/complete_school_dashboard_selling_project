
@app.delete("/teacher/tests/delete/{id}")
async def teacher_delete_test(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Test deleted successfully"})

@app.post("/teacher/students/{student_id}/contact")
async def teacher_contact_student(request: Request, student_id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Message sent successfully"})

@app.delete("/teacher/assignments/delete/{id}")
async def teacher_delete_assignment(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Assignment deleted successfully"})

@app.delete("/teacher/attendance/delete/{id}")
async def teacher_delete_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Attendance record deleted successfully"})
