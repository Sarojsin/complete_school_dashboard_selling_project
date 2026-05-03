import api from '../../../shared/api/client';

// College Research API endpoints
export const getResearchDashboardStats = () => api.get('/college/research/dashboard');
export const getResearchProjects = () => api.get('/college/research/projects');
export const getPublications = () => api.get('/college/research/publications');
export const getGrants = () => api.get('/college/research/grants');
export const submitProject = (data) => api.post('/college/research/projects', data);
export const submitPublication = (data) => api.post('/college/research/publications', data);
