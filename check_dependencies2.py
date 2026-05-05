"""
Check foreign key dependencies in new college module tables
"""

dependencies = {
    # Base college (from migration 1f0fc964eedc)
    "college_departments": [],
    "college_faculty": ["college_departments"],
    "college_programs": ["college_departments"],
    "college_semesters": ["college_programs"],
    "college_courses": ["college_departments", "college_faculty", "college_semesters"],
    "college_students": ["college_programs", "college_semesters"],
    "college_enrollments": ["college_students", "college_courses", "college_semesters"],
    # Placement (migration uses different names - here using backup names)
    "placement_companies": [],  # migration uses this; backup uses companies
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
    "labs": ["college_departments", "college_faculty"],
    "lab_equipment": ["labs"],
    "lab_schedules": ["labs", "college_courses", "college_semesters", "college_faculty"],
    # Fee (not in migrations but in backup models)
    "college_fee_structures": ["college_programs", "college_semesters"],
    "college_fee_records": ["college_students", "college_semesters"],
    # New module tables (from 20260505 migration)
    "college_exam_notices": ["users", "college_semesters"],
    "college_exam_results": ["college_students", "college_courses", "college_semesters", "users"],
    "college_faculty_payments": ["college_faculty", "users"],
}

print("Table creation dependency order:")
print("="*60)

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
        remaining = [t for t in dependencies if t not in created]
        print(f"Remaining: {remaining}")
        # Try to break ties by adding one with most deps already met
        for t in remaining:
            deps = dependencies[t]
            met = [d for d in deps if d in created]
            if len(met) == len(deps) - 1:
                print(f"  Could add: {t} (waiting on {[d for d in deps if d not in created]})")
        break

print("\nSuggested creation order:")
for i, t in enumerate(order, 1):
    deps = dependencies[t]
    if deps:
        print(f"{i:2}. {t} (requires: {', '.join(sorted(deps))})")
    else:
        print(f"{i:2}. {t} (no dependencies)")

print(f"\nTotal tables ordered: {len(order)}/{len(dependencies)}")
