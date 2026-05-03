# Plan 3: Fix Relationship Conflicts

## Objective
Silence SQLAlchemy mapper warnings about overlapping relationships and resolve circular dependencies between school and college models.

## Background
Currently, both School and College models may be defining relationships back to `User`, `Department`, or `Course` that SQLAlchemy perceives as overlapping or conflicting, especially when they share foreign keys.

## Implementation Steps

1. **Identify Warnings**:
   - Start the server (`uvicorn main:app --reload`) and capture all `SAWarning` logs related to overlapping relationships (e.g., `Assignment`, `Note`, `Video`).

2. **Add Overlaps Parameters**:
   - In the parent model (or child model), update the `relationship` definition by adding `overlaps="<relationship_name>"`.
   - Example (if `Assignment` and `Note` conflict over `Course`):
     ```python
     assignments = relationship("Assignment", back_populates="course", overlaps="notes,videos")
     ```

3. **Fix Circular Dependencies in College Models**:
   - Instead of importing models directly at the top of the file, use string-based references in `relationship()`.
   - For `Faculty`:
     ```python
     user = relationship("User", foreign_keys=[user_id])
     department = relationship("Department", primaryjoin="Faculty.department_id == Department.id")
     ```

4. **Validation**:
   - Restart the server and verify that the `SAWarning` logs related to `overlaps` or uninitialized mappers are completely silenced.
