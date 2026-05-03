import api from '../../../shared/api/client';

// Get HOD profile
export const getProfile = () => {
  return api.get('/hod/profile');
};

// Get department teachers
export const getDepartmentTeachers = () => {
  return api.get('/hod/teachers');
};

// Get department students
export const getDepartmentStudents = () => {
  return api.get('/hod/students');
};

// Get student performance
export const getStudentPerformance = (studentId) => {
  return api.get(`/hod/students/${studentId}/performance`);
};

// Get department reports
export const getReports = () => {
  return api.get('/hod/reports');
};

// Get department courses
export const getCourses = () => {
  return api.get('/hod/courses');
};

// Get attendance overview
export const getAttendanceOverview = () => {
  return api.get('/hod/attendance');
};

// Get dashboard stats
export const getDashboardStats = () => {
  return api.get('/school/dashboard');
};

// ============================================
// NEW: Extended HOD Management
// ============================================

export const getDepartmentPerformance = () => api.get('/hod/performance');
export const getTeacherPerformance = (teacherId) => api.get(`/hod/teachers/${teacherId}/performance`);
export const getCourseAnalytics = (courseId) => api.get(`/hod/courses/${courseId}/analytics`);
export const getDepartmentAttendance = () => api.get('/hod/attendance/overview');
export const getDepartmentGrades = () => api.get('/hod/grades/overview');
export const assignCourse = (data) => api.post('/hod/courses/assign', data);
export const removeCourse = (courseId, teacherId) => api.delete(`/hod/courses/${courseId}/teacher/${teacherId}`);
export const getDepartmentTimetable = () => api.get('/hod/timetable');
export const getTeacherSchedule = (teacherId) => api.get(`/hod/teachers/${teacherId}/schedule`);
export const approveLeave = (leaveId) => api.put(`/hod/leave/${leaveId}/approve`);
export const rejectLeave = (leaveId, reason) => api.put(`/hod/leave/${leaveId}/reject`, { reason });
export const getLeaveRequests = () => api.get('/hod/leave-requests');
export const getStudentList = (courseId) => api.get(`/hod/courses/${courseId}/students`);
export const getDepartmentExams = () => api.get('/hod/exams');
export const getExamSchedule = () => api.get('/hod/exams/schedule');
export const generateDepartmentReport = (type) => api.get(`/hod/reports/${type}`);
