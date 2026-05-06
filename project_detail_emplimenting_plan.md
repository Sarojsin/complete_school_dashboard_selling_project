school_management_system/
├── 📂 -p/
├── 📂 alembic/
│   ├── 📂 versions/
│   │   ├── 🐍 22683032b580_initial_migration.py
│   │   ├── 🐍 32177aaa75d6_add_all_modular_models_v3.py
│   │   ├── 🐍 9ce7ad18c90b_initial_college_migration.py
│   │   └── 🐍 d1a2b3c4d5e6_add_portal_type_to_users.py
│   ├── 📄 README
│   ├── 🐍 env.py
│   └── 📄 script.py.mako
├── 📂 alembic_college/
│   ├── 📂 versions/
│   │   └── 🐍 1f0fc964eedc_initial_college_base_schema.py
│   ├── 📄 README
│   ├── 🐍 env.py
│   └── 📄 script.py.mako
├── 📱 app/
│   ├── 🐍 __init__.py
│   └── 🐍 main.py
├── 📂 doc/
│   ├── 📝 COMPREHENSIVE_FEATURE_DOCUMENTATION.md
│   ├── 📝 MIGRATION_CHANGELOG.md
│   ├── 📝 README.md
│   ├── 📝 RENDER_DEPLOYMENT.md
│   ├── 📝 admin.md
│   ├── 📝 api_testing.md
│   ├── 📝 complete_uidesign.md
│   ├── 📝 csrf.md
│   ├── 📝 deployment.md
│   ├── 📝 enrollment_system.md
│   ├── 📝 finally_check_list.md
│   ├── 📝 group.md
│   ├── 📝 guide.md
│   ├── 📝 issue_to_solve.md
│   ├── 📝 issued_by_claud.md
│   ├── 📝 kilo_code_task_mar-25-2026_1-37-39-am.md
│   ├── 📝 know_about_project.md
│   ├── 📝 lets_go.md
│   ├── 📝 lets_go2.md
│   ├── 📝 logic_feature.md
│   ├── 📝 missingplan1.md
│   ├── 📝 model.md
│   ├── 📝 model_plan.md
│   ├── 📝 new.md
│   ├── 📝 new_roles.md
│   ├── 📝 plan.md
│   ├── 📝 plan_implemented.md
│   ├── 📝 problem.md
│   ├── 📝 production_ready.md
│   ├── 📝 project_detail_emplimenting_plan.md
│   ├── 📝 project_report.md
│   ├── 📝 project_structure.md
│   ├── 📝 quick_Solve_issue_API.md
│   ├── 📝 quickstart.md
│   ├── 📝 roadmap_to_10.md
│   ├── 📝 security.md
│   ├── 📝 test.md
│   ├── 📝 things_to_add_on security.md
│   └── 📝 things_we_learn_by_this_project.md
├── 📚 docs/
│   └── 📝 adding_a_new_module.md
├── 🖥️ frontend/
│   ├── 🌍 public/
│   │   ├── 🖌️ favicon.svg
│   │   └── 🖌️ icons.svg
│   ├── 📦 src/
│   │   ├── 🖼️ assets/
│   │   │   ├── 🖼️ hero.png
│   │   │   ├── 🖌️ react.svg
│   │   │   └── 🖌️ vite.svg
│   │   ├── 📂 modules/
│   │   │   ├── 📂 auth/
│   │   │   │   ├── 🔌 api/
│   │   │   │   │   ├── 🟨 auth.js
│   │   │   │   │   └── 🟨 signup.js
│   │   │   │   ├── 📄 pages/
│   │   │   │   │   ├── ⚛️ DashboardRedirector.jsx
│   │   │   │   │   ├── ⚛️ LandingPage.jsx
│   │   │   │   │   ├── ⚛️ LoginPage.jsx
│   │   │   │   │   ├── ⚛️ RegisterChoice.jsx
│   │   │   │   │   └── ⚛️ SignupPage.jsx
│   │   │   │   └── 🎨 styles/
│   │   │   │       └── 🎨 auth.css
│   │   │   ├── 📂 collage/
│   │   │   │   ├── 📂 collage_placement/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 students.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   └── ⚛️ GlassCard.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 usePlacement.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ StudentDashboard.jsx
│   │   │   │   └── 📂 collage_teacher/
│   │   │   │       ├── 🔌 api/
│   │   │   │       │   └── 🟨 teachers.js
│   │   │   │       ├── 🧩 components/
│   │   │   │       │   └── ⚛️ GlassCard.jsx
│   │   │   │       ├── 🪝 hooks/
│   │   │   │       │   └── 🟨 useCollegeTeacher.js
│   │   │   │       ├── 📂 lib/
│   │   │   │       │   └── 🟨 toast.js
│   │   │   │       └── 📄 pages/
│   │   │   │           └── ⚛️ TeacherDashboard.jsx
│   │   │   ├── 📂 college/
│   │   │   │   ├── 📂 college_account_section/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 account.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ AccountDashboard.jsx
│   │   │   │   ├── 📂 college_dean/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 dean.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ DeanDashboard.jsx
│   │   │   │   ├── 📂 college_exam_section/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 exam.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ ExamDashboard.jsx
│   │   │   │   ├── 📂 college_hod/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 hod.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ HODDashboard.jsx
│   │   │   │   ├── 📂 college_hostel/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 hostel.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ HostelDashboard.jsx
│   │   │   │   ├── 📂 college_lab/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 lab.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ LabDashboard.jsx
│   │   │   │   ├── 📂 college_library/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 library.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ LibraryDashboard.jsx
│   │   │   │   ├── 📂 college_registrar/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 registrar.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ RegistrarDashboard.jsx
│   │   │   │   ├── 📂 college_research/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 research.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ ResearchDashboard.jsx
│   │   │   │   └── 📂 college_student/
│   │   │   │       └── 🔌 api/
│   │   │   │           └── 🟨 students.js
│   │   │   ├── 📂 school/
│   │   │   │   ├── 📂 school_account_section/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 account.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   └── ⚛️ GlassCard.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useAccount.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   └── ⚛️ AccountDashboard.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 account.css
│   │   │   │   ├── 📂 school_attendance/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 attendance.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   └── ⚛️ GlassCard.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useAttendance.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   └── ⚛️ AttendanceDashboard.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 attendance.css
│   │   │   │   ├── 📂 school_authority/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   ├── 🟨 authority.js
│   │   │   │   │   │   └── 🟨 students.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useAuthority.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       ├── 📂 authority/
│   │   │   │   │       │   ├── ⚛️ AddCourse.jsx
│   │   │   │   │       │   ├── 🎨 AddEdit.css
│   │   │   │   │       │   ├── ⚛️ AddNotice.jsx
│   │   │   │   │       │   ├── ⚛️ AddStudent.jsx
│   │   │   │   │       │   ├── ⚛️ AddTeacher.jsx
│   │   │   │   │       │   ├── ⚛️ Analytics.jsx
│   │   │   │   │       │   ├── 🎨 AuthorityDetail.css
│   │   │   │   │       │   ├── 🎨 AuthorityFees.css
│   │   │   │   │       │   ├── 🎨 AuthorityGroups.css
│   │   │   │   │       │   ├── 🎨 AuthorityNotices.css
│   │   │   │   │       │   ├── 🎨 AuthorityReports.css
│   │   │   │   │       │   ├── ⚛️ CourseDetail.jsx
│   │   │   │   │       │   ├── ⚛️ CreateGroup.jsx
│   │   │   │   │       │   ├── ⚛️ EditCourse.jsx
│   │   │   │   │       │   ├── ⚛️ EditNotice.jsx
│   │   │   │   │       │   ├── ⚛️ EditStudent.jsx
│   │   │   │   │       │   ├── ⚛️ EditTeacher.jsx
│   │   │   │   │       │   ├── ⚛️ FeeStructure.jsx
│   │   │   │   │       │   ├── ⚛️ Fees.jsx
│   │   │   │   │       │   ├── ⚛️ ManageGroup.jsx
│   │   │   │   │       │   ├── ⚛️ Reports.jsx
│   │   │   │   │       │   ├── ⚛️ StudentDetail.jsx
│   │   │   │   │       │   ├── ⚛️ TeacherDetail.jsx
│   │   │   │   │       │   └── ⚛️ ViewNotice.jsx
│   │   │   │   │       ├── ⚛️ AdminAnalytics.jsx
│   │   │   │   │       ├── ⚛️ AdminFees.jsx
│   │   │   │   │       ├── 🎨 AuthorityDashboard.css
│   │   │   │   │       ├── ⚛️ AuthorityDashboard.jsx
│   │   │   │   │       ├── ⚛️ Students.jsx
│   │   │   │   │       └── ⚛️ Teachers.jsx
│   │   │   │   ├── 📂 school_chat/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 chat.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   ├── 🟨 useChat.js
│   │   │   │   │   │   └── 🟨 useWebSocket.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   ├── ⚛️ ChatDashboard.jsx
│   │   │   │   │   │   ├── ⚛️ ChatList.jsx
│   │   │   │   │   │   └── ⚛️ ChatWindow.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 chat.css
│   │   │   │   ├── 📂 school_exam_section/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 examSection.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useExamSection.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   ├── ⚛️ ExamDashboard.jsx
│   │   │   │   │   │   ├── ⚛️ ExamGradeSheet.jsx
│   │   │   │   │   │   ├── ⚛️ ExamNotices.jsx
│   │   │   │   │   │   ├── ⚛️ ExamPostResult.jsx
│   │   │   │   │   │   └── 🎨 ExamSection.css
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 exam-section.css
│   │   │   │   ├── 📂 school_groups/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 groups.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useGroups.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   ├── ⚛️ CreateGroup.jsx
│   │   │   │   │   │   ├── ⚛️ GroupDetail.jsx
│   │   │   │   │   │   ├── ⚛️ GroupEdit.jsx
│   │   │   │   │   │   ├── ⚛️ GroupList.jsx
│   │   │   │   │   │   ├── ⚛️ GroupManageMembers.jsx
│   │   │   │   │   │   ├── ⚛️ GroupPosts.jsx
│   │   │   │   │   │   ├── ⚛️ NewPost.jsx
│   │   │   │   │   │   └── ⚛️ ViewPost.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 groups.css
│   │   │   │   ├── 📂 school_hod/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 hod.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   └── ⚛️ GlassCard.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useHod.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   ├── ⚛️ HODDashboard.jsx
│   │   │   │   │   │   └── ⚛️ HODProfile.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 hod.css
│   │   │   │   ├── 📂 school_library/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 library.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useLibrary.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   ├── ⚛️ AddBook.jsx
│   │   │   │   │   │   ├── ⚛️ Books.jsx
│   │   │   │   │   │   ├── ⚛️ IssueBook.jsx
│   │   │   │   │   │   ├── ⚛️ LibraryDashboard.jsx
│   │   │   │   │   │   ├── ⚛️ Overdue.jsx
│   │   │   │   │   │   └── ⚛️ ReturnBook.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 library.css
│   │   │   │   ├── 📂 school_notes/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 notes.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   └── ⚛️ GlassCard.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useNotes.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   └── ⚛️ NotesDashboard.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 notes.css
│   │   │   │   ├── 📂 school_parent/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 parents.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useParent.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   ├── ⚛️ ChildAttendance.jsx
│   │   │   │   │   │   ├── ⚛️ ChildFees.jsx
│   │   │   │   │   │   ├── ⚛️ ChildGrades.jsx
│   │   │   │   │   │   ├── ⚛️ ParentChat.jsx
│   │   │   │   │   │   ├── ⚛️ ParentDashboard.jsx
│   │   │   │   │   │   ├── ⚛️ ParentHomework.jsx
│   │   │   │   │   │   ├── ⚛️ ParentNotices.jsx
│   │   │   │   │   │   └── ⚛️ ParentProfile.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 parent.css
│   │   │   │   ├── 📂 school_student/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 students.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useStudent.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       ├── 🎨 AssignmentDetail.css
│   │   │   │   │       ├── ⚛️ AssignmentDetail.jsx
│   │   │   │   │       ├── ⚛️ Assignments.jsx
│   │   │   │   │       ├── 🎨 Attendance.css
│   │   │   │   │       ├── ⚛️ Attendance.jsx
│   │   │   │   │       ├── 🎨 Courses.css
│   │   │   │   │       ├── ⚛️ Courses.jsx
│   │   │   │   │       ├── 🎨 ExamResults.css
│   │   │   │   │       ├── ⚛️ ExamResults.jsx
│   │   │   │   │       ├── 🎨 Forum.css
│   │   │   │   │       ├── ⚛️ Forum.jsx
│   │   │   │   │       ├── 🎨 Grades.css
│   │   │   │   │       ├── ⚛️ Grades.jsx
│   │   │   │   │       ├── ⚛️ Notices.jsx
│   │   │   │   │       ├── 🎨 StudentDashboard.css
│   │   │   │   │       ├── ⚛️ StudentDashboard.jsx
│   │   │   │   │       ├── 🎨 StudentFees.css
│   │   │   │   │       ├── ⚛️ StudentFees.jsx
│   │   │   │   │       ├── 🎨 StudentProfile.css
│   │   │   │   │       ├── ⚛️ StudentProfile.jsx
│   │   │   │   │       ├── 🎨 StudentTeachers.css
│   │   │   │   │       ├── ⚛️ StudentTeachers.jsx
│   │   │   │   │       ├── 🎨 TakeTest.css
│   │   │   │   │       ├── ⚛️ TakeTest.jsx
│   │   │   │   │       ├── 🎨 TestList.css
│   │   │   │   │       ├── ⚛️ TestList.jsx
│   │   │   │   │       ├── 🎨 TestResult.css
│   │   │   │   │       └── ⚛️ TestResult.jsx
│   │   │   │   ├── 📂 school_teacher/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 teachers.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useTeacher.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       ├── ⚛️ Assignments.jsx
│   │   │   │   │       ├── 🎨 Courses.css
│   │   │   │   │       ├── ⚛️ Courses.jsx
│   │   │   │   │       ├── ⚛️ CreateAssignment.jsx
│   │   │   │   │       ├── 🎨 Students.css
│   │   │   │   │       ├── ⚛️ Students.jsx
│   │   │   │   │       ├── ⚛️ TeacherAddGrade.jsx
│   │   │   │   │       ├── ⚛️ TeacherAttendance.jsx
│   │   │   │   │       ├── ⚛️ TeacherCourseDetail.jsx
│   │   │   │   │       ├── ⚛️ TeacherCreateTest.jsx
│   │   │   │   │       ├── 🎨 TeacherDashboard.css
│   │   │   │   │       ├── ⚛️ TeacherDashboard.jsx
│   │   │   │   │       ├── ⚛️ TeacherEditAssignment.jsx
│   │   │   │   │       ├── ⚛️ TeacherEditTest.jsx
│   │   │   │   │       ├── ⚛️ TeacherGrades.jsx
│   │   │   │   │       ├── ⚛️ TeacherGroups.jsx
│   │   │   │   │       ├── ⚛️ TeacherNotices.jsx
│   │   │   │   │       ├── 🎨 TeacherPortal.css
│   │   │   │   │       ├── ⚛️ TeacherProfile.jsx
│   │   │   │   │       ├── ⚛️ TeacherStudentDetail.jsx
│   │   │   │   │       ├── ⚛️ TeacherTakeAttendance.jsx
│   │   │   │   │       ├── ⚛️ TeacherTimetable.jsx
│   │   │   │   │       ├── ⚛️ TeacherUploadNotes.jsx
│   │   │   │   │       ├── ⚛️ TeacherUploadVideos.jsx
│   │   │   │   │       └── ⚛️ TeacherViewSubmissions.jsx
│   │   │   │   ├── 📂 school_timetable/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 timetable.js
│   │   │   │   │   ├── 🧩 components/
│   │   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   │   └── ⚛️ SkeletonShimmer.jsx
│   │   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   │   └── 🟨 useTimetable.js
│   │   │   │   │   ├── 📂 lib/
│   │   │   │   │   │   └── 🟨 toast.js
│   │   │   │   │   ├── 📄 pages/
│   │   │   │   │   │   └── ⚛️ TimetableDashboard.jsx
│   │   │   │   │   └── 🎨 styles/
│   │   │   │   │       └── 🎨 timetable.css
│   │   │   │   └── 📂 school_videos/
│   │   │   │       ├── 🔌 api/
│   │   │   │       │   └── 🟨 videos.js
│   │   │   │       ├── 🧩 components/
│   │   │   │       │   └── ⚛️ GlassCard.jsx
│   │   │   │       ├── 🪝 hooks/
│   │   │   │       │   └── 🟨 useVideos.js
│   │   │   │       ├── 📂 lib/
│   │   │   │       │   └── 🟨 toast.js
│   │   │   │       ├── 📄 pages/
│   │   │   │       │   └── ⚛️ VideosDashboard.jsx
│   │   │   │       └── 🎨 styles/
│   │   │   │           └── 🎨 videos.css
│   │   │   ├── 📂 shared/
│   │   │   │   ├── 🔌 api/
│   │   │   │   │   └── 🟨 client.js
│   │   │   │   ├── 🧩 components/
│   │   │   │   │   ├── 🎨 Badge.css
│   │   │   │   │   ├── ⚛️ Badge.jsx
│   │   │   │   │   ├── ⚛️ Button.jsx
│   │   │   │   │   ├── 🎨 Card.css
│   │   │   │   │   ├── ⚛️ Card.jsx
│   │   │   │   │   ├── ⚛️ DataTable.jsx
│   │   │   │   │   ├── ⚛️ GlassCard.jsx
│   │   │   │   │   ├── ⚛️ Modal.jsx
│   │   │   │   │   ├── ⚛️ ModernBadge.jsx
│   │   │   │   │   ├── ⚛️ ModernStatCard.jsx
│   │   │   │   │   ├── 🎨 Navbar.css
│   │   │   │   │   ├── ⚛️ Navbar.jsx
│   │   │   │   │   ├── 🎨 PageHeader.css
│   │   │   │   │   ├── ⚛️ PageHeader.jsx
│   │   │   │   │   ├── ⚛️ PrivateRoute.jsx
│   │   │   │   │   ├── 🎨 Sidebar.css
│   │   │   │   │   ├── ⚛️ Sidebar.jsx
│   │   │   │   │   ├── 🎨 StatCard.css
│   │   │   │   │   └── ⚛️ StatCard.jsx
│   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   └── 🟨 useAuth.js
│   │   │   │   ├── 📂 layouts/
│   │   │   │   │   ├── ⚛️ AuthLayout.jsx
│   │   │   │   │   ├── 🎨 MainLayout.css
│   │   │   │   │   └── ⚛️ MainLayout.jsx
│   │   │   │   ├── 🎨 styles/
│   │   │   │   │   └── 🎨 global.css
│   │   │   │   └── 🔧 utils/
│   │   │   │       └── 🟨 dateFormatter.js
│   │   │   └── 📂 super_admin/
│   │   │       ├── 🔌 api/
│   │   │       │   ├── 🟨 students.js
│   │   │       │   └── 🟨 superadmin.js
│   │   │       ├── 🧩 components/
│   │   │       │   ├── ⚛️ GlassCard.jsx
│   │   │       │   └── ⚛️ SkeletonShimmer.jsx
│   │   │       ├── 🪝 hooks/
│   │   │       │   └── 🟨 useSuperAdmin.js
│   │   │       ├── 📂 lib/
│   │   │       │   └── 🟨 toast.js
│   │   │       ├── 📄 pages/
│   │   │       │   ├── ⚛️ Academic.jsx
│   │   │       │   ├── ⚛️ AdminNotices.jsx
│   │   │       │   ├── 🎨 AdminPages.css
│   │   │       │   ├── ⚛️ Advanced.jsx
│   │   │       │   ├── ⚛️ AuditLogs.jsx
│   │   │       │   ├── ⚛️ Backups.jsx
│   │   │       │   ├── ⚛️ Communication.jsx
│   │   │       │   ├── ⚛️ FeatureDetail.jsx
│   │   │       │   ├── ⚛️ Features.jsx
│   │   │       │   ├── ⚛️ Finance.jsx
│   │   │       │   ├── ⚛️ Media.jsx
│   │   │       │   ├── ⚛️ Reports.jsx
│   │   │       │   ├── ⚛️ Security.jsx
│   │   │       │   ├── ⚛️ Settings.jsx
│   │   │       │   ├── 🎨 SuperAdminDashboard.css
│   │   │       │   ├── ⚛️ SuperAdminDashboard.jsx
│   │   │       │   ├── ⚛️ System.jsx
│   │   │       │   └── ⚛️ Users.jsx
│   │   │       └── 🎨 styles/
│   │   │           └── 🎨 superadmin.css
│   │   ├── 🎨 styles/
│   │   │   └── 🎨 variables.css
│   │   ├── 🎨 App.css
│   │   ├── ⚛️ App.jsx
│   │   ├── 🎨 index.css
│   │   └── 🚀 main.jsx
│   ├── 📄 .gitignore
│   ├── 📝 README.md
│   ├── 🟨 eslint.config.js
│   ├── 🌐 index.html
│   ├── 🧾 package-lock.json
│   ├── 📦 package.json
│   └── ⚡ vite.config.js
├── 📂 frontend_plan/
│   ├── 📝 fronted_plan1.md
│   ├── 📝 fronted_plan2.md
│   ├── 📝 fronted_plan3.md
│   ├── 📝 fronted_plan4.md
│   ├── 📝 fronted_plan5.md
│   ├── 📝 frontend_mapping1_auth.md
│   ├── 📝 frontend_mapping2_school_student.md
│   ├── 📝 frontend_mapping3_school_teacher.md
│   ├── 📝 frontend_mapping4_school_authority.md
│   ├── 📝 frontend_mapping5_school_parent.md
│   ├── 📝 frontend_mapping6_school_library.md
│   ├── 📝 frontend_mapping7_super_admin.md
│   ├── 📝 frontend_mapping8_school_other_modules.md
│   ├── 📝 frontend_mapping_index.md
│   ├── 📝 frontend_migration.md
│   ├── 📝 frontend_missing_service_endpointsplan1.md
│   ├── 📝 frontend_missing_service_endpointsplan10.md
│   ├── 📝 frontend_missing_service_endpointsplan2.md
│   ├── 📝 frontend_missing_service_endpointsplan3.md
│   ├── 📝 frontend_missing_service_endpointsplan4.md
│   ├── 📝 frontend_missing_service_endpointsplan5.md
│   ├── 📝 frontend_missing_service_endpointsplan6.md
│   ├── 📝 frontend_missing_service_endpointsplan7.md
│   ├── 📝 frontend_missing_service_endpointsplan8.md
│   ├── 📝 frontend_missing_service_endpointsplan9.md
│   ├── 📝 frontend_plan1.1.md
│   ├── 📝 frontend_plan2.1.md
│   ├── 📝 frontend_plan3.1.md
│   ├── 📝 frontend_plan4.1.md
│   ├── 📝 frontend_plan5.1.md
│   ├── 📝 frontend_react_migration_plan.md
│   ├── 📝 plan1.md
│   ├── 📝 plan10.md
│   ├── 📝 plan11.md
│   ├── 📝 plan12.md
│   ├── 📝 plan13.md
│   ├── 📝 plan14.md
│   ├── 📝 plan15.md
│   ├── 📝 plan16.md
│   ├── 📝 plan17.md
│   ├── 📝 plan18.md
│   ├── 📝 plan19.md
│   ├── 📝 plan2.md
│   ├── 📝 plan20.md
│   ├── 📝 plan21.md
│   ├── 📝 plan22.md
│   ├── 📝 plan3.md
│   ├── 📝 plan4.md
│   ├── 📝 plan5.md
│   ├── 📝 plan6.md
│   ├── 📝 plan7.md
│   ├── 📝 plan8.md
│   └── 📝 plan9.md
├── 📂 modules/
│   ├── 📂 auth/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 api.py
│   │   ├── 🐍 dependencies.py
│   │   ├── 🐍 repository.py
│   │   ├── 🐍 router.py
│   │   ├── 🐍 schemas.py
│   │   ├── 🐍 service.py
│   │   └── 🐍 utils.py
│   ├── 📂 college/
│   │   ├── 📂 college_account_section/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_courses/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   └── 🐍 service.py
│   │   ├── 📂 college_dean/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_enrollments/
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_exam_section/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_faculty/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 college_hod/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_hostel/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   └── 🐍 service.py
│   │   ├── 📂 college_lab/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   └── 🐍 service.py
│   │   ├── 📂 college_library/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 college_placement/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   └── 🐍 service.py
│   │   ├── 📂 college_programs/
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_registrar/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_research/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   └── 🐍 service.py
│   │   ├── 📂 college_semesters/
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_student/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 🐍 base.py
│   │   └── 🐍 database.py
│   ├── 📂 school/
│   │   ├── 📂 school_account_section/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_assignments/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_attendance/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_authority/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_chat/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 websocket.py
│   │   ├── 📂 school_classes/
│   │   │   └── 🐍 models.py
│   │   ├── 📂 school_courses/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_dashboard/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_exam_section/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_grades/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_groups/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_hod/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   └── 🐍 router.py
│   │   ├── 📂 school_library/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_notes/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_notices/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_parent/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_student/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_subjects/
│   │   │   └── 🐍 models.py
│   │   ├── 📂 school_teacher/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_tests/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   ├── 📂 school_timetable/
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   └── 🐍 utils.py
│   │   └── 📂 school_videos/
│   │       ├── 🧪 tests/
│   │       │   └── 🐍 __init__.py
│   │       ├── 🐍 __init__.py
│   │       ├── 🐍 api.py
│   │       ├── 🐍 constants.py
│   │       ├── 🐍 exceptions.py
│   │       ├── 🐍 models.py
│   │       ├── 🐍 repository.py
│   │       ├── 🐍 router.py
│   │       ├── 🐍 schemas.py
│   │       ├── 🐍 service.py
│   │       └── 🐍 utils.py
│   ├── 📂 shared/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 auth.py
│   │   ├── 🐍 auth_utils.py
│   │   ├── 🐍 base.py
│   │   ├── 🐍 config.py
│   │   ├── 🐍 database.py
│   │   ├── 🐍 exceptions.py
│   │   ├── 🐍 feature_guard.py
│   │   ├── 🐍 health.py
│   │   ├── 🐍 logger.py
│   │   ├── 🐍 models.py
│   │   └── 🐍 utils.py
│   ├── 📂 super_admin/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 api.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 repository.py
│   │   ├── 🐍 schemas.py
│   │   └── 🐍 service.py
│   ├── 🐍 __init__.py
│   ├── 📝 modules_endpoints.md
│   └── 📝 modules_missing_endpoints.md
├── 📂 plans/
│   ├── 📝 Converting_All_Roles_to_React_with_Modular_Structure.md
│   ├── 📝 School_vs_College_mode.md
│   ├── 📝 admin.md
│   ├── 📝 admin_feature_control_plan.md
│   ├── 📝 all_school_modules_migration_plan.md
│   ├── 📝 collage.md
│   ├── 📝 duplicate.md
│   ├── 📝 elite_migration.md
│   ├── 📝 elite_plan1.md
│   ├── 📝 elite_plan10.md
│   ├── 📝 elite_plan11.md
│   ├── 📝 elite_plan12.md
│   ├── 📝 elite_plan2.md
│   ├── 📝 elite_plan3.md
│   ├── 📝 elite_plan4.md
│   ├── 📝 elite_plan5.md
│   ├── 📝 elite_plan6.md
│   ├── 📝 elite_plan7.md
│   ├── 📝 elite_plan8.md
│   ├── 📝 elite_plan9.md
│   ├── 📝 final_missingplan1.md
│   ├── 📝 final_missingplan2.md
│   ├── 📝 future_plan_Can_add.md
│   ├── 📝 logic_plan1.md
│   ├── 📝 logic_plan2.md
│   ├── 📝 logic_plan3.md
│   ├── 📝 mapping_index.md
│   ├── 📝 mapping_plan1_auth.md
│   ├── 📝 mapping_plan2_school_roles.md
│   ├── 📝 mapping_plan3_school_features.md
│   ├── 📝 mapping_plan4_school_ops.md
│   ├── 📝 mapping_plan5_college.md
│   ├── 📝 mapping_plan6_super_admin.md
│   ├── 📝 mapping_plan7_web_routes.md
│   ├── 📝 migration_phase1.md
│   ├── 📝 migration_phase2.md
│   ├── 📝 migration_phase3.md
│   ├── 📝 migration_phase4.md
│   ├── 📝 migration_phase5.md
│   ├── 📝 migration_phase6.md
│   ├── 📝 migration_phase7.md
│   ├── 📝 migration_phase8.md
│   ├── 📝 migration_plan.md
│   ├── 📝 missingplan1.md
│   ├── 📝 missingplan2.md
│   ├── 📝 missingplan3.md
│   ├── 📝 missingplan4.md
│   ├── 📝 missingplan5.md
│   ├── 📝 missingplan6.md
│   ├── 📝 missingplan7.md
│   ├── 📝 missingplan8.md
│   ├── 📝 new_structure.md
│   ├── 📝 phase1_implementation_breakdown.md
│   ├── 📝 phase2_implementation_breakdown.md
│   ├── 📝 phase3_implementation_breakdown.md
│   ├── 📝 phase4_implementation_breakdown.md
│   ├── 📝 phase5_implementation_breakdown.md
│   ├── 📝 plan_1_fix_faculty_import.md
│   ├── 📝 plan_2_update_routers_db.md
│   ├── 📝 plan_3_fix_relationship_conflicts.md
│   ├── 📝 plan_4_test_college_signup.md
│   ├── 📝 plan_5_create_frontend_pages.md
│   ├── 📝 plan_6_portal_guard_testing.md
│   ├── 📝 plan_7_final_review.md
│   ├── 📝 school.md
│   ├── 📝 school_account_section_migration_plan.md
│   ├── 📝 school_analytics_migration_plan.md
│   ├── 📝 school_assignments_migration_plan.md
│   ├── 📝 school_attendance_migration_plan.md
│   ├── 📝 school_authority_migration_plan.md
│   ├── 📝 school_chat_migration_plan.md
│   ├── 📝 school_chat_section_migration_plan.md
│   ├── 📝 school_collage_structure.md
│   ├── 📝 school_courses_migration_plan.md
│   ├── 📝 school_dashboard_migration_plan.md
│   ├── 📝 school_exam_section_migration_plan.md
│   ├── 📝 school_fee_structure_migration_plan.md
│   ├── 📝 school_fees_migration_plan.md
│   ├── 📝 school_grades_migration_plan.md
│   ├── 📝 school_group_section_migration_plan.md
│   ├── 📝 school_groups_migration_plan.md
│   ├── 📝 school_library_migration_plan.md
│   ├── 📝 school_notes_migration_plan.md
│   ├── 📝 school_notices_migration_plan.md
│   ├── 📝 school_parent_migration_plan.md
│   ├── 📝 school_reports_migration_plan.md
│   ├── 📝 school_student_migration_plan.md
│   ├── 📝 school_teacher_migration_plan.md
│   ├── 📝 school_tests_migration_plan.md
│   ├── 📝 school_timetable_migration_plan.md
│   ├── 📝 school_videos_migration_plan.md
│   ├── 📝 separate_database_architecture1.md
│   ├── 📝 separate_database_architecture2.md
│   └── 📝 transformation_status.md
├── 📂 rules/
│   ├── 📝 coding_rules.md
│   ├── 📝 frontend_react_rules.md
│   └── 📝 moving_code_rules.md
├── 📜 scripts/
│   ├── 📂 check/
│   │   ├── 🐍 check_db_enum.py
│   │   ├── 🐍 check_db_teachers.py
│   │   ├── 🐍 check_enum.py
│   │   ├── 🐍 check_enum_values.py
│   │   ├── 🐍 check_integrity.py
│   │   ├── 🐍 check_local_db.py
│   │   ├── 🐍 check_role_type.py
│   │   ├── 🐍 check_schema.py
│   │   ├── 🐍 check_test.py
│   │   ├── 🐍 check_users.py
│   │   ├── 🐍 list_courses.py
│   │   ├── 🐍 list_users.py
│   │   ├── 🐍 raw_list_courses.py
│   │   ├── 🐍 raw_list_users.py
│   │   ├── 🐍 test_auth.py
│   │   └── 🐍 test_teacher_lookup.py
│   ├── 📂 debug/
│   │   ├── 🐍 debug_access.py
│   │   ├── 🐍 debug_enrollments.py
│   │   ├── 🐍 debug_teacher_repo.py
│   │   ├── 🐍 debug_test_questions.py
│   │   ├── 🐍 debug_tests.py
│   │   ├── 🐍 debug_visibility.py
│   │   ├── 🐍 final_debug.py
│   │   └── 🐍 simple_debug.py
│   ├── 📂 fix/
│   │   ├── 🐍 fix_authority_urls.py
│   │   ├── 🐍 fix_imports_bulk.py
│   │   ├── 🐍 fix_main.py
│   │   ├── 🐍 fix_null_bytes.py
│   │   ├── 🐍 fix_student_urls.py
│   │   └── 🐍 inject_csrf.py
│   ├── 🗃️ migrations/
│   │   ├── 🐍 add_admin_role.py
│   │   ├── 🐍 add_admin_security_tables.py
│   │   ├── 📄 add_name_columns.sql
│   │   ├── 🐍 add_parent_id_to_students.py
│   │   ├── 📄 add_parent_to_enum.sql
│   │   ├── 🐍 add_target_classes_column.py
│   │   ├── 🐍 drop_column.py
│   │   ├── 🐍 migrate_attendance.py
│   │   ├── 🐍 migrate_grades.py
│   │   ├── 🐍 migrate_profile_pic.py
│   │   ├── 🐍 migrate_role_modules.py
│   │   ├── 🐍 migrations_add_messages.py
│   │   └── 🐍 run_add_name_migration.py
│   ├── 📂 setup/
│   │   ├── 🐍 add_parent_enum.py
│   │   ├── 🐍 create_assignment_test_data.py
│   │   ├── 🐍 create_messages_table.py
│   │   ├── 🐍 create_signup_student.py
│   │   ├── 🐍 create_test_parent.py
│   │   ├── 🐍 create_test_users.py
│   │   ├── 🐍 create_user.py
│   │   ├── 🐍 seed_courses.py
│   │   ├── 🐍 seed_features.py
│   │   └── 🐍 setup_database.py
│   ├── 📂 temp/
│   │   ├── 🐍 authority_routes_complete.py
│   │   ├── 📄 fail_output.txt
│   │   ├── 📄 main.py.backup
│   │   ├── 🐍 reproduce_enum.py
│   │   ├── 📄 routes.txt
│   │   ├── 🐍 temp_routes.py
│   │   ├── 🐍 temp_routes_2.py
│   │   ├── 🐍 temp_routes_3.py
│   │   ├── 📄 test_output.txt
│   │   └── 📄 test_output_2.txt
│   ├── 🔧 utils/
│   │   └── 🐍 generate_tree.py
│   ├── 📂 verify/
│   │   ├── 🐍 debug_filter.py
│   │   ├── 🐍 inspect_routes.py
│   │   ├── 🐍 verify_authority_search.py
│   │   ├── 🐍 verify_cleanup.py
│   │   ├── 🐍 verify_endpoints.py
│   │   ├── 🐍 verify_fix.py
│   │   └── 🐍 verify_groups.py
│   ├── 🐍 benchmark.py
│   ├── 🐍 check_alerts.py
│   ├── 🐍 check_db_enum.py
│   ├── 🐍 check_enum.py
│   ├── 🐍 check_hod.py
│   ├── 🐍 check_special_roles.py
│   ├── 🐍 check_user.py
│   ├── 🐍 compare_benchmarks.py
│   ├── 🐍 create_db_temp.py
│   ├── 🐍 create_special_users.py
│   ├── 🐍 data_inventory.py
│   ├── 📄 debug_output.txt
│   ├── 🐍 debug_signup.py
│   ├── 🐍 detect_n_plus_one.py
│   ├── 🐍 e2e_walkthrough.py
│   ├── 🐍 fix_db.py
│   ├── 🐍 list_tables.py
│   ├── 🐍 locustfile.py
│   ├── 🐍 reset_alembic.py
│   ├── 🐍 rollback.py
│   ├── 🐍 setup_new_roles.py
│   ├── 🐍 simulate_login.py
│   ├── 🐍 test_db_debug.py
│   ├── 🐍 test_signups.py
│   ├── 🐍 update_college_models.py
│   ├── 🐍 update_db_enum.py
│   ├── 🐍 verify_changes.py
│   ├── 🐍 verify_dashboards_v2.py
│   ├── 🐍 verify_login_page.py
│   └── 🐍 verify_schema.py
├── 🧪 tests/
│   ├── 🐍 conftest.py
│   ├── 📝 frontend_portal_guard_manual.md
│   ├── 🐍 test_add_course.py
│   ├── 🐍 test_add_student_form.py
│   ├── 🐍 test_auth_api_only.py
│   ├── 🐍 test_auth_fix.py
│   ├── 🐍 test_authority_routes.py
│   ├── 🐍 test_bcrypt.py
│   ├── 🐍 test_chat_simple.py
│   ├── 🐍 test_course_search.py
│   ├── 🐍 test_delete_route.py
│   ├── 🐍 test_fee_structure.py
│   ├── 🐍 test_login_signup.py
│   ├── 🐍 test_name_fields.py
│   ├── 🐍 test_parent_all_teachers.py
│   ├── 🐍 test_parent_chat.py
│   ├── 🐍 test_parent_dashboard.py
│   ├── 🐍 test_parent_endpoints.py
│   ├── 🐍 test_parent_teacher_chat.py
│   ├── 🐍 test_portal_guard.py
│   ├── 🐍 test_refresh_flow.py
│   ├── 🐍 test_signup_api.py
│   ├── 🐍 test_student_auth.py
│   ├── 🐍 test_student_routes.py
│   ├── 🐍 test_teacher_chat.py
│   ├── 🐍 test_teacher_search.py
│   └── 🐍 test_web_basic.py
├── 📄 .env
├── 📄 .gitignore
├── 📄 Dockerfile
├── 📝 FINAL_REVIEW_COMPLETE.md
├── 📝 README.md
├── ⚙️ alembic.ini
├── ⚙️ alembic_college.ini
├── 🐍 best_structure.py
├── 📄 build.sh
├── 🐍 capture_server_log.py
├── 🐍 capture_uvicorn.py
├── 🐍 capture_warnings.py
├── 🐍 capture_warnings2.py
├── 🐍 check_assign_indent.py
├── 🐍 check_college_db.py
├── 🐍 check_notes2.py
├── 🐍 check_notes_indent.py
├── 🐍 check_videos.py
├── 🐍 check_warnings.py
├── 🐍 check_warnings2.py
├── 🐍 clean_db.py
├── 🐍 count_spaces.py
├── 🐍 create_college_tables.py
├── 🐍 direct_test.py
├── 🧾 docker-compose.yml
├── 🐍 final_test.py
├── 🐍 fix_all_indents.py
├── 🐍 fix_indent.py
├── 📄 login_trace.txt
├── 📄 login_trace_utf8.txt
├── 🐍 main.py
├── 📄 makefile
├── 📝 model_run.md
├── 🐍 model_run.py
├── 📄 output.txt
├── 📄 plan_to_do.txt
├── 📝 project_detail_emplimenting_plan.md
├── ⚙️ pytest.ini
├── 🐍 quick_test.py
├── 🧾 render.yaml
├── 📄 requirements.txt
├── 🐍 run.py
├── 🐍 run_with_log.py
├── 📄 school_db.sqlite
├── 🐍 seed.py
├── 📜 server_error.log
├── 📄 server_startup_log.txt
├── 🐍 show_indent.py
├── 🐍 start_and_test.py
├── 🐍 start_test.py
├── 🐍 temp_index.py
├── 🐍 temp_migrate.py
├── 🐍 test_all_college_models.py
├── 🐍 test_all_models.py
├── 🐍 test_all_school_models.py
├── 🐍 test_app_import.py
├── 🐍 test_college_course_import.py
├── 🐍 test_college_course_import2.py
├── 🐍 test_college_only.py
├── 🐍 test_college_only2.py
├── 🐍 test_college_signup.py
├── 🐍 test_college_signup_final.py
├── 🐍 test_configure.py
├── 🐍 test_dept_dup.py
├── 🐍 test_duplicate.py
├── 🐍 test_faculty_import.py
├── 🐍 test_import_backup_student.py
├── 🐍 test_overlaps.py
├── 🐍 test_overlaps_warnings.py
├── 📄 test_run_log.txt
├── 🐍 test_sa_warning.py
├── 🐍 test_sa_warning2.py
├── 🐍 test_with_testclient.py
├── 📜 uvicorn_output.log
├── 🐍 verify_app.py
├── 🐍 verify_college_tables.py
└── 🐍 verify_data.py
