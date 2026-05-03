import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/notes';

export const notesKeys = { all: ['notes'], list: (p) => [...notesKeys.all, 'list', p], byId: (id) => [...notesKeys.all, id], byCourse: (id) => [...notesKeys.all, 'course', id], bySubject: (id) => [...notesKeys.all, 'subject', id], search: (q) => [...notesKeys.all, 'search', q], my: () => [...notesKeys.all, 'my'] };

export const useNotes = (p = {}, o = {}) => useQuery({ queryKey: notesKeys.list(p), queryFn: () => api.getNotes(p), ...o });
export const useNote = (id, o = {}) => useQuery({ queryKey: notesKeys.byId(id), queryFn: () => api.getNote(id), enabled: !!id, ...o });
export const useNotesByCourse = (courseId, o = {}) => useQuery({ queryKey: notesKeys.byCourse(courseId), queryFn: () => api.getNotesByCourse(courseId), enabled: !!courseId, ...o });
export const useNotesBySubject = (subjectId, o = {}) => useQuery({ queryKey: notesKeys.bySubject(subjectId), queryFn: () => api.getNotesBySubject(subjectId), enabled: !!subjectId, ...o });
export const useSearchNotes = (q, o = {}) => useQuery({ queryKey: notesKeys.search(q), queryFn: () => api.searchNotes(q), enabled: !!q, ...o });
export const useFeaturedNotes = (o = {}) => useQuery({ queryKey: [...notesKeys.all, 'featured'], queryFn: api.getFeaturedNotes, ...o });
export const usePopularNotes = (o = {}) => useQuery({ queryKey: [...notesKeys.all, 'popular'], queryFn: api.getPopularNotes, ...o });
export const useMyNotes = (o = {}) => useQuery({ queryKey: notesKeys.my(), queryFn: api.getMyNotes, ...o });
export const useNoteComments = (noteId, o = {}) => useQuery({ queryKey: [...notesKeys.byId(noteId), 'comments'], queryFn: () => api.getNoteComments(noteId), enabled: !!noteId, ...o });

export const useCreateNote = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createNote, onSuccess: () => qc.invalidateQueries({ queryKey: notesKeys.all }) }); };
export const useUpdateNote = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateNote(id, data), onSuccess: () => qc.invalidateQueries({ queryKey: notesKeys.all }) }); };
export const useDeleteNote = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteNote, onSuccess: () => qc.invalidateQueries({ queryKey: notesKeys.all }) }); };
export const useShareNote = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.shareNote(id, data), onSuccess: () => qc.invalidateQueries({ queryKey: notesKeys.all }) }); };
export const useLikeNote = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.likeNote, onSuccess: () => qc.invalidateQueries({ queryKey: notesKeys.all }) }); };
export const useAddComment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ noteId, data }) => api.addComment(noteId, data), onSuccess: () => qc.invalidateQueries({ queryKey: notesKeys.all }) }); };
