import api from '../../../shared/api/client';

// College Exam Section API endpoints
export const getExamDashboardStats = () => api.get('/college/exam/dashboard');
export const getExams = () => api.get('/college/exam/exams');
export const getResults = () => api.get('/college/exam/results');
export const getNotices = () => api.get('/college/exam/notices');
export const scheduleExam = (data) => api.post('/college/exam/exams', data);
export const postResult = (data) => api.post('/college/exam/results', data);
