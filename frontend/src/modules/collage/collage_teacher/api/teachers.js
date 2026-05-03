import api from '../../../shared/api/client';

export const getTeachers = () => api.get('/school/teachers/');
export const getMyTeacherProfile = () => api.get('/school/teachers/me');

// ============================================
// NEW: Extended College Teacher API
// ============================================

export const getMyCourses = () => api.get('/college/courses/my');
export const getCourseStudents = (courseId) => api.get(`/college/courses/${courseId}/students`);
export const getAttendance = (courseId, date) => api.get(`/college/courses/${courseId}/attendance`, { params: { date } });
export const markAttendance = (courseId, data) => api.post(`/college/courses/${courseId}/attendance`, data);
export const getGrades = (courseId) => api.get(`/college/courses/${courseId}/grades`);
export const submitGrades = (courseId, data) => api.post(`/college/courses/${courseId}/grades`, data);
export const getAssignments = (courseId) => api.get(`/college/courses/${courseId}/assignments`);
export const createAssignment = (data) => api.post('/college/assignments', data);
export const gradeAssignment = (assignmentId, data) => api.put(`/college/assignments/${assignmentId}/grade`, data);
export const getResearchPapers = () => api.get('/college/research');
export const publishResearch = (data) => api.post('/college/research', data);
export const getPublications = () => api.get('/college/publications');
export const getTeachingSchedule = () => api.get('/college/schedule');
export const getLeaveRequests = () => api.get('/college/leave');
export const applyLeave = (data) => api.post('/college/leave', data);
