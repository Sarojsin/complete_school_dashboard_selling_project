import api from '../../../shared/api/client';

// Get exam section profile
export const getProfile = () => {
  return api.get('/exam-section/profile');
};

// Get all exams
export const getExams = () => {
  return api.get('/exam-section/exams');
};

// Get exam by ID
export const getExam = (examId) => {
  return api.get(`/exam-section/exams/${examId}`);
};

// Create new exam
export const createExam = (data) => {
  return api.post('/exam-section/exams', data);
};

// Update exam
export const updateExam = (examId, data) => {
  return api.put(`/exam-section/exams/${examId}`, data);
};

// Delete exam
export const deleteExam = (examId) => {
  return api.delete(`/exam-section/exams/${examId}`);
};

// Get results
export const getResults = () => {
  return api.get('/exam-section/results');
};

// Get result by student
export const getStudentResult = (studentId) => {
  return api.get(`/exam-section/results/student/${studentId}`);
};

// Post results
export const postResults = (data) => {
  return api.post('/exam-section/results', data);
};

// Get grade sheets
export const getGradeSheets = () => {
  return api.get('/exam-section/grade-sheets');
};

// Get notices
export const getNotices = () => {
  return api.get('/exam-section/notices');
};

// Create notice
export const createNotice = (data) => {
  return api.post('/exam-section/notices', data);
};

// Update notice
export const updateNotice = (noticeId, data) => {
  return api.put(`/exam-section/notices/${noticeId}`, data);
};

// Delete notice
export const deleteNotice = (noticeId) => {
  return api.delete(`/exam-section/notices/${noticeId}`);
};

// ============================================
// NEW: Extended Exam Management
// ============================================

export const getAllExams = (params) => {
  return api.get('/exam-section/exams/all', { params });
};

export const getExamById = (examId) => {
  return api.get(`/exam-section/exams/${examId}`);
};

export const publishExam = (examId) => {
  return api.put(`/exam-section/exams/${examId}/publish`);
};

export const scheduleExam = (examId, scheduleData) => {
  return api.put(`/exam-section/exams/${examId}/schedule`, scheduleData);
};

export const getExamQuestions = (examId) => {
  return api.get(`/exam-section/exams/${examId}/questions`);
};

export const addExamQuestion = (examId, questionData) => {
  return api.post(`/exam-section/exams/${examId}/questions`, questionData);
};

export const updateExamQuestion = (questionId, questionData) => {
  return api.put(`/exam-section/questions/${questionId}`, questionData);
};

export const deleteExamQuestion = (questionId) => {
  return api.delete(`/exam-section/questions/${questionId}`);
};

// ============================================
// NEW: Results Management
// ============================================

export const getAllResults = (params) => {
  return api.get('/exam-section/results/all', { params });
};

export const getExamResults = (examId) => {
  return api.get(`/exam-section/exams/${examId}/results`);
};

export const getStudentResults = (studentId) => {
  return api.get(`/exam-section/students/${studentId}/results`);
};

export const createResult = (data) => {
  return api.post('/exam-section/results', data);
};

export const bulkCreateResults = (examId, results) => {
  return api.post(`/exam-section/exams/${examId}/results/bulk`, { results });
};

export const updateResult = (resultId, data) => {
  return api.put(`/exam-section/results/${resultId}`, data);
};

export const publishResults = (examId) => {
  return api.put(`/exam-section/exams/${examId}/results/publish`);
};

export const getGradeAnalytics = (examId) => {
  return api.get(`/exam-section/exams/${examId}/analytics`);
};

// ============================================
// NEW: Grade Sheets
// ============================================

export const getGradeSheetByStudent = (studentId, examId) => {
  return api.get(`/exam-section/students/${studentId}/grade-sheets`, { params: { examId } });
};

export const generateGradeSheet = (examId, studentId) => {
  return api.post(`/exam-section/exams/${examId}/grade-sheets/generate`, { studentId });
};

export const exportGradeSheet = (examId, format) => {
  return api.get(`/exam-section/exams/${examId}/grade-sheets/export`, {
    params: { format },
    responseType: 'blob',
  });
};

export const bulkGenerateGradeSheets = (examId) => {
  return api.post(`/exam-section/exams/${examId}/grade-sheets/bulk`);
};

// ============================================
// NEW: Exam Sessions
// ============================================

export const getExamSessions = () => {
  return api.get('/exam-section/sessions');
};

export const createExamSession = (data) => {
  return api.post('/exam-section/sessions', data);
};

export const updateExamSession = (sessionId, data) => {
  return api.put(`/exam-section/sessions/${sessionId}`, data);
};

export const deleteExamSession = (sessionId) => {
  return api.delete(`/exam-section/sessions/${sessionId}`);
};

export const assignExamToSession = (sessionId, examId) => {
  return api.post(`/exam-section/sessions/${sessionId}/exams`, { examId });
};

// ============================================
// NEW: Student Exam Access
// ============================================

export const getStudentExams = (studentId) => {
  return api.get(`/exam-section/students/${studentId}/exams`);
};

export const startExam = (examId) => {
  return api.post(`/exam-section/exams/${examId}/start`);
};

export const submitExam = (examId, answers) => {
  return api.post(`/exam-section/exams/${examId}/submit`, { answers });
};

export const getExamAttempt = (examId, attemptId) => {
  return api.get(`/exam-section/exams/${examId}/attempts/${attemptId}`);
};

// ============================================
// NEW: Grading Schemes
// ============================================

export const getGradingSchemes = () => {
  return api.get('/exam-section/grading-schemes');
};

export const createGradingScheme = (data) => {
  return api.post('/exam-section/grading-schemes', data);
};

export const updateGradingScheme = (schemeId, data) => {
  return api.put(`/exam-section/grading-schemes/${schemeId}`, data);
};

export const deleteGradingScheme = (schemeId) => {
  return api.delete(`/exam-section/grading-schemes/${schemeId}`);
};

export const assignGradingScheme = (examId, schemeId) => {
  return api.put(`/exam-section/exams/${examId}/grading-scheme`, { schemeId });
};

// ============================================
// NEW: Exam Analytics
// ============================================

export const getExamAnalytics = (examId) => {
  return api.get(`/exam-section/exams/${examId}/analytics`);
};

export const getStudentPerformance = (studentId) => {
  return api.get(`/exam-section/students/${studentId}/performance`);
};

export const getClassPerformance = (examId) => {
  return api.get(`/exam-section/exams/${examId}/class-performance`);
};

export const exportExamReport = (examId, format) => {
  return api.get(`/exam-section/exams/${examId}/report/export`, {
    params: { format },
    responseType: 'blob',
  });
};
