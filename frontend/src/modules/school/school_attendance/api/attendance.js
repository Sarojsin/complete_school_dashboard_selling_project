import api from '../../../shared/api/client';

// Get attendance records
export const getAttendanceRecords = (params) => {
  return api.get('/attendance/records', { params });
};

// Get attendance by student
export const getStudentAttendance = (studentId) => {
  return api.get(`/attendance/student/${studentId}`);
};

// Get attendance by class
export const getClassAttendance = (classId, date) => {
  return api.get(`/attendance/class/${classId}`, { params: { date } });
};

// Take attendance
export const takeAttendance = (data) => {
  return api.post('/attendance', data);
};

// Update attendance
export const updateAttendance = (attendanceId, data) => {
  return api.put(`/attendance/${attendanceId}`, data);
};

// Get attendance sessions
export const getSessions = () => {
  return api.get('/attendance/sessions');
};

// Create attendance session
export const createSession = (data) => {
  return api.post('/attendance/sessions', data);
};

// Get attendance reports
export const getReports = () => {
  return api.get('/attendance/reports');
};

// Get attendance stats
export const getStats = (studentId) => {
  return api.get(`/attendance/stats/${studentId}`);
};

// ============================================
// NEW: Extended Attendance Management
// ============================================

export const getAttendanceByDate = (date, params) => {
  return api.get(`/attendance/date/${date}`, { params });
};

export const getAttendanceByCourse = (courseId, params) => {
  return api.get(`/attendance/course/${courseId}`, { params });
};

export const markAttendanceBulk = (data) => {
  return api.post('/attendance/bulk', data);
};

export const getAttendanceHistory = (studentId, params) => {
  return api.get(`/attendance/student/${studentId}/history`, { params });
};

export const getMonthlyAttendance = (studentId, month, year) => {
  return api.get(`/attendance/student/${studentId}/monthly`, { params: { month, year } });
};

export const getAttendancePercentage = (studentId, courseId) => {
  return api.get(`/attendance/percentage`, { params: { studentId, courseId } });
};

export const getAttendanceSummary = (params) => {
  return api.get('/attendance/summary', { params });
};

export const getAttendanceCalendar = (studentId, month, year) => {
  return api.get(`/attendance/calendar/${studentId}`, { params: { month, year } });
};

export const getClassAttendanceStats = (classId) => {
  return api.get(`/attendance/class/${classId}/stats`);
};

export const exportAttendance = (format, params) => {
  return api.get(`/attendance/export/${format}`, { params, responseType: 'blob' });
};

export const getAttendanceTrends = (params) => {
  return api.get('/attendance/trends', { params });
};

// ============================================
// NEW: Session Management
// ============================================

export const getSessionById = (sessionId) => {
  return api.get(`/attendance/sessions/${sessionId}`);
};

export const updateSession = (sessionId, data) => {
  return api.put(`/attendance/sessions/${sessionId}`, data);
};

export const deleteSession = (sessionId) => {
  return api.delete(`/attendance/sessions/${sessionId}`);
};

export const closeSession = (sessionId) => {
  return api.put(`/attendance/sessions/${sessionId}/close`);
};

export const getActiveSessions = () => {
  return api.get('/attendance/sessions/active');
};

// ============================================
// NEW: Reports
// ============================================

export const getAttendanceReport = (params) => {
  return api.get('/attendance/report', { params });
};

export const generateAttendanceReport = (data) => {
  return api.post('/attendance/report/generate', data);
};

export const getLowAttendanceStudents = (threshold) => {
  return api.get('/attendance/alerts/low-attendance', { params: { threshold } });
};

export const getPerfectAttendanceStudents = () => {
  return api.get('/attendance/alerts/perfect');
};
