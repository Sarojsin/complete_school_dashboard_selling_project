import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import PrivateRoute from './modules/shared/components/PrivateRoute';
import LoginPage from './modules/auth/pages/LoginPage';
import SignupPage from './modules/auth/pages/SignupPage';
import LandingPage from './modules/auth/pages/LandingPage';
import RegisterChoice from './modules/auth/pages/RegisterChoice';
import DashboardRedirector from './modules/auth/pages/DashboardRedirector';

// Teacher Portal
import TeacherDashboard from './modules/school/school_teacher/pages/TeacherDashboard';
import TeacherProfile from './modules/school/school_teacher/pages/TeacherProfile';
import TeacherGrades from './modules/school/school_teacher/pages/TeacherGrades';
import TeacherAttendance from './modules/school/school_teacher/pages/TeacherAttendance';
import CreateAssignment from './modules/school/school_teacher/pages/CreateAssignment';
import TeacherViewSubmissions from './modules/school/school_teacher/pages/TeacherViewSubmissions';
import TeacherCreateTest from './modules/school/school_teacher/pages/TeacherCreateTest';
import TeacherStudentDetail from './modules/school/school_teacher/pages/TeacherStudentDetail';
import TeacherTimetable from './modules/school/school_teacher/pages/TeacherTimetable';
import TeacherNotices from './modules/school/school_teacher/pages/TeacherNotices';
import TeacherGroups from './modules/school/school_teacher/pages/TeacherGroups';
import TeacherAddGrade from './modules/school/school_teacher/pages/TeacherAddGrade';
import TeacherEditAssignment from './modules/school/school_teacher/pages/TeacherEditAssignment';
import TeacherEditTest from './modules/school/school_teacher/pages/TeacherEditTest';
import TeacherTakeAttendance from './modules/school/school_teacher/pages/TeacherTakeAttendance';
import TeacherUploadNotes from './modules/school/school_teacher/pages/TeacherUploadNotes';
import TeacherUploadVideos from './modules/school/school_teacher/pages/TeacherUploadVideos';
import TeacherCourseDetail from './modules/school/school_teacher/pages/TeacherCourseDetail';

// Student Portal
import StudentDashboard from './modules/school/school_student/pages/StudentDashboard';
import StudentProfile from './modules/school/school_student/pages/StudentProfile';
import Assignments from './modules/school/school_student/pages/Assignments';
import Attendance from './modules/school/school_student/pages/Attendance';
import Courses from './modules/school/school_student/pages/Courses';
import Grades from './modules/school/school_student/pages/Grades';
import Notices from './modules/school/school_student/pages/Notices';
import StudentFees from './modules/school/school_student/pages/StudentFees';
import StudentTeachers from './modules/school/school_student/pages/StudentTeachers';
import TestList from './modules/school/school_student/pages/TestList';
import ExamResults from './modules/school/school_student/pages/ExamResults';

// Groups Portal
import GroupList from './modules/school/school_groups/pages/GroupList';
import GroupDetail from './modules/school/school_groups/pages/GroupDetail';
import GroupEdit from './modules/school/school_groups/pages/GroupEdit';
import GroupPosts from './modules/school/school_groups/pages/GroupPosts';
import NewPost from './modules/school/school_groups/pages/NewPost';
import ViewPost from './modules/school/school_groups/pages/ViewPost';
import GroupManageMembers from './modules/school/school_groups/pages/GroupManageMembers';
import CreateGroup from './modules/school/school_groups/pages/CreateGroup';

// HOD Portal
import HODDashboard from './modules/school/school_hod/pages/HODDashboard';
import HODProfile from './modules/school/school_hod/pages/HODProfile';

// Parent Portal
import ParentDashboard from './modules/school/school_parent/pages/ParentDashboard';
import ParentProfile from './modules/school/school_parent/pages/ParentProfile';
import ParentNotices from './modules/school/school_parent/pages/ParentNotices';
import ChildGrades from './modules/school/school_parent/pages/ChildGrades';
import ChildAttendance from './modules/school/school_parent/pages/ChildAttendance';
import ParentChat from './modules/school/school_parent/pages/ParentChat';
import ParentHomework from './modules/school/school_parent/pages/ParentHomework';
import ChildFees from './modules/school/school_parent/pages/ChildFees';

