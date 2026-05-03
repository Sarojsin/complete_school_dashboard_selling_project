import api from '../../../shared/api/client';

// College Dean API endpoints
export const getDeanDashboardStats = () => api.get('/college/dean/dashboard');
export const getDeanFaculties = () => api.get('/college/dean/faculties');
export const getDeanResearch = () => api.get('/college/dean/research');
export const getDeanPublications = () => api.get('/college/dean/publications');
export const getDeanAcademicPrograms = () => api.get('/college/dean/programs');
