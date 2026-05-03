import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/attendance';

// Query Keys
export const attendanceKeys = {
  all: ['attendance'] as const,
  records: (params) => [...attendanceKeys.all, 'records', params] as const,
  byStudent: (studentId) => [...attendanceKeys.all, 'student', studentId] as const,
  byClass: (classId) => [...attendanceKeys.all, 'class', classId] as const,
  sessions: () => [...attendanceKeys.all, 'sessions'] as const,
  sessionById: (id) => [...attendanceKeys.all, 'sessions', id] as const,
  stats: (studentId) => [...attendanceKeys.all, 'stats', studentId] as const,
  reports: () => [...attendanceKeys.all, 'reports'] as const,
  summary: () => [...attendanceKeys.all, 'summary'] as const,
  trends: () => [...attendanceKeys.all, 'trends'] as const,
  calendar: (studentId, month, year) => [...attendanceKeys.all, 'calendar', studentId, month, year] as const,
};

// Queries
export const useAttendanceRecords = (params = {}, options = {}) => 
  useQuery({ queryKey: attendanceKeys.records(params), queryFn: () => api.getAttendanceRecords(params), ...options });

export const useStudentAttendance = (studentId, options = {}) => 
  useQuery({ queryKey: attendanceKeys.byStudent(studentId), queryFn: () => api.getStudentAttendance(studentId), enabled: !!studentId, ...options });

export const useClassAttendance = (classId, date, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.byClass(classId), date], queryFn: () => api.getClassAttendance(classId, date), enabled: !!classId, ...options });

export const useAttendanceSessions = (options = {}) => 
  useQuery({ queryKey: attendanceKeys.sessions(), queryFn: api.getSessions, ...options });

export const useActiveSessions = (options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.sessions(), 'active'], queryFn: api.getActiveSessions, ...options });

export const useAttendanceStats = (studentId, options = {}) => 
  useQuery({ queryKey: attendanceKeys.stats(studentId), queryFn: () => api.getStats(studentId), enabled: !!studentId, ...options });

export const useAttendanceReports = (options = {}) => 
  useQuery({ queryKey: attendanceKeys.reports(), queryFn: api.getReports, ...options });

export const useAttendanceSummary = (params = {}, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.summary(), params], queryFn: () => api.getAttendanceSummary(params), ...options });

export const useAttendanceTrends = (params = {}, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.trends(), params], queryFn: () => api.getAttendanceTrends(params), ...options });

export const useAttendanceByDate = (date, params = {}, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.all, 'date', date, params], queryFn: () => api.getAttendanceByDate(date, params), ...options });

export const useAttendanceByCourse = (courseId, params = {}, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.all, 'course', courseId, params], queryFn: () => api.getAttendanceByCourse(courseId, params), enabled: !!courseId, ...options });

export const useAttendanceHistory = (studentId, params = {}, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.byStudent(studentId), 'history', params], queryFn: () => api.getAttendanceHistory(studentId, params), enabled: !!studentId, ...options });

export const useMonthlyAttendance = (studentId, month, year, options = {}) => 
  useQuery({ queryKey: attendanceKeys.calendar(studentId, month, year), queryFn: () => api.getMonthlyAttendance(studentId, month, year), enabled: !!studentId, ...options });

export const useAttendancePercentage = (studentId, courseId, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.all, 'percentage', studentId, courseId], queryFn: () => api.getAttendancePercentage(studentId, courseId), enabled: !!studentId, ...options });

export const useClassAttendanceStats = (classId, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.byClass(classId), 'stats'], queryFn: () => api.getClassAttendanceStats(classId), enabled: !!classId, ...options });

export const useLowAttendanceStudents = (threshold = 75, options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.all, 'alerts', 'low', threshold], queryFn: () => api.getLowAttendanceStudents(threshold), ...options });

export const usePerfectAttendanceStudents = (options = {}) => 
  useQuery({ queryKey: [...attendanceKeys.all, 'alerts', 'perfect'], queryFn: api.getPerfectAttendanceStudents, ...options });

// Mutations
export const useTakeAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.takeAttendance,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.records() });
      queryClient.invalidateQueries({ queryKey: attendanceKeys.sessions() });
    },
  });
};

export const useMarkAttendanceBulk = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markAttendanceBulk,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.records() });
    },
  });
};

export const useUpdateAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateAttendance(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.records() });
    },
  });
};

export const useCreateSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.sessions() });
    },
  });
};

export const useUpdateSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateSession(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.sessions() });
    },
  });
};

export const useDeleteSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.sessions() });
    },
  });
};

export const useCloseSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.closeSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: attendanceKeys.sessions() });
    },
  });
};
