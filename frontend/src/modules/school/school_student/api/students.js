import api from '../../../shared/api/client';

const SCHOOL_API = '/school';

// =====================
// EXISTING API ENDPOINTS
// =====================

export const getMyStudentProfile = () => api.get(`${SCHOOL_API}/students/me`);

export const getStudentCourses = () => api.get(`${SCHOOL_API}/students/courses`);

export const getStudentGrades = () => api.get(`${SCHOOL_API}/students/grades`);

export const getStudentAttendance = () => api.get(`${SCHOOL_API}/students/attendance`);

export const getStudentAssignments = () => api.get(`${SCHOOL_API}/students/assignments`);

export const getStudentNotices = () => api.get(`${SCHOOL_API}/students/notices`);

export const getStudentTests = () => api.get(`${SCHOOL_API}/students/tests`);

export const getStudentDashboard = () => api.get(`${SCHOOL_API}/students/dashboard`);

// =====================
// NEW API ENDPOINTS
// =====================

// === PROFILE ENDPOINTS ===
export const getStudentById = (studentId) => api.get(`${SCHOOL_API}/students/${studentId}`);

export const updateStudent = (studentId, data) => api.put(`${SCHOOL_API}/students/${studentId}`, data);

export const deleteStudent = (studentId) => api.delete(`${SCHOOL_API}/students/${studentId}`);

// === COURSES ENDPOINTS ===
export const getEnrolledCourses = () => api.get(`${SCHOOL_API}/students/courses/enrolled`);

// === GRADES ENDPOINTS ===
export const getMyGrades = () => api.get(`${SCHOOL_API}/grades/my-grades`);

// === ATTENDANCE ENDPOINTS ===
export const getMyAttendance = () => api.get(`${SCHOOL_API}/attendance/student/my`);

export const getMyCourseAttendance = (courseId) => api.get(`${SCHOOL_API}/attendance/student/my/course/${courseId}`);

// === ASSIGNMENTS ENDPOINTS ===
export const submitAssignment = (assignmentId, data) => 
  api.post(`${SCHOOL_API}/assignments/${assignmentId}/submit`, data);

export const getMySubmission = (assignmentId) => 
  api.get(`${SCHOOL_API}/assignments/${assignmentId}/my-submission`);

// === TESTS ENDPOINTS ===
export const getAvailableTests = () => api.get(`${SCHOOL_API}/tests/student/available`);

export const getTestDetails = (testId) => api.get(`${SCHOOL_API}/tests/student/${testId}`);

export const startTest = (testId) => api.post(`${SCHOOL_API}/tests/${testId}/start`);

export const submitTest = (testId, answers) => 
  api.post(`${SCHOOL_API}/tests/${testId}/submit`, answers);

export const getTestResult = (testId) => api.get(`${SCHOOL_API}/tests/student/${testId}/result`);

export const getMyTestResults = () => api.get(`${SCHOOL_API}/tests/student/my-results`);

// === PROFILE UPDATE ===
export const updateMyProfile = (data) => api.patch(`${SCHOOL_API}/students/me`, data);
