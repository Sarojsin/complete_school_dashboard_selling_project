// USE TIMETABLE - TanStack Query Hooks
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/timetable';
import { timetableToast } from '../lib/toast';

export const timetableKeys = { all: ['timetable'], list: () => [...timetableKeys.all, 'list'], byClass: (id) => [...timetableKeys.all, 'class', id], byTeacher: (id) => [...timetableKeys.all, 'teacher', id] };

export const useTimetable = (params) => useQuery({ queryKey: [...timetableKeys.list(), params], queryFn: () => api.getTimetable(params), staleTime: 10 * 60 * 1000 });
export const useClassTimetable = (classId, params) => useQuery({ queryKey: [...timetableKeys.byClass(classId), params], queryFn: () => api.getClassTimetable(classId, params), enabled: !!classId, staleTime: 10 * 60 * 1000 });
export const useTeacherTimetable = (teacherId, params) => useQuery({ queryKey: [...timetableKeys.byTeacher(teacherId), params], queryFn: () => api.getTeacherTimetable(teacherId, params), enabled: !!teacherId, staleTime: 10 * 60 * 1000 });
export const useStudentTimetable = (studentId, params) => useQuery({ queryKey: [...timetableKeys.all, 'student', studentId, params], queryFn: () => api.getStudentTimetable(studentId, params), enabled: !!studentId, staleTime: 10 * 60 * 1000 });
export const usePeriods = () => useQuery({ queryKey: [...timetableKeys.all, 'periods'], queryFn: api.getPeriods, staleTime: 10 * 60 * 1000 });
export const useRooms = () => useQuery({ queryKey: [...timetableKeys.all, 'rooms'], queryFn: api.getRooms, staleTime: 10 * 60 * 1000 });
export const useSubstitutions = (params) => useQuery({ queryKey: [...timetableKeys.all, 'substitutions', params], queryFn: () => api.getSubstitutions(params), staleTime: 5 * 60 * 1000 });
export const useConflicts = (params) => useQuery({ queryKey: [...timetableKeys.all, 'conflicts'], queryFn: () => api.getTimetableConflicts(params), staleTime: 10 * 60 * 1000 });

export const useCreateEntry = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createTimetableEntry, onSuccess: () => { qc.invalidateQueries({ queryKey: timetableKeys.all }); timetableToast.entry.create(); }, onError: () => timetableToast.error() }); };
export const useUpdateEntry = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateTimetableEntry(id, data), onSuccess: () => { qc.invalidateQueries({ queryKey: timetableKeys.all }); timetableToast.entry.update(); }, onError: () => timetableToast.error() }); };
export const useDeleteEntry = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteTimetableEntry, onSuccess: () => { qc.invalidateQueries({ queryKey: timetableKeys.all }); timetableToast.entry.delete(); }, onError: () => timetableToast.error() }); };
export const useBulkCreateEntries = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.bulkCreateEntries, onSuccess: () => { qc.invalidateQueries({ queryKey: timetableKeys.all }); timetableToast.entry.bulk(); }, onError: () => timetableToast.error() }); };
export const useCreatePeriod = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createPeriod, onSuccess: () => { qc.invalidateQueries({ queryKey: [...timetableKeys.all, 'periods'] }); timetableToast.period.create(); }, onError: () => timetableToast.error() }); };
export const useCreateRoom = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createRoom, onSuccess: () => { qc.invalidateQueries({ queryKey: [...timetableKeys.all, 'rooms'] }); timetableToast.room.create(); }, onError: () => timetableToast.error() }); };
export const useCreateSubstitution = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createSubstitution, onSuccess: () => { qc.invalidateQueries({ queryKey: [...timetableKeys.all, 'substitutions'] }); timetableToast.substitution.create(); }, onError: () => timetableToast.error() }); };
export const useCancelSubstitution = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.cancelSubstitution, onSuccess: () => { qc.invalidateQueries({ queryKey: [...timetableKeys.all, 'substitutions'] }); timetableToast.substitution.cancel(); }, onError: () => timetableToast.error() }); };

export default { timetableKeys, useTimetable, useClassTimetable, useTeacherTimetable };
