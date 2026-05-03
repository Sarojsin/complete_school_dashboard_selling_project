import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/examSection';

// ============================================
// Query Keys
// ============================================

export const examKeys = {
  all: ['exam'] as const,
  list: () => [...examKeys.all, 'list'] as const,
  byId: (id) => [...examKeys.all, 'list', id] as const,
  questions: (examId) => [...examKeys.all, 'questions', examId] as const,
  results: () => [...examKeys.all, 'results'] as const,
  resultsByExam: (examId) => [...examKeys.all, 'results', examId] as const,
  resultsByStudent: (studentId) => [...examKeys.all, 'results', 'student', studentId] as const,
  gradeSheets: () => [...examKeys.all, 'gradeSheets'] as const,
  gradeAnalytics: (examId) => [...examKeys.all, 'analytics', examId] as const,
  sessions: () => [...examKeys.all, 'sessions'] as const,
  gradingSchemes: () => [...examKeys.all, 'gradingSchemes'] as const,
  studentExams: (studentId) => [...examKeys.all, 'studentExams', studentId] as const,
  notices: () => [...examKeys.all, 'notices'] as const,
};

// ============================================
// Exam Queries
// ============================================

export const useAllExams = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.list(), params],
    queryFn: () => api.getAllExams(params),
    ...options,
  });
};

export const useExamById = (examId, options = {}) => {
  return useQuery({
    queryKey: examKeys.byId(examId),
    queryFn: () => api.getExamById(examId),
    enabled: !!examId,
    ...options,
  });
};

export const useExamQuestions = (examId, options = {}) => {
  return useQuery({
    queryKey: examKeys.questions(examId),
    queryFn: () => api.getExamQuestions(examId),
    enabled: !!examId,
    ...options,
  });
};

export const useExams = (options = {}) => {
  return useQuery({
    queryKey: examKeys.list(),
    queryFn: api.getExams,
    ...options,
  });
};

export const useExam = (examId, options = {}) => {
  return useQuery({
    queryKey: examKeys.byId(examId),
    queryFn: () => api.getExam(examId),
    enabled: !!examId,
    ...options,
  });
};

// ============================================
// Results Queries
// ============================================

export const useAllResults = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.results(), params],
    queryFn: () => api.getAllResults(params),
    ...options,
  });
};

export const useExamResults = (examId, options = {}) => {
  return useQuery({
    queryKey: examKeys.resultsByExam(examId),
    queryFn: () => api.getExamResults(examId),
    enabled: !!examId,
    ...options,
  });
};

export const useStudentResults = (studentId, options = {}) => {
  return useQuery({
    queryKey: examKeys.resultsByStudent(studentId),
    queryFn: () => api.getStudentResults(studentId),
    enabled: !!studentId,
    ...options,
  });
};

export const useResults = (options = {}) => {
  return useQuery({
    queryKey: examKeys.results(),
    queryFn: api.getResults,
    ...options,
  });
};

export const useStudentResult = (studentId, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.results(), 'student', studentId],
    queryFn: () => api.getStudentResult(studentId),
    enabled: !!studentId,
    ...options,
  });
};

export const useGradeAnalytics = (examId, options = {}) => {
  return useQuery({
    queryKey: examKeys.gradeAnalytics(examId),
    queryFn: () => api.getGradeAnalytics(examId),
    enabled: !!examId,
    ...options,
  });
};

// ============================================
// Grade Sheets Queries
// ============================================

export const useGradeSheets = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.gradeSheets(), params],
    queryFn: () => api.getGradeSheets(params),
    ...options,
  });
};

export const useGradeSheetByStudent = (studentId, examId, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.gradeSheets(), 'student', studentId, examId],
    queryFn: () => api.getGradeSheetByStudent(studentId, examId),
    enabled: !!studentId && !!examId,
    ...options,
  });
};

// ============================================
// Session Queries
// ============================================

export const useExamSessions = (options = {}) => {
  return useQuery({
    queryKey: examKeys.sessions(),
    queryFn: api.getExamSessions,
    ...options,
  });
};

// ============================================
// Student Exam Queries
// ============================================

export const useStudentExams = (studentId, options = {}) => {
  return useQuery({
    queryKey: examKeys.studentExams(studentId),
    queryFn: () => api.getStudentExams(studentId),
    enabled: !!studentId,
    ...options,
  });
};

export const useExamAttempt = (examId, attemptId, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.byId(examId), 'attempt', attemptId],
    queryFn: () => api.getExamAttempt(examId, attemptId),
    enabled: !!examId && !!attemptId,
    ...options,
  });
};

// ============================================
// Grading Schemes Queries
// ============================================

export const useGradingSchemes = (options = {}) => {
  return useQuery({
    queryKey: examKeys.gradingSchemes(),
    queryFn: api.getGradingSchemes,
    ...options,
  });
};

// ============================================
// Analytics Queries
// ============================================

export const useExamAnalytics = (examId, options = {}) => {
  return useQuery({
    queryKey: examKeys.gradeAnalytics(examId),
    queryFn: () => api.getExamAnalytics(examId),
    enabled: !!examId,
    ...options,
  });
};

export const useStudentPerformance = (studentId, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.all, 'performance', studentId],
    queryFn: () => api.getStudentPerformance(studentId),
    enabled: !!studentId,
    ...options,
  });
};

