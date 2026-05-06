# Day 23 Production Implementation Plan
**Date**: 2026-05-28
**Focus**: User Documentation & Training Materials

## Objectives
- Create comprehensive user manuals for all user roles (Student, Parent, Teacher, HOD, Dean, Registrar, Admin)
- Develop FAQ section addressing common questions
- Outline video tutorial scripts for key workflows
- Prepare in-app help system structure (markdown files + API)
- Ensure all documentation is clear, accessible, and role-specific

## Tasks

### 1. Morning: Documentation Structure Setup (1 hour)
**Create `docs/user_guides/` directory**:
```
docs/user_guides/
├── README.md                     # Index of guides
├── student_guide.md
├── parent_guide.md
├── teacher_guide.md
├── hod_guide.md
├── dean_guide.md
├── registrar_guide.md
├── super_admin_guide.md
├── faq.md
├── videos/
│   ├── student_onboarding.md    # Script + shot list
│   ├── parent_onboarding.md
│   └── admin_onboarding.md
└── help_api.md                   # API for in-app help
```

**Style guide**: Use Markdown with screenshots, numbered steps, warnings in callouts

### 2. Role-Based User Guides (3 hours)
**Each guide should include**:
- Overview of role capabilities
- How to login & reset password
- Day-to-day tasks with step-by-step instructions
- Troubleshooting common issues
- Contact support info

**Student Guide** (`student_guide.md`):
- [ ] Login & dashboard overview
- [ ] View personal profile (photo, roll number, department)
- [ ] View academic timetable
- [ ] Check attendance (if applicable)
- [ ] View exam schedule & results
- [ ] Submit assignments (if applicable)
- [ ] Fee payment status & online payment flow
- [ ] Download ID card / certificates
- [ ] Common issues: "I can't see my results", "Wrong attendance", "Forgot password"

**Parent Guide** (`parent_guide.md`):
- [ ] How to link to children (multiple students)
- [ ] View children's dashboard: attendance, grades, fees due
- [ ] Communication: messaging teachers, viewing notices
- [ ] Fee payment on behalf of student
- [ ] How to add/remove linked students
- [ ] Mobile app usage (if applicable)

**Teacher Guide** (`teacher_guide.md`):
- [ ] Login, profile setup (photo, contact)
- [ ] View assigned classes & timetable
- [ ] Mark attendance (daily/weekly)
- [ ] Enter marks/exam results
- [ ] Create & grade assignments
- [ ] Upload study materials/notes (if library module)
- [ ] Communicate with students/parents (chat, notices)
- [ ] Request leave (if applicable)
- [ ] View payroll / payment info (if integrated)
- [ ] Troubleshooting: "Marks not saving", "Attendance not counting"

**HOD Guide** (`hod_guide.md`):
- [ ] Department overview: faculty list, student count
- [ ] Assign courses to faculty
- [ ] Approve/reject faculty leave requests (if any)
- [ ] View department analytics (performance, pass rate)
- [ ] Publish department notices
- [ ] Manage department labs/equipment (if applicable)
- [ ] View and act on student grievances (if welfare module)
- [ ] Generate department reports

**Dean Guide** (`dean_guide.md`):
- [ ] College-wide analytics dashboard interpretation
- [ ] Faculty performance review workflow
- [ ] Program evaluation (enrollment trends, success rates)
- [ ] Approve new programs/syllabi (if workflow exists)
- [ ] Budget overview & allocation (if account section)
- [ ] Research promotion: view publications/patents
- [ ] Export reports (CSV, Excel)

**Registrar Guide** (`registrar_guide.md`):
- [ ] Enrollment management: confirm admissions, manage waitlist
- [ ] Fee collection monitoring: outstanding, collections report
- [ ] Exam result publication: verify, publish to students
- [ ] Generate certificates (bonafide, migration, etc.)
- [ ] Manage academic calendar/semesters
- [ ] Student grievances escalation
- [ ] Reporting: statutory reports to university/board

**Super Admin Guide** (`super_admin_guide.md`):
- [ ] User management: create, edit, assign roles
- [ ] System configuration: settings, feature flags
- [ ] Backup & restore procedures (manual trigger)
- [ ] View system health: metrics, logs, error rates
- [ ] Manage roles & permissions matrix
- [ ] Security: 2FA enforcement, session management
- [ ] Upgrade/maintenance: run migrations, deploy new version

### 3. FAQ Section (1 hour)
**`faq.md`** – categorize by user type:

**General**:
- Q: How do I reset my password?
  A: Click "Forgot Password" on login page; check email for reset link (valid 1 hour).
- Q: I didn't receive the verification email. What to do?
  A: Check spam folder; if still missing, contact admin at support@example.com.
