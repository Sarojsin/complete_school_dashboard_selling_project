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
(+) authority/notices/add:Internal Server Errorfee 
(*) authority/notices/: yeta . after (-)
(*)group/ 
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


