import api from '../../../shared/api/client';

/**
 * Teacher API Service
 * Updated to match the modular FastAPI backend /api/v1/teachers/ structure.
 */

// =====================
// EXISTING API ENDPOINTS
// =====================

export const getMyTeacherProfile = () => api.get('/teachers/me');
export const getTeacherCourses = () => api.get('/teachers/my-courses');
export const getTeacherStudents = () => api.get('/teachers/my-students');
export const getTeacherAssignments = () => api.get('/teachers/my-assignments');
export const getTeacherTests = () => api.get('/teachers/my-tests');
export const getTeacherDashboard = () => api.get('/teachers/dashboard');
export const createAssignment = (data) => api.post('/assignments/', data);
export const createTest = (data) => api.post('/tests/', data);
export const getTeacherProfile = () => api.get('/teachers/me');
export const updateTeacherProfile = (data) => api.put('/teachers/me', data);
export const getTeacherGrades = (courseId) => api.get(`/grades/teacher/course/${courseId}`);
export const addGrade = (data) => api.post('/grades/', data);
export const updateGrade = (gradeId, data) => api.put(`/grades/${gradeId}`, data);
export const getAttendanceSessions = (courseId) => api.get(`/attendance/teacher/course/${courseId}`);
export const createAttendanceSession = (data) => api.post('/attendance/', data);
export const recordAttendance = (sessionId, data) => api.post(`/attendance/${sessionId}/record`, data);
export const getAttendanceDetails = (sessionId) => api.get(`/attendance/${sessionId}`);
export const getMyAttendanceRecords = () => api.get('/teachers/my-attendance');
export const getMyTimetable = () => api.get('/teachers/my-timetable');
export const getAssignment = (id) => api.get(`/assignments/${id}`);
export const updateAssignment = (id, data) => api.put(`/assignments/${id}`, data);
export const deleteAssignment = (id) => api.delete(`/assignments/${id}`);
export const getSubmissions = (assignmentId) => api.get(`/assignments/${assignmentId}/submissions`);
export const getTest = (id) => api.get(`/tests/${id}`);
export const updateTest = (id, data) => api.put(`/tests/${id}`, data);
export const deleteTest = (id) => api.delete(`/tests/${id}`);
export const getTestSubmissions = (testId) => api.get(`/tests/${testId}/submissions`);
export const getTeacherNotices = () => api.get('/notices/teacher');
export const createTeacherNotice = (data) => api.post('/notices/', data);
export const updateTeacherNotice = (id, data) => api.put(`/notices/${id}`, data);
export const deleteTeacherNotice = (id) => api.delete(`/notices/${id}`);
export const getTeacherGroups = () => api.get('/groups/teacher');
export const getTeacherMessages = () => api.get('/messages/teacher');
export const sendMessage = (data) => api.post('/messages/', data);
export const getTeacherNotes = () => api.get('/notes/teacher');
export const uploadNote = (data) => api.post('/notes/', data, { headers: { 'Content-Type': 'multipart/form-data' } });
export const deleteNote = (id) => api.delete(`/notes/${id}`);
export const getTeacherVideos = () => api.get('/videos/teacher');
export const uploadVideo = (data) => api.post('/videos/', data, { headers: { 'Content-Type': 'multipart/form-data' } });
export const deleteVideo = (id) => api.delete(`/videos/${id}`);
export const getStudentDetails = (studentId) => api.get(`/students/${studentId}`);
export const getStudentAcademicHistory = (studentId) => api.get(`/students/${studentId}/grades`);
export const getStudentGrades = (studentId) => api.get(`/students/${studentId}/grades`);
export const getTeacherTimetable = () => api.get('/teachers/my-timetable');

// =====================
// NEW API ENDPOINTS (from Plan 2)
// =====================

// Teacher Profile
export const getTeacherById = (teacherId) => api.get(`/teachers/${teacherId}`);
export const updateTeacher = (teacherId, data) => api.put(`/teachers/${teacherId}`, data);

// Teacher Courses
export const getMyCourses = () => api.get('/courses/teacher/my');
export const updateCourse = (courseId, data) => api.put(`/courses/${courseId}`, data);
export const deleteCourse = (courseId) => api.delete(`/courses/${courseId}`);

// Teacher Grades
export const createGrade = (data) => api.post('/grades/', data);
export const createBulkGrades = (grades) => api.post('/grades/bulk', { grades });
export const deleteGrade = (gradeId) => api.delete(`/grades/${gradeId}`);
export const getCourseGrades = (courseId) => api.get(`/grades/course/${courseId}`);

// Teacher Attendance
export const getAttendanceRecords = (courseId) => api.get('/attendance/records', { params: { course_id: courseId } });
export const getCourseAttendance = (courseId) => api.get(`/attendance/course/${courseId}`);
export const getCourseAttendanceStats = (courseId) => api.get(`/attendance/course/${courseId}/stats`);
export const bulkMarkAttendance = (data) => api.post('/attendance/bulk', data);

// Teacher Assignments
export const getMyAssignments = () => api.get('/assignments/teacher/my-assignments');
export const getAssignmentSubmissions = (assignmentId) => api.get(`/assignments/${assignmentId}/submissions`);
export const gradeSubmission = (submissionId, data) => api.put(`/assignments/submissions/${submissionId}/grade`, data);

// Teacher Tests
export const getMyTests = () => api.get('/tests/teacher/my-tests');
export const getTestForTeacher = (testId) => api.get(`/tests/teacher/${testId}`);
export const getTestResults = (testId) => api.get(`/tests/${testId}/results`);

// Teacher Timetable
export const getTeacherTimetableById = (teacherId) => api.get(`/timetable/teacher/${teacherId}`);

// Teacher Videos
export const getMyVideos = () => api.get('/videos/teacher/my-videos');

// Teacher Notes
export const getMyNotes = () => api.get('/notes/teacher/my-notes');
