import api from '../../../shared/api/client';

// With missing endpoints from Plan 9

// Timetable
export const getTimetable = (params) => api.get('/timetable', { params });
export const getClassTimetable = (classId, params) => api.get(`/timetable/class/${classId}`, { params });
export const getTeacherTimetable = (teacherId, params) => api.get(`/timetable/teacher/${teacherId}`, { params });
export const getStudentTimetable = (studentId, params) => api.get(`/timetable/student/${studentId}`, { params });
export const getTimetableByDate = (date, params) => api.get('/timetable', { params: { date, ...params } });
export const getTimetableEntry = (entryId) => api.get(`/timetable/${entryId}`);
export const createTimetableEntry = (data) => api.post('/timetable', data);
export const updateTimetableEntry = (entryId, data) => api.put(`/timetable/${entryId}`, data);
export const deleteTimetableEntry = (entryId) => api.delete(`/timetable/${entryId}`);
export const bulkCreateEntries = (data) => api.post('/timetable/bulk', data);
export const copyWeekTimetable = (data) => api.post('/timetable/copy-week', data);
export const getTimetableConflicts = (params) => api.get('/timetable/conflicts', { params });

// Periods & Slots
export const getPeriods = () => api.get('/timetable/periods');
export const createPeriod = (data) => api.post('/timetable/periods', data);
export const updatePeriod = (periodId, data) => api.put(`/timetable/periods/${periodId}`, data);
export const deletePeriod = (periodId) => api.delete(`/timetable/periods/${periodId}`);
export const getTimeSlots = () => api.get('/timetable/time-slots');
export const createTimeSlot = (data) => api.post('/timetable/time-slots', data);
export const updateTimeSlot = (slotId, data) => api.put(`/timetable/time-slots/${slotId}`, data);
export const deleteTimeSlot = (slotId) => api.delete(`/timetable/time-slots/${slotId}`);

// Rooms & Resources
export const getRooms = () => api.get('/timetable/rooms');
export const createRoom = (data) => api.post('/timetable/rooms', data);
export const updateRoom = (roomId, data) => api.put(`/timetable/rooms/${roomId}`, data);
export const deleteRoom = (roomId) => api.delete(`/timetable/rooms/${roomId}`);
export const getRoomAvailability = (roomId, date) => api.get(`/timetable/rooms/${roomId}/availability`, { params: { date } });

// Classes
export const getTimetableClasses = () => api.get('/timetable/classes');
export const createTimetableClass = (data) => api.post('/timetable/classes', data);
export const updateTimetableClass = (classId, data) => api.put(`/timetable/classes/${classId}`, data);
export const deleteTimetableClass = (classId) => api.delete(`/timetable/classes/${classId}`);

// Substitutions
export const getSubstitutions = (params) => api.get('/timetable/substitutions', { params });
export const createSubstitution = (data) => api.post('/timetable/substitutions', data);
export const cancelSubstitution = (substitutionId) => api.delete(`/timetable/substitutions/${substitutionId}`);
export const getTeacherSubstitutions = (teacherId) => api.get(`/timetable/substitutions/teacher/${teacherId}`);

// Reports & Analytics
export const getTimetableReport = (params) => api.get('/timetable/report', { params });
export const getTimetableUtilization = () => api.get('/timetable/analytics/utilization');
export const exportTimetable = (params) => api.get('/timetable/export', { params, responseType: 'blob' });