// Authority Portal
import AuthorityDashboard from './modules/school/school_authority/pages/AuthorityDashboard';
import StudentsManagement from './modules/school/school_authority/pages/Students';
import TeachersManagement from './modules/school/school_authority/pages/Teachers';
import AdminFees from './modules/school/school_authority/pages/AdminFees';
import AdminAnalytics from './modules/school/school_authority/pages/AdminAnalytics';

// Account Section
import AccountDashboard from './modules/school/school_account_section/pages/AccountDashboard';

// Exam Section
import ExamDashboard from './modules/school/school_exam_section/pages/ExamDashboard';
import ExamGradeSheet from './modules/school/school_exam_section/pages/ExamGradeSheet';
import ExamPostResult from './modules/school/school_exam_section/pages/ExamPostResult';
import ExamNotices from './modules/school/school_exam_section/pages/ExamNotices';

// Super Admin
import SuperAdminDashboard from './modules/super_admin/pages/SuperAdminDashboard';
import Academic from './modules/super_admin/pages/Academic';
import Advanced from './modules/super_admin/pages/Advanced';
import AuditLogs from './modules/super_admin/pages/AuditLogs';
import Backups from './modules/super_admin/pages/Backups';
import Communication from './modules/super_admin/pages/Communication';
import Features from './modules/super_admin/pages/Features';
import Finance from './modules/super_admin/pages/Finance';
import Media from './modules/super_admin/pages/Media';
import Security from './modules/super_admin/pages/Security';
import Settings from './modules/super_admin/pages/Settings';
import System from './modules/super_admin/pages/System';
import Users from './modules/super_admin/pages/Users';
import AdminNotices from './modules/super_admin/pages/AdminNotices';
import FeatureDetail from './modules/super_admin/pages/FeatureDetail';
import Reports from './modules/super_admin/pages/Reports';

// College Teacher Portal
import CollegeTeacherDashboard from './modules/collage/collage_teacher/pages/TeacherDashboard';

// College Placement Portal
import CollegePlacementStudentDashboard from './modules/collage/collage_placement/pages/StudentDashboard';

// College HOD Portal
import CollegeHODDashboard from './modules/college/college_hod/pages/HODDashboard';

// College Dean Portal
import CollegeDeanDashboard from './modules/college/college_dean/pages/DeanDashboard';

// College Registrar Portal
import CollegeRegistrarDashboard from './modules/college/college_registrar/pages/RegistrarDashboard';

// College Exam Section Portal
import CollegeExamDashboard from './modules/college/college_exam_section/pages/ExamDashboard';

// College Account Section Portal
import CollegeAccountDashboard from './modules/college/college_account_section/pages/AccountDashboard';

// College Library Portal
import CollegeLibraryDashboard from './modules/college/college_library/pages/LibraryDashboard';

// College Lab Portal
import CollegeLabDashboard from './modules/college/college_lab/pages/LabDashboard';

// College Hostel Portal
import CollegeHostelDashboard from './modules/college/college_hostel/pages/HostelDashboard';

