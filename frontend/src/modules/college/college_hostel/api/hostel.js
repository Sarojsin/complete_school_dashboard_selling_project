import api from '../../../shared/api/client';

// College Hostel API endpoints
export const getHostelDashboardStats = () => api.get('/college/hostel/dashboard');
export const getHostels = () => api.get('/college/hostel/hostels');
export const getRooms = (hostelId) => api.get(`/college/hostel/hostels/${hostelId}/rooms`);
export const getStudents = () => api.get('/college/hostel/students');
export const allocateRoom = (data) => api.post('/college/hostel/allocate', data);
export const vacateRoom = (studentId) => api.post(`/college/hostel/vacate/${studentId}`);
