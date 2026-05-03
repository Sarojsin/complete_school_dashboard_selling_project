import api from '@shared/api/client';

export const getStudents = () => api.get('/school/students/');
export const getMyStudentProfile = () => api.get('/school/students/me');
