import api from '../../../shared/api/client';

// College Account Section API endpoints
export const getAccountDashboardStats = () => api.get('/college/account/dashboard');
export const getFees = () => api.get('/college/account/fees');
export const getPayments = () => api.get('/college/account/payments');
export const getPendingStudents = () => api.get('/college/account/pending');
export const createFee = (data) => api.post('/college/account/fees', data);
export const recordPayment = (data) => api.post('/college/account/payments', data);
