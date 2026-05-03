import api from '../../../shared/api/client';

// College HOD API endpoints
export const getHODDashboardStats = () => api.get('/college/hod/dashboard');
export const getHODDepartment = () => api.get('/college/hod/department');
export const getHODFaculty = () => api.get('/college/hod/faculty');
export const getHODStudents = () => api.get('/college/hod/students');
export const getHODCourses = () => api.get('/college/hod/courses');
