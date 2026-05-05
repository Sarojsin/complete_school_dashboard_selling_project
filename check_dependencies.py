"""
Check foreign key dependencies in new college module tables
"""

# college_exam_notices references:
#   - users.id (created_by)
#   - college_semesters.id (semester_id) -> college_semusters must exist

# college_exam_results references:
#   - college_students.id
#   - college_courses.id
#   - college_semesters.id (optional)
#   - users.id (published_by)

# college_faculty_payments references:
#   - college_faculty.id
#   - users.id (paid_by_user_id)

# Also backup models CollegeStudent references:
#   - users.id (user_id)
#   - college_programs.id
#   - college_semesters.id

# CollegeCourse references:
#   - college_departments.id
#   - college_semesters.id
#   - college_faculty.id (instructor_id)

# Enrollment references:
#   - college_students.id
#   - college_courses.id
#   - college_semesters.id

# So the dependency order for creating tables should be:
# 1. college_departments (for faculty and courses)
# 2. college_faculty (for courses, and payments)
# 3. college_programs (for students)
# 4. college_semesters (for courses, students, enrollments)
# 5. college_courses (for enrollments, exam_results)
# 6. college_students (for enrollments, exam_results, applications)
# 7. college_enrollments (base)
# 8. Then placement/research/hostel/lab/fee tables
# 9. Finally new module tables: college_exam_notices, college_exam_results, college_faculty_payments

dependencies = {
    "college_departments": [],
    "college_faculty": ["college_departments"],
    "college_programs": ["college_departments"],
    "college_semesters": ["college_programs"],
    "college_courses": ["college_departments", "college_faculty", "college_semesters"],
    "college_students": ["college_programs", "college_semesters"],
    "college_enrollments": ["college_students", "college_courses", "college_semesters"],
    # Placement
    "placement_companies": [],  # but migration uses this name, backup uses companies
    "placement_jobs": ["placement_companies"],
    "placement_applications": ["placement_jobs", "college_students"],
    # Research
    "research_projects": ["college_faculty"],
    "research_publications": ["college_faculty", "research_projects"],
    "research_patents": ["college_faculty"],
    # Hostel
    "hostels": ["college_faculty"],
    "rooms": ["hostels"],
    "hostel_allocations": ["college_students", "rooms"],
    "hostel_complaints": ["college_students", "hostels", "rooms", "college_faculty"],
    # Lab
    "labs": ["college_departments", "college_faculty"],  # migration name
    "lab_equipment": ["labs"],
    "lab_schedules": ["labs", "college_courses", "college_semesters", "college_faculty"],
    # Fee
    "college_fee_structures": ["college_programs", "college_semesters"],
    "college_fee_records": ["college_students", "college_semesters"],
    # New modules
    "college_exam_notices": ["users", "college_semesters"],
    "college_exam_results": ["college_students", "college_courses", "college_semesters", "users"],
    "college_faculty_payments": ["college_faculty", "users"],
}

print("Table creation dependency order:")
print("="*60)
# Simple topological sort simulation
created = set()
order = []
while len(created) < len(dependencies):
    progress = False
    for table, deps in dependencies.items():
        if table not in created and all(d in created for d in deps):
            order.append(table)
            created.add(table)
            progress = True
    if not progress:
        print("WARNING: Circular dependency or missing table!")
        missing = [t for t in dependencies if t not in created]
        print(f"Remaining: {missing}")
        break

print("\nSuggested creation order:")
for i, t in enumerate(order, 1):
    deps = dependencies[t]
    if deps:
        print(f"{i:2}. {t} (requires: {', '.join(deps)})")
    else:
        print(f"{i:2}. {t} (no dependencies)")
