import api from '../../../shared/api/client';

// Get all notes
export const getNotes = (params) => {
  return api.get('/notes', { params });
};

// Get note by ID
export const getNote = (noteId) => {
  return api.get(`/notes/${noteId}`);
};

// Create note
export const createNote = (data) => {
  return api.post('/notes', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

// Update note
export const updateNote = (noteId, data) => {
  return api.put(`/notes/${noteId}`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

// Delete note
export const deleteNote = (noteId) => {
  return api.delete(`/notes/${noteId}`);
};

// Download note
export const downloadNote = (noteId) => {
  return api.get(`/notes/${noteId}/download`, { responseType: 'blob' });
};

// Get notes by subject
export const getNotesBySubject = (subjectId) => {
  return api.get(`/notes/subject/${subjectId}`);
};

// ============================================
// NEW: Extended Notes Management
// ============================================

export const getNotesByCourse = (courseId) => api.get(`/notes/course/${courseId}`);
export const searchNotes = (query) => api.get('/notes/search', { params: { q: query } });
export const getFeaturedNotes = () => api.get('/notes/featured');
export const getPopularNotes = () => api.get('/notes/popular');
export const getMyNotes = () => api.get('/notes/my');
export const shareNote = (noteId, data) => api.post(`/notes/${noteId}/share`, data);
export const unshareNote = (noteId) => api.delete(`/notes/${noteId}/share`);
export const viewNote = (noteId) => api.put(`/notes/${noteId}/view`);
export const likeNote = (noteId) => api.post(`/notes/${noteId}/like`);
export const unlikeNote = (noteId) => api.delete(`/notes/${noteId}/like`);
export const getNoteComments = (noteId) => api.get(`/notes/${noteId}/comments`);
export const addComment = (noteId, data) => api.post(`/notes/${noteId}/comments`, data);
export const deleteComment = (noteId, commentId) => api.delete(`/notes/${noteId}/comments/${commentId}`);
export const getNoteVersions = (noteId) => api.get(`/notes/${noteId}/versions`);
export const restoreVersion = (noteId, versionId) => api.post(`/notes/${noteId}/versions/${versionId}/restore`);
