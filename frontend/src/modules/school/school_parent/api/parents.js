import api from '../../../shared/api/client';

// All endpoints now follow the /api/v1/parents/ modular structure
// With missing endpoints from Plan 4

/**
 * Parent Profile & Meta
 */
export const getParentProfile = () => api.get('/parents/me');
export const updateParentProfile = (data) => { const id = data.id || 'me'; return api.put(`/parents/${id}`, data); };
export const getParentSettings = () => api.get('/parents/settings');
export const updateParentSettings = (data) => api.put('/parents/settings', data);
export const changeParentPassword = (data) => api.post('/parents/change-password', data);

/**
 * Dashboard & Multi-Child Management
 */
export const getParentDashboard = () => api.get('/parents/dashboard');
export const getLinkedChildren = () => api.get('/parents/dashboard');
export const getChildrenList = () => api.get('/parents/children');
export const getChildById = (childId) => api.get(`/parents/children/${childId}`);
export const getChildProfile = (studentId) => api.get(`/parents/child/${studentId}/profile`);
export const getChildTimetable = (studentId) => api.get(`/parents/child/${studentId}/timetable`);
export const getChildCourses = (studentId) => api.get(`/parents/child/${studentId}/courses`);
export const getChildTeachers = (studentId) => api.get(`/parents/child/${studentId}/teachers`);

/**
 * Child-Specific Academic Data
 */
export const getChildAttendance = (studentId) => api.get(`/parents/child/${studentId}/attendance`);
export const getChildAttendanceSummary = (studentId) => api.get(`/parents/child/${studentId}/attendance/summary`);
export const getChildGrades = (studentId) => api.get(`/parents/child/${studentId}/grades`);
export const getChildGradeHistory = (studentId) => api.get(`/parents/child/${studentId}/grades/history`);
export const getChildGPA = (studentId) => api.get(`/parents/child/${studentId}/grades/gpa`);
export const getChildHomework = (studentId) => api.get(`/parents/child/${studentId}/homework`);
export const getChildHomeworkDetails = (studentId, homeworkId) => api.get(`/parents/child/${studentId}/homework/${homeworkId}`);
export const getChildAssignments = (studentId) => api.get(`/parents/child/${studentId}/assignments`);
export const getChildTests = (studentId) => api.get(`/parents/child/${studentId}/tests`);
export const getChildTestResults = (studentId, testId) => api.get(`/parents/child/${studentId}/tests/${testId}/results`);

/**
 * Child Fees & Payments
 */
export const getChildFees = (studentId) => api.get(`/parents/child/${studentId}/fees`);
export const getChildFeeDetails = (studentId, feeId) => api.get(`/parents/child/${studentId}/fees/${feeId}`);
export const getChildPaymentHistory = (studentId) => api.get(`/parents/child/${studentId}/payments`);
export const getChildFeeStructure = () => api.get('/parents/fee-structure');

/**
 * Child Library
 */
export const getChildBorrowedBooks = (studentId) => api.get(`/parents/child/${studentId}/library/borrowed`);
export const getChildLibraryHistory = (studentId) => api.get(`/parents/child/${studentId}/library/history`);
export const getChildOverdueBooks = (studentId) => api.get(`/parents/child/${studentId}/library/overdue`);

/**
 * Communication & Notices
 */
export const getParentNotices = () => api.get('/parents/notices');
export const getNoticeById = (noticeId) => api.get(`/parents/notices/${noticeId}`);
export const markNoticeAsRead = (noticeId) => api.patch(`/parents/notices/${noticeId}/read`);
export const getChatContacts = () => api.get('/parents/chat');
export const getMessages = (contactId) => api.get(`/chat/messages/${contactId}`);
export const sendMessage = (data) => api.post('/chat/messages', data);
export const markMessageAsRead = (messageId) => api.patch(`/chat/messages/${messageId}/read`);
export const getUnreadMessageCount = () => api.get('/parents/chat/unread-count');

/**
 * Child Performance Analytics
 */
export const getChildPerformanceOverview = (studentId) => api.get(`/parents/child/${studentId}/performance`);
export const getChildAttendanceRate = (studentId) => api.get(`/parents/child/${studentId}/attendance/rate`);
export const getChildRank = (studentId) => api.get(`/parents/child/${studentId}/rank`);
export const getChildProgress = (studentId) => api.get(`/parents/child/${studentId}/progress`);

/**
 * Child Groups & Activities
 */
export const getChildGroups = (studentId) => api.get(`/parents/child/${studentId}/groups`);
export const getChildAnnouncements = (studentId) => api.get(`/parents/child/${studentId}/announcements`);

/**
 * Notifications
 */
export const getParentNotifications = (params) => api.get('/parents/notifications', { params });
export const markNotificationAsRead = (notificationId) => api.patch(`/parents/notifications/${notificationId}/read`);
export const markAllNotificationsAsRead = () => api.patch('/parents/notifications/read-all');
export const getNotificationSettings = () => api.get('/parents/notifications/settings');
export const updateNotificationSettings = (data) => api.put('/parents/notifications/settings', data);

/**
 * Administrative (Admin/Authority usage if needed)
 */
export const getAllParents = (params = {}) => api.get('/parents/', { params });
export const getParentById = (parentId) => api.get(`/parents/${parentId}`);
export const createParent = (data) => api.post('/parents/', data);
export const updateParent = (parentId, data) => api.put(`/parents/${parentId}`, data);
export const deleteParent = (parentId) => api.delete(`/parents/${parentId}`);
export const linkStudentToParent = (parentId, studentId) => api.post(`/parents/${parentId}/link-student`, { student_id: studentId });
export const unlinkStudentFromParent = (parentId, studentId) => api.delete(`/parents/${parentId}/unlink-student/${studentId}`);
export const getParentLinkedStudents = (parentId) => api.get(`/parents/${parentId}/students`);