export const useClassPerformance = (examId, options = {}) => {
  return useQuery({
    queryKey: [...examKeys.all, 'classPerformance', examId],
    queryFn: () => api.getClassPerformance(examId),
    enabled: !!examId,
    ...options,
  });
};

// ============================================
// Notices Queries
// ============================================

export const useExamNotices = (options = {}) => {
  return useQuery({
    queryKey: examKeys.notices(),
    queryFn: api.getNotices,
    ...options,
  });
};

// ============================================
// Mutations - Exams
// ============================================

export const useCreateExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createExam,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.list() });
    },
  });
};

export const useUpdateExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, data }) => api.updateExam(examId, data),
    onSuccess: (_, { examId }) => {
      queryClient.invalidateQueries({ queryKey: examKeys.list() });
      queryClient.invalidateQueries({ queryKey: examKeys.byId(examId) });
    },
  });
};

export const useDeleteExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteExam,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.list() });
    },
  });
};

export const usePublishExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.publishExam,
    onSuccess: (_, examId) => {
      queryClient.invalidateQueries({ queryKey: examKeys.list() });
      queryClient.invalidateQueries({ queryKey: examKeys.byId(examId) });
    },
  });
};

export const useScheduleExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, scheduleData }) => api.scheduleExam(examId, scheduleData),
    onSuccess: (_, { examId }) => {
      queryClient.invalidateQueries({ queryKey: examKeys.list() });
      queryClient.invalidateQueries({ queryKey: examKeys.byId(examId) });
    },
  });
};

// ============================================
// Mutations - Questions
// ============================================

export const useAddExamQuestion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, questionData }) => api.addExamQuestion(examId, questionData),
    onSuccess: (_, { examId }) => {
      queryClient.invalidateQueries({ queryKey: examKeys.questions(examId) });
    },
  });
};

export const useUpdateExamQuestion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ questionId, questionData }) => api.updateExamQuestion(questionId, questionData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.questions() });
    },
  });
};

export const useDeleteExamQuestion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteExamQuestion,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.questions() });
    },
  });
};

// ============================================
// Mutations - Results
// ============================================

export const useCreateResult = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createResult,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.results() });
    },
  });
};

export const useBulkCreateResults = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, results }) => api.bulkCreateResults(examId, results),
    onSuccess: (_, { examId }) => {
      queryClient.invalidateQueries({ queryKey: examKeys.results() });
      queryClient.invalidateQueries({ queryKey: examKeys.resultsByExam(examId) });
    },
  });
};

export const useUpdateResult = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ resultId, data }) => api.updateResult(resultId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.results() });
    },
  });
};

export const usePublishResults = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.publishResults,
    onSuccess: (_, examId) => {
      queryClient.invalidateQueries({ queryKey: examKeys.results() });
      queryClient.invalidateQueries({ queryKey: examKeys.resultsByExam(examId) });
    },
  });
};

export const usePostResults = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.postResults,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.results() });
    },
  });
};

// ============================================
// Mutations - Grade Sheets
// ============================================

export const useGenerateGradeSheet = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, studentId }) => api.generateGradeSheet(examId, studentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.gradeSheets() });
    },
  });
};

export const useBulkGenerateGradeSheets = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkGenerateGradeSheets,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.gradeSheets() });
    },
  });
};

// ============================================
// Mutations - Sessions
// ============================================

export const useCreateExamSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createExamSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.sessions() });
    },
  });
};

export const useUpdateExamSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ sessionId, data }) => api.updateExamSession(sessionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.sessions() });
    },
  });
};

export const useDeleteExamSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteExamSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.sessions() });
    },
  });
};

export const useAssignExamToSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ sessionId, examId }) => api.assignExamToSession(sessionId, examId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.sessions() });
    },
  });
};

// ============================================
// Mutations - Student Exam
// ============================================

export const useStartExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.startExam,
    onSuccess: (_, examId) => {
      queryClient.invalidateQueries({ queryKey: examKeys.byId(examId) });
    },
  });
};

export const useSubmitExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, answers }) => api.submitExam(examId, answers),
    onSuccess: (_, examId) => {
      queryClient.invalidateQueries({ queryKey: examKeys.results() });
      queryClient.invalidateQueries({ queryKey: examKeys.resultsByExam(examId) });
    },
  });
};

// ============================================
// Mutations - Grading Schemes
// ============================================

export const useCreateGradingScheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createGradingScheme,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.gradingSchemes() });
    },
  });
};

export const useUpdateGradingScheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ schemeId, data }) => api.updateGradingScheme(schemeId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.gradingSchemes() });
    },
  });
};

export const useDeleteGradingScheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteGradingScheme,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.gradingSchemes() });
    },
  });
};

export const useAssignGradingScheme = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ examId, schemeId }) => api.assignGradingScheme(examId, schemeId),
    onSuccess: (_, { examId }) => {
      queryClient.invalidateQueries({ queryKey: examKeys.byId(examId) });
    },
  });
};

// ============================================
// Mutations - Notices
// ============================================

export const useCreateExamNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createNotice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.notices() });
    },
  });
};

export const useUpdateExamNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ noticeId, data }) => api.updateNotice(noticeId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.notices() });
    },
  });
};

export const useDeleteExamNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteNotice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examKeys.notices() });
    },
  });
};