- Q: Can I change my email address?
  A: Yes, go to Profile → Edit → Change Email; verification required.
- Q: Why can't I login?
  A: Ensure caps lock off; if using 2FA, enter correct code; contact admin if account locked.

**Students**:
- Q: Where can I see my exam results?
  A: Login → Academics → Results; published by registrar.
- Q: How to pay fees online?
  A: Dashboard → Fees → "Pay Now" connects to payment gateway (Razorpay/Stripe).
- Q: My attendance is incorrect. Who to contact?
  A: Contact class teacher first; if not resolved, approach HOD.

**Parents**:
- Q: How do I add my child's account to my profile?
  A: In Parent Dashboard → "Link Student" → enter student roll number; student must approve link.
- Q: Can I pay fees for multiple children together?
  A: Yes, cart feature in Fees section.

**Faculty**:
- Q: How to enter marks for internal assessment?
  A: Course → Assessments → "Enter Marks" → select batch → save → submit for HOD approval.
- Q: My course is not showing in my dashboard. Why?
  A: HOD may not have assigned you yet; contact HOD.

**Admins**:
- Q: How to backup the database?
  A: Super Admin → System → Backup Now; also automated daily at 2 AM.
- Q: What if a migration fails?
  A: Check `alembic` version; rollback: `alembic downgrade -1`; contact tech team.

### 4. Video Tutorial Scripts (1 hour)
**Outline scripts** (full scripts recorded later, but outline for each):

**Student Onboarding** (`videos/student_onboarding.md`):
- Scene 1: Login screen (0:00-0:15)
- Scene 2: Dashboard panels explanation (0:15-1:00)
- Scene 3: View profile + edit photo (1:00-1:30)
- Scene 4: Check attendance & results (1:30-2:15)
- Scene 5: Pay fees (2:15-3:00)
- Scene 6: Contact support (3:00-3:30)
- Voiceover script + on-screen text

**Similarly** for parent, teacher, admin (shorter scripts 3-5 min each)

**Note**: Actual video production is outside scope but scripts ready for recording

### 5. In-App Help System Structure (1 hour)
**API for contextual help** (`modules/shared/help/router.py`):
```python
router = APIRouter(prefix="/api/v1/help", tags=["help"])

@router.get("/articles/{role}")
async def get_help_articles(role: str):
    """Return list of help article titles for given role (student/parent/teacher/...)"""
    # Load from markdown files or DB
    articles = [
        {"id": "login", "title": "How to Login", "role": "all"},
        {"id": "password_reset", "title": "Reset Password", "role": "all"},
        # ...
    ]
    return {"articles": articles}

@router.get("/article/{article_id}")
async def get_article(article_id: str):
    """Return full markdown content (converted to HTML or raw)"""
    # Read from `docs/user_guides/{article_id}.md`
    with open(f"docs/user_guides/{article_id}.md") as f:
        content = f.read()
    return {"article": content, "format": "markdown"}
```

**Frontend**: Contextual help button calls `/api/v1/help?role=student&topic=login`

### 6. Accessibility & Formatting (1 hour)
- Use plain language, avoid jargon
- Step numbering: `1.`, `2.`, `3.`
- Warnings: `> **⚠️ Warning:** ...`
- Notes: `> **Note:** ...`
- Screenshots: place in `docs/screenshots/` with captions
- Ensure mobile-friendly reading (shorter paragraphs)

### 7. Commit (30 min)
- [ ] `docs/user_guides/` directory with 8+ guides
- [ ] `docs/faq.md` with 30+ Q&As
- [ ] `docs/videos/` scripts
- [ ] `modules/shared/help/router.py` (optional)
- [ ] Update `README.md` with link to documentation
- [ ] Commit: "docs: Add comprehensive user guides for all roles, FAQ, video scripts, help API"

## Deliverables
- ✅ 9 markdown user guides (student, parent, teacher, HOD, dean, registrar, super_admin, + general)
- ✅ FAQ with 30+ questions
- ✅ 3 video tutorial outlines (student, parent, admin)
- ✅ Help API endpoints (optional)
- ✅ Documentation organized in `docs/` with clear index

## Success Criteria
- New user can read relevant guide and understand how to use system
- All common support questions answered in FAQ
- Help system can be integrated into frontend (React pages)
- Guides cover all modules and roles comprehensively

## Notes
- Keep guides up-to-date as features change; assign owner for doc updates
- Consider translating guides to Hindi and other regional languages later
- Video scripts will be recorded by content team; provide clear voiceover text
- Use consistent terminology across guides (match UI labels)

## Next: Day 24
Final security & performance audit: run full bandit scan, dependency audit (pip-audit), load testing with k6/locust, fix any bottlenecks, achieve 70%+ test coverage.
