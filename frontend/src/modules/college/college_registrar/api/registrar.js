import api from '../../../shared/api/client';

// College Registrar API endpoints
export const getRegistrarDashboardStats = () => api.get('/college/registrar/dashboard');
export const getRegistrarStudents = () => api.get('/college/registrar/students');
export const getRegistrarEnrollments = () => api.get('/college/registrar/enrollments');
export const getRegistrarSchedules = () => api.get('/college/registrar/schedules');
export const getRegistrarCertificates = () => api.get('/college/registrar/certificates');
