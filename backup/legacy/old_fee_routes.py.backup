@app.get("/authority/fees")
async def authority_fees(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/fees.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "fees": [],
        "pending_amount": 0
    })

@app.get("/authority/fees/structure")
async def authority_fee_structure_old(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Redirect to main fee structure route
    return RedirectResponse(url="/authority/fee-structure", status_code=301)

@app.post("/authority/fees/structure")
async def authority_fee_structure_post(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Handle POST - same as /authority/fee-structure POST
    from repositories.fee_structure_repository import FeeStructureRepository
    from datetime import datetime
    
    form = await request.form()
    
    #Extract form data
    tuition_fee = float(form.get("tuition_fee", 0))
    registration_fee = float(form.get("registration_fee", 0))
    library_fee = float(form.get("library_fee", 0))
    sports_fee = float(form.get("sports_fee", 0))
    lab_fee = float(form.get("lab_fee", 0))
    activity_fee = float(form.get("activity_fee", 0))
    other_charges = float(form.get("other_charges", 0))
    
    total_amount = (tuition_fee + registration_fee + library_fee + 
                   sports_fee + lab_fee + activity_fee + other_charges)
    
    structure_data = {
        "grade_level": form.get("grade_level"),
        "academic_year": form.get("academic_year"),
        "tuition_fee": tuition_fee,
        "registration_fee": registration_fee,
        "library_fee": library_fee,
        "sports_fee": sports_fee,
        "lab_fee": lab_fee,
        "activity_fee": activity_fee,
        "other_charges": other_charges,
        "total_amount": total_amount,
        "status": form.get("status", "active"),
        "description": form.get("description"),
        "due_date": datetime.strptime(form.get("due_date"), '%Y-%m-%d').date() if form.get("due_date") else None
    }
    
    FeeStructureRepository.create(db, structure_data)
    
    return RedirectResponse(url="/authority/fees/structure", status_code=303)

@app.get("/authority/fees/add")
async def authority_add_fee(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_fee.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user
    })
