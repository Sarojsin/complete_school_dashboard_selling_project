import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/teachers';

export const collegeTeacherKeys = { all: ['collegeTeacher'], courses: () => [...collegeTeacherKeys.all, 'courses'], schedule: () => [...collegeTeacherKeys.all, 'schedule'], leave: () => [...collegeTeacherKeys.all, 'leave'] };

export const useCollegeTeachers = (o = {}) => useQuery({ queryKey: ['teachers'], queryFn: api.getTeachers, ...o });
export const useMyProfile = (o = {}) => useQuery({ queryKey: [...collegeTeacherKeys.all, 'profile'], queryFn: api.getMyTeacherProfile, ...o });
export const useMyCourses = (o = {}) => useQuery({ queryKey: collegeTeacherKeys.courses(), queryFn: api.getMyCourses, ...o });
export const useCourseStudents = (courseId, o = {}) => useQuery({ queryKey: [...collegeTeacherKeys.courses(), courseId], queryFn: () => api.getCourseStudents(courseId), enabled: !!courseId, ...o });
export const useCourseAttendance = (courseId, date, o = {}) => useQuery({ queryKey: [...collegeTeacherKeys.courses(), courseId, 'attendance', date], queryFn: () => api.getAttendance(courseId, date), enabled: !!courseId, ...o });
export const useCourseGrades = (courseId, o = {}) => useQuery({ queryKey: [...collegeTeacherKeys.courses(), courseId, 'grades'], queryFn: () => api.getGrades(courseId), enabled: !!courseId, ...o });
export const useCourseAssignments = (courseId, o = {}) => useQuery({ queryKey: [...collegeTeacherKeys.courses(), courseId, 'assignments'], queryFn: () => api.getAssignments(courseId), enabled: !!courseId, ...o });
export const useTeachingSchedule = (o = {}) => useQuery({ queryKey: collegeTeacherKeys.schedule(), queryFn: api.getTeachingSchedule, ...o });
export const useLeaveRequests = (o = {}) => useQuery({ queryKey: collegeTeacherKeys.leave(), queryFn: api.getLeaveRequests, ...o });
export const useResearchPapers = (o = {}) => useQuery({ queryKey: [...collegeTeacherKeys.all, 'research'], queryFn: api.getResearchPapers, ...o });

export const useMarkAttendance = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ courseId, data }) => api.markAttendance(courseId, data), onSuccess: () => qc.invalidateQueries({ queryKey: collegeTeacherKeys.courses() }) }); };
export const useSubmitGrades = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ courseId, data }) => api.submitGrades(courseId, data), onSuccess: () => qc.invalidateQueries({ queryKey: collegeTeacherKeys.courses() }) }); };
export const useCreateAssignment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createAssignment, onSuccess: () => qc.invalidateQueries({ queryKey: collegeTeacherKeys.courses() }) }); };
export const useGradeAssignment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.gradeAssignment(id, data), onSuccess: () => qc.invalidateQueries({ queryKey: collegeTeacherKeys.courses() }) }); };
export const usePublishResearch = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.publishResearch, onSuccess: () => qc.invalidateQueries({ queryKey: collegeTeacherKeys.all }) }); };
export const useApplyLeave = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.applyLeave, onSuccess: () => qc.invalidateQueries({ queryKey: collegeTeacherKeys.leave() }) }); };