// College Research Portal
import CollegeResearchDashboard from './modules/college/college_research/pages/ResearchDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<SignupPage />} />
        <Route path="/register-choice" element={<RegisterChoice />} />
        <Route path="/dashboard" element={<PrivateRoute><DashboardRedirector /></PrivateRoute>} />
        
        <Route 
          path="/teacher/dashboard" 
          element={
            <PrivateRoute allowedPortal="school">
              <TeacherDashboard />
            </PrivateRoute>
          } 
        />
        
        <Route 
          path="/student/dashboard" 
          element={
            <PrivateRoute allowedPortal="school">
              <StudentDashboard />
            </PrivateRoute>
          } 
        />
        
        {/* Student Portal Routes */}
        <Route path="/student/profile" element={<PrivateRoute allowedPortal="school"><StudentProfile /></PrivateRoute>} />
        <Route path="/student/assignments" element={<PrivateRoute allowedPortal="school"><Assignments /></PrivateRoute>} />
        <Route path="/student/attendance" element={<PrivateRoute allowedPortal="school"><Attendance /></PrivateRoute>} />
        <Route path="/student/courses" element={<PrivateRoute allowedPortal="school"><Courses /></PrivateRoute>} />
        <Route path="/student/grades" element={<PrivateRoute allowedPortal="school"><Grades /></PrivateRoute>} />
        <Route path="/student/notices" element={<PrivateRoute allowedPortal="school"><Notices /></PrivateRoute>} />
        <Route path="/student/fees" element={<PrivateRoute allowedPortal="school"><StudentFees /></PrivateRoute>} />
        <Route path="/student/teachers" element={<PrivateRoute allowedPortal="school"><StudentTeachers /></PrivateRoute>} />
        <Route path="/student/tests" element={<PrivateRoute allowedPortal="school"><TestList /></PrivateRoute>} />
        <Route path="/student/exam-results" element={<PrivateRoute allowedPortal="school"><ExamResults /></PrivateRoute>} />
        
        {/* Teacher Portal Routes */}
        <Route path="/teacher/profile" element={<PrivateRoute allowedPortal="school"><TeacherProfile /></PrivateRoute>} />
        <Route path="/teacher/grades" element={<PrivateRoute allowedPortal="school"><TeacherGrades /></PrivateRoute>} />
        <Route path="/teacher/attendance" element={<PrivateRoute allowedPortal="school"><TeacherAttendance /></PrivateRoute>} />
        <Route path="/teacher/create-assignment" element={<PrivateRoute allowedPortal="school"><CreateAssignment /></PrivateRoute>} />
        <Route path="/teacher/assignments/:assignmentId" element={<PrivateRoute allowedPortal="school"><CreateAssignment /></PrivateRoute>} />
        <Route path="/teacher/edit-assignment/:assignmentId" element={<PrivateRoute allowedPortal="school"><TeacherEditAssignment /></PrivateRoute>} />
        <Route path="/teacher/view-submissions" element={<PrivateRoute allowedPortal="school"><TeacherViewSubmissions /></PrivateRoute>} />
        <Route path="/teacher/create-test" element={<PrivateRoute allowedPortal="school"><TeacherCreateTest /></PrivateRoute>} />
        <Route path="/teacher/edit-test/:testId" element={<PrivateRoute allowedPortal="school"><TeacherEditTest /></PrivateRoute>} />
        <Route path="/teacher/student/:studentId" element={<PrivateRoute allowedPortal="school"><TeacherStudentDetail /></PrivateRoute>} />
        <Route path="/teacher/timetable" element={<PrivateRoute allowedPortal="school"><TeacherTimetable /></PrivateRoute>} />
        <Route path="/teacher/notices" element={<PrivateRoute allowedPortal="school"><TeacherNotices /></PrivateRoute>} />
        <Route path="/teacher/groups" element={<PrivateRoute allowedPortal="school"><TeacherGroups /></PrivateRoute>} />
        <Route path="/teacher/add-grade" element={<PrivateRoute allowedPortal="school"><TeacherAddGrade /></PrivateRoute>} />
        <Route path="/teacher/add-grade/:courseId" element={<PrivateRoute allowedPortal="school"><TeacherAddGrade /></PrivateRoute>} />
        <Route path="/teacher/take-attendance" element={<PrivateRoute allowedPortal="school"><TeacherTakeAttendance /></PrivateRoute>} />
        <Route path="/teacher/take-attendance/:courseId" element={<PrivateRoute allowedPortal="school"><TeacherTakeAttendance /></PrivateRoute>} />
        <Route path="/teacher/upload-notes" element={<PrivateRoute allowedPortal="school"><TeacherUploadNotes /></PrivateRoute>} />
        <Route path="/teacher/upload-videos" element={<PrivateRoute allowedPortal="school"><TeacherUploadVideos /></PrivateRoute>} />
        <Route path="/teacher/courses/:courseId" element={<PrivateRoute allowedPortal="school"><TeacherCourseDetail /></PrivateRoute>} />
        <Route path="/teacher/courses" element={<PrivateRoute allowedPortal="school"><TeacherDashboard /></PrivateRoute>} />
        <Route path="/teacher/students" element={<PrivateRoute allowedPortal="school"><TeacherDashboard /></PrivateRoute>} />
        <Route path="/teacher/view-tests" element={<PrivateRoute allowedPortal="school"><TeacherDashboard /></PrivateRoute>} />
        <Route path="/teacher/messages" element={<PrivateRoute allowedPortal="school"><TeacherDashboard /></PrivateRoute>} />
        <Route path="/teacher/chat" element={<PrivateRoute allowedPortal="school"><TeacherDashboard /></PrivateRoute>} />
        
        {/* Groups Portal Routes */}
        <Route path="/groups" element={<PrivateRoute allowedPortal="school"><GroupList /></PrivateRoute>} />
        <Route path="/groups/create" element={<PrivateRoute allowedPortal="school"><CreateGroup /></PrivateRoute>} />
        <Route path="/groups/:groupId" element={<PrivateRoute allowedPortal="school"><GroupDetail /></PrivateRoute>} />
        <Route path="/groups/:groupId/edit" element={<PrivateRoute allowedPortal="school"><GroupEdit /></PrivateRoute>} />
        <Route path="/groups/:groupId/posts" element={<PrivateRoute allowedPortal="school"><GroupPosts /></PrivateRoute>} />
        <Route path="/groups/:groupId/posts/new" element={<PrivateRoute allowedPortal="school"><NewPost /></PrivateRoute>} />
        <Route path="/groups/:groupId/posts/:postId" element={<PrivateRoute allowedPortal="school"><ViewPost /></PrivateRoute>} />
        <Route path="/groups/:groupId/members" element={<PrivateRoute allowedPortal="school"><GroupManageMembers /></PrivateRoute>} />
        
        {/* HOD Portal Routes */}
        <Route path="/hod/dashboard" element={<PrivateRoute allowedPortal="school"><HODDashboard /></PrivateRoute>} />
        <Route path="/hod/profile" element={<PrivateRoute allowedPortal="school"><HODProfile /></PrivateRoute>} />
        <Route path="/hod" element={<PrivateRoute allowedPortal="school"><HODDashboard /></PrivateRoute>} />
        
        {/* Parent Portal Routes */}
        <Route path="/parent/dashboard" element={<PrivateRoute allowedPortal="school"><ParentDashboard /></PrivateRoute>} />
        <Route path="/parent/profile" element={<PrivateRoute allowedPortal="school"><ParentProfile /></PrivateRoute>} />
        <Route path="/parent/notices" element={<PrivateRoute allowedPortal="school"><ParentNotices /></PrivateRoute>} />
        <Route path="/parent/grades" element={<PrivateRoute allowedPortal="school"><ChildGrades /></PrivateRoute>} />
        <Route path="/parent/attendance" element={<PrivateRoute allowedPortal="school"><ChildAttendance /></PrivateRoute>} />
        <Route path="/parent/chat" element={<PrivateRoute allowedPortal="school"><ParentChat /></PrivateRoute>} />
        <Route path="/parent/homework" element={<PrivateRoute allowedPortal="school"><ParentHomework /></PrivateRoute>} />
        <Route path="/parent/fees" element={<PrivateRoute allowedPortal="school"><ChildFees /></PrivateRoute>} />
        
        {/* Authority Portal Routes */}
        <Route path="/authority/dashboard" element={<PrivateRoute allowedPortal="school"><AuthorityDashboard /></PrivateRoute>} />
        <Route path="/authority/students" element={<PrivateRoute allowedPortal="school"><StudentsManagement /></PrivateRoute>} />
        <Route path="/authority/teachers" element={<PrivateRoute allowedPortal="school"><TeachersManagement /></PrivateRoute>} />
        <Route path="/authority/fees" element={<PrivateRoute allowedPortal="school"><AdminFees /></PrivateRoute>} />
        <Route path="/authority/analytics" element={<PrivateRoute allowedPortal="school"><AdminAnalytics /></PrivateRoute>} />
        <Route path="/authority" element={<PrivateRoute allowedPortal="school"><AuthorityDashboard /></PrivateRoute>} />
        
        {/* Exam Section Routes */}
        <Route path="/exam/dashboard" element={<PrivateRoute allowedPortal="school"><ExamDashboard /></PrivateRoute>} />
        <Route path="/exam/grade-sheet" element={<PrivateRoute allowedPortal="school"><ExamGradeSheet /></PrivateRoute>} />
        <Route path="/exam/post-result" element={<PrivateRoute allowedPortal="school"><ExamPostResult /></PrivateRoute>} />
        <Route path="/exam/notices" element={<PrivateRoute allowedPortal="school"><ExamNotices /></PrivateRoute>} />
        <Route path="/exam" element={<PrivateRoute allowedPortal="school"><ExamDashboard /></PrivateRoute>} />
        
        {/* Account Section Routes */}
        <Route path="/account/dashboard" element={<PrivateRoute allowedPortal="school"><AccountDashboard /></PrivateRoute>} />
        <Route path="/account" element={<PrivateRoute allowedPortal="school"><AccountDashboard /></PrivateRoute>} />
        
        {/* Super Admin Routes */}
        <Route path="/admin/dashboard" element={<PrivateRoute allowedPortal="school"><SuperAdminDashboard /></PrivateRoute>} />
        <Route path="/admin/academic" element={<PrivateRoute allowedPortal="school"><Academic /></PrivateRoute>} />
        <Route path="/admin/advanced" element={<PrivateRoute allowedPortal="school"><Advanced /></PrivateRoute>} />
        <Route path="/admin/audit-logs" element={<PrivateRoute allowedPortal="school"><AuditLogs /></PrivateRoute>} />
        <Route path="/admin/backups" element={<PrivateRoute allowedPortal="school"><Backups /></PrivateRoute>} />
        <Route path="/admin/communication" element={<PrivateRoute allowedPortal="school"><Communication /></PrivateRoute>} />
        <Route path="/admin/features" element={<PrivateRoute allowedPortal="school"><Features /></PrivateRoute>} />
        <Route path="/admin/feature/:featureId" element={<PrivateRoute allowedPortal="school"><FeatureDetail /></PrivateRoute>} />
        <Route path="/admin/finance" element={<PrivateRoute allowedPortal="school"><Finance /></PrivateRoute>} />
        <Route path="/admin/media" element={<PrivateRoute allowedPortal="school"><Media /></PrivateRoute>} />
        <Route path="/admin/notices" element={<PrivateRoute allowedPortal="school"><AdminNotices /></PrivateRoute>} />
        <Route path="/admin/reports" element={<PrivateRoute allowedPortal="school"><Reports /></PrivateRoute>} />
        <Route path="/admin/security" element={<PrivateRoute allowedPortal="school"><Security /></PrivateRoute>} />
        <Route path="/admin/settings" element={<PrivateRoute allowedPortal="school"><Settings /></PrivateRoute>} />
        <Route path="/admin/system" element={<PrivateRoute allowedPortal="school"><System /></PrivateRoute>} />
        <Route path="/admin/users" element={<PrivateRoute allowedPortal="school"><Users /></PrivateRoute>} />
        <Route path="/admin" element={<PrivateRoute allowedPortal="school"><SuperAdminDashboard /></PrivateRoute>} />
        
        {/* ==================== COLLEGE PORTAL ROUTES ==================== */}
        
        {/* College Teacher Portal Routes */}
        <Route path="/college/teacher/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeTeacherDashboard /></PrivateRoute>} />
        
        {/* College Placement Portal Routes */}
        <Route path="/college/student/dashboard" element={<PrivateRoute allowedPortal="college"><CollegePlacementStudentDashboard /></PrivateRoute>} />

        {/* College HOD Portal Routes */}
        <Route path="/college/hod/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeHODDashboard /></PrivateRoute>} />

        {/* College Dean Portal Routes */}
        <Route path="/college/dean/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeDeanDashboard /></PrivateRoute>} />

        {/* College Registrar Portal Routes */}
        <Route path="/college/registrar/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeRegistrarDashboard /></PrivateRoute>} />

        {/* College Exam Section Portal Routes */}
        <Route path="/college/exam/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeExamDashboard /></PrivateRoute>} />

        {/* College Account Section Portal Routes */}
        <Route path="/college/account/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeAccountDashboard /></PrivateRoute>} />

        {/* College Library Portal Routes */}
        <Route path="/college/library/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeLibraryDashboard /></PrivateRoute>} />

        {/* College Lab Portal Routes */}
        <Route path="/college/lab/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeLabDashboard /></PrivateRoute>} />

        {/* College Hostel Portal Routes */}
        <Route path="/college/hostel/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeHostelDashboard /></PrivateRoute>} />

        {/* College Research Portal Routes */}
        <Route path="/college/research/dashboard" element={<PrivateRoute allowedPortal="college"><CollegeResearchDashboard /></PrivateRoute>} />
        
        {/* 404 Catch-All Route */}
        <Route path="*" element={<div style={{ padding: '2rem', textAlign: 'center', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(to bottom, #0f172a, #1e293b)' }}>
          <h1 style={{ fontSize: '4rem', fontWeight: 'bold', color: '#3b82f6', margin: 0 }}>404</h1>
          <h2 style={{ color: '#e2e8f0', marginTop: '1rem' }}>Page Not Found</h2>
          <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>The page you're looking for doesn't exist or has been moved.</p>
          <button onClick={() => window.history.back()} style={{ marginTop: '1.5rem', padding: '0.75rem 1.5rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '0.5rem', cursor: 'pointer', fontWeight: '500' }}>
            Go Back
          </button>
        </div>} />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;


