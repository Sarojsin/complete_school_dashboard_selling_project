import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/hod';

export const hodKeys = { all: ['hod'], teachers: () => [...hodKeys.all, 'teachers'], students: () => [...hodKeys.all, 'students'], courses: () => [...hodKeys.all, 'courses'], reports: () => [...hodKeys.all, 'reports'], leave: () => [...hodKeys.all, 'leave'] };

export const useDepartmentTeachers = (opts = {}) => useQuery({ queryKey: hodKeys.teachers(), queryFn: api.getDepartmentTeachers, ...opts });
export const useDepartmentStudents = (opts = {}) => useQuery({ queryKey: hodKeys.students(), queryFn: api.getDepartmentStudents, ...opts });
export const useDepartmentCourses = (opts = {}) => useQuery({ queryKey: hodKeys.courses(), queryFn: api.getCourses, ...opts });
export const useDepartmentReports = (opts = {}) => useQuery({ queryKey: hodKeys.reports(), queryFn: api.getReports, ...opts });
export const useLeaveRequests = (opts = {}) => useQuery({ queryKey: hodKeys.leave(), queryFn: api.getLeaveRequests, ...opts });
export const useDepartmentPerformance = (opts = {}) => useQuery({ queryKey: [...hodKeys.all, 'performance'], queryFn: api.getDepartmentPerformance, ...opts });
export const useTeacherPerformance = (teacherId, opts = {}) => useQuery({ queryKey: [...hodKeys.teachers(), teacherId], queryFn: () => api.getTeacherPerformance(teacherId), enabled: !!teacherId, ...opts });
export const useCourseAnalytics = (courseId, opts = {}) => useQuery({ queryKey: [...hodKeys.courses(), courseId], queryFn: () => api.getCourseAnalytics(courseId), enabled: !!courseId, ...opts });
export const useDepartmentAttendance = (opts = {}) => useQuery({ queryKey: [...hodKeys.all, 'attendance'], queryFn: api.getDepartmentAttendance, ...opts });
export const useDepartmentGrades = (opts = {}) => useQuery({ queryKey: [...hodKeys.all, 'grades'], queryFn: api.getDepartmentGrades, ...opts });
export const useDepartmentTimetable = (opts = {}) => useQuery({ queryKey: [...hodKeys.all, 'timetable'], queryFn: api.getDepartmentTimetable, ...opts });
export const useTeacherSchedule = (teacherId, opts = {}) => useQuery({ queryKey: [...hodKeys.teachers(), teacherId, 'schedule'], queryFn: () => api.getTeacherSchedule(teacherId), enabled: !!teacherId, ...opts });
export const useStudentList = (courseId, opts = {}) => useQuery({ queryKey: [...hodKeys.courses(), courseId, 'students'], queryFn: () => api.getStudentList(courseId), enabled: !!courseId, ...opts });
export const useDepartmentExams = (opts = {}) => useQuery({ queryKey: [...hodKeys.all, 'exams'], queryFn: api.getDepartmentExams, ...opts });
export const useExamSchedule = (opts = {}) => useQuery({ queryKey: [...hodKeys.all, 'exam-schedule'], queryFn: api.getExamSchedule, ...opts });

export const useAssignCourse = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.assignCourse, onSuccess: () => qc.invalidateQueries({ queryKey: hodKeys.courses() }) }); };
export const useRemoveCourse = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ courseId, teacherId }) => api.removeCourse(courseId, teacherId), onSuccess: () => qc.invalidateQueries({ queryKey: hodKeys.courses() }) }); };
export const useApproveLeave = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.approveLeave, onSuccess: () => qc.invalidateQueries({ queryKey: hodKeys.leave() }) }); };
export const useRejectLeave = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, reason }) => api.rejectLeave(id, reason), onSuccess: () => qc.invalidateQueries({ queryKey: hodKeys.leave() }) }); };
