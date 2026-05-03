import api from '../../../shared/api/client';

// College Lab API endpoints
export const getLabDashboardStats = () => api.get('/college/lab/dashboard');
export const getLabSchedules = () => api.get('/college/lab/schedules');
export const getLabEquipments = () => api.get('/college/lab/equipments');
export const getLabBookings = () => api.get('/college/lab/bookings');
export const bookLab = (data) => api.post('/college/lab/bookings', data);
export const maintainEquipment = (id, data) => api.put(`/college/lab/equipments/${id}`, data);
