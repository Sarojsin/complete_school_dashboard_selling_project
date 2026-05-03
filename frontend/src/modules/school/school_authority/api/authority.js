import api from '../../../shared/api/client';

/**
 * Authority API Service
 * Aligned with modular backend /api/v1/authorities/
 * With missing endpoints from Plan 3
 */

// Dashboard & Profile
export const getAuthorityDashboard = () => api.get('/authorities/dashboard');
export const getMyAuthorityProfile = () => api.get('/authorities/me');
export const updateAuthorityProfile = (data) => api.put('/authorities/me', data);

// Students Administration
export const getAdminStudents = (params) => api.get('/authorities/students', { params });
export const createAdminStudent = (data) => api.post('/authorities/students', data);
export const getStudentById = (id) => api.get(`/authorities/students/${id}`);
export const updateStudent = (id, data) => api.put(`/authorities/students/${id}`, data);
export const deleteStudent = (id) => api.delete(`/authorities/students/${id}`);
export const bulkCreateStudents = (data) => api.post('/authorities/students/bulk', data);
export const importStudentsFromFile = (formData) => api.post('/authorities/students/import', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const exportStudents = (params) => api.get('/authorities/students/export', { params, responseType: 'blob' });

// Teachers Administration
export const getAdminTeachers = (params) => api.get('/authorities/teachers', { params });
export const createAdminTeacher = (data) => api.post('/authorities/teachers', data);
export const getTeacherById = (id) => api.get(`/authorities/teachers/${id}`);
export const updateTeacher = (id, data) => api.put(`/authorities/teachers/${id}`, data);
export const deleteTeacher = (id) => api.delete(`/authorities/teachers/${id}`);
export const bulkCreateTeachers = (data) => api.post('/authorities/teachers/bulk', data);
export const exportTeachers = (params) => api.get('/authorities/teachers/export', { params, responseType: 'blob' });

// Courses Administration
export const getAdminCourses = (params) => api.get('/authorities/courses', { params });
export const getCourseById = (id) => api.get(`/authorities/courses/${id}`);
export const createCourse = (data) => api.post('/authorities/courses', data);
export const updateCourse = (id, data) => api.put(`/authorities/courses/${id}`, data);
export const deleteCourse = (id) => api.delete(`/authorities/courses/${id}`);
export const assignTeacherToCourse = (courseId, teacherId) => api.post(`/authorities/courses/${courseId}/assign-teacher`, { teacher_id: teacherId });

// Departments
export const getAllDepartments = () => api.get('/authorities/departments');
export const createDepartment = (data) => api.post('/authorities/departments', data);
export const updateDepartment = (id, data) => api.put(`/authorities/departments/${id}`, data);
export const deleteDepartment = (id) => api.delete(`/authorities/departments/${id}`);

// Fees & Finance
export const getAdminFees = (params) => api.get('/authorities/fees', { params });
export const getFeeById = (id) => api.get(`/authorities/fees/${id}`);
export const createFee = (data) => api.post('/authorities/fees', data);
export const updateFee = (id, data) => api.put(`/authorities/fees/${id}`, data);
export const deleteFee = (id) => api.delete(`/authorities/fees/${id}`);
export const getFeeStructure = () => api.get('/authorities/fees/structure');
export const createFeeStructure = (data) => api.post('/authorities/fees/structure', data);
export const updateFeeStructure = (id, data) => api.put(`/authorities/fees/structure/${id}`, data);
export const bulkAssignFees = (data) => api.post('/authorities/fees/bulk-assign', data);
export const getPendingPayments = (params) => api.get('/authorities/fees/pending', { params });
export const recordPayment = (feeId, data) => api.post(`/authorities/fees/${feeId}/payment`, data);

// Notices
export const getAdminNotices = (params) => api.get('/authorities/notices', { params });
export const getNoticeById = (id) => api.get(`/authorities/notices/${id}`);
export const createNotice = (data) => api.post('/authorities/notices', data);
export const updateNotice = (id, data) => api.put(`/authorities/notices/${id}`, data);
export const deleteNotice = (id) => api.delete(`/authorities/notices/${id}`);
export const toggleNoticeStatus = (id) => api.patch(`/authorities/notices/${id}/toggle`);

// Groups
export const getAllGroups = (params) => api.get('/authorities/groups', { params });
export const createGroup = (data) => api.post('/authorities/groups', data);
export const updateGroup = (id, data) => api.put(`/authorities/groups/${id}`, data);
export const deleteGroup = (id) => api.delete(`/authorities/groups/${id}`);
export const manageGroupMembers = (groupId, data) => api.post(`/authorities/groups/${groupId}/members`, data);

// Analytics
export const getStudentAnalytics = () => api.get('/authorities/analytics/students');
export const getAttendanceAnalytics = () => api.get('/authorities/analytics/attendance');
export const getPerformanceAnalytics = () => api.get('/authorities/analytics/performance');
export const getEnrollmentStats = (params) => api.get('/authorities/analytics/enrollment', { params });
export const getRevenueStats = (params) => api.get('/authorities/analytics/revenue', { params });
export const getCourseAnalytics = () => api.get('/authorities/analytics/courses');

// Reports
export const getAdminReports = (reportType = 'summary') => api.get('/authorities/reports', { params: { report_type: reportType } });
export const getDetailedReport = (type, params) => api.get(`/authorities/reports/${type}`, { params, responseType: 'blob' });
export const generateReport = (type, params) => api.post('/authorities/reports/generate', { type, ...params });

// Library Management
export const getLibraryStats = () => api.get('/authorities/library/stats');
export const getOverdueBooks = () => api.get('/authorities/library/overdue');

// Attendance Overview
export const getAttendanceOverview = (params) => api.get('/authorities/attendance/overview', { params });
export const getAttendanceReport = (params) => api.get('/authorities/attendance/report', { params });

// Legacy Compatibility
export const getStudents = getAdminStudents;
export const getTeachers = getAdminTeachers;
export const getCourses = getAdminCourses;
export const getNotices = getAdminNotices;
export const getAnalytics = getStudentAnalytics;
