Clean Architecture Refactor (Account, Exam, Library, Department)
Refactor the specified modules to strictly follow a Tiered Architecture, ensuring that Routers only handle request/response logic, Services handle business logic, and Repositories handle all data access.

Proposed Changes
[Component] Repository Layer
[MODIFY] 
student_repository.py
: Add methods for fetching students for dropdowns (filtered by grade/section), fetching unique grade levels, and sections.
[MODIFY] 
course_repository.py
: Add methods for fetching unique semesters and courses by name/code.
[MODIFY] 
exam_repository.py
: Move complex result-listing queries and unique semester fetching from the router.
[MODIFY] 
library_repository.py
: Add methods for book catalog search, unique grade/section fetching from students, and active loan queries with student joins.
[Component] Service Layer
[MODIFY] 
account_service.py
: Add methods to wrap repository calls for teacher/student dropdown data.
[MODIFY] 
exam_service.py
: Update to handle filtering logic and pass results to the router in a clean format.
[MODIFY] 
library_service.py
: Add methods for orchestration of book issuance/return, including the necessary dropdown data fetching.
[Component] Router Layer (API Boundary)
[MODIFY] 
account.py
: Remove direct ORM queries. Use 
AccountService
 for everything.
[MODIFY] 
exam_section.py
: Purge SQLAlchemy imports. Rely on 
ExamService
.
[MODIFY] 
library.py
: Refactor to call 
LibraryService
 for both data and metadata (filters).
[MODIFY] 
authority.py
: Major cleanup of direct queries for students, teachers, and courses.
Verification Plan
Automated Tests
N/A (Currently focusing on manual verification and ensuring no regressions in UI rendering).
Manual Verification
Log in as Account Section (account_admin) and verify dashboard, payment recording, and reports work flawlessly.
Log in as Exam Section (
exam_section
) and verify result posting, grade sheets, and notices.
Log in as Library Manager (library_admin) and verify book issuance, returns, catalog, and overdue lists.
Verify navigation and filtering on all these pages still produce the same data results.
