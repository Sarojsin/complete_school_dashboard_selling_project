## issue_to_solve.md
need to solve (*)
not really an issue(+)
solved the issue(-)

(*) authority/students/1/edit :{"detail":"Method Not Allowed"}
(*) authority/students/1 : could not send the message
(*) authority/students/add:{"detail":"Method Not Allowed"} 
(*)authority/teachers/1/edit:{"detail":"Method Not Allowed"}
(*)authority/teachers/1 : could not send the message
(*) authority/teachers/add:{"detail":"Method Not Allowed"}
(*)teacher/notes and /videos : could not send the message 
  how to solve
  teacher_upload_notes
  (GET) to fetch the teacher's enrolled courses.
  Add teacher_upload_notes_post (POST) to handle file uploads, save them to the filesystem, and create database records using 
  NotesRepository
  teacher_upload_videos
  (GET) to fetch the teacher's enrolled courses.
  Add teacher_upload_videos_post (POST) to handle video uploads and create records using 
  VideosRepository
  student_notes
  (GET) to fetch notes for the student's enrolled courses.
  student_videos
  (GET) to fetch videos for the student's enrolled courses.

(+) authority/notices/add:Internal Server Errorfee 
(+)student/assignments . ma grade wise assignment not comming . sabai class ko aaudai cha.
   I need to solve this issue by using 
   filter while student is getting his assignment from database.
   filter by grade , which teacher is providing the assignment.
   (-)submission  wala part thik cha it working aali glitch gudai cha .


(*) authority/notices/: yeta . after (-)
(*)group/ .(-)
what to solve on it ?
❗ High-Priority Issues (Must Fix)
Duplicate / wrong repository method
Issue: update_group() defined twice, uses non-existent get_by_id
Fix: Keep one update_group() and use get_group_by_id()
Service constructor mismatch
Issue: GroupService(group_repo, user_repo) but constructor accepts only group_repo
Fix: Either:
Update constructor to accept user_repo, OR
Always use group_repo.session
Mixed exception types
Issue: HTTPException + custom errors used together
Fix: Use only custom exceptions in service, map to HTTP in routes
UserRepository usage unclear
Issue: Static call style may not match repository design
Fix: Instantiate UserRepository(db) or standardize static usage
No DB-level unique constraint
Issue: Duplicate (group_id, user_id) possible
Fix:
UniqueConstraint("group_id", "user_id")
⚠️ Medium / Behavioral Issues
Role enforcement inconsistency
Issue: Routes allow Authority/Admin, service checks only teacher
Fix: Define single permission rule in service
Enum not enforced
Issue: post_type stored as string
Fix: Use SQLAlchemy Enum or validate via Pydantic
Templates depend on session
Issue: request.session used
Fix: Ensure SessionMiddleware exists
🧪 Missing Safety / Quality
No unit tests
Add tests for:
Group creation
Member invite/remove
Permission checks
Group detail fetch
No migration for constraints
Add Alembic migration for:
Unique constraint
Enum enforcement (optional)
## issue is solved
Fixed Issues
1. Repository — Removed duplicate update_group method

Deleted the broken second implementation that called non-existent get_by_id()
Kept the first update_group(group_id, update_data) method
2. Service — Standardized exception handling

Removed HTTPException usage from group_service.py
Now uses custom exceptions (NotFoundError, PermissionDeniedError, ValidationError) consistently
Fixed update_group to call repository with correct method signature
3. Routes — Fixed dependency injection

Removed incorrect UserRepository(db) instantiation (UserRepository uses static methods)
Added proper exception handling for custom exceptions in all route handlers:
update_group — catches NotFoundError, PermissionDeniedError
add_members — catches NotFoundError, PermissionDeniedError
remove_member — catches NotFoundError, PermissionDeniedError, ValidationError
4. Routes — Fixed data access bug

Changed group_data["creator"]["id"] → group_data["created_by"] in edit_group_page

