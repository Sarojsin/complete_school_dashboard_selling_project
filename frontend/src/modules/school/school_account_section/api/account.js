import api from '../../../shared/api/client';

// Get account profile
export const getProfile = () => {
  return api.get('/account/profile');
};

// Get all fees
export const getFees = () => {
  return api.get('/account/fees');
};

// Get fee by ID
export const getFee = (feeId) => {
  return api.get(`/account/fees/${feeId}`);
};

// Create fee
export const createFee = (data) => {
  return api.post('/account/fees', data);
};

// Update fee
export const updateFee = (feeId, data) => {
  return api.put(`/account/fees/${feeId}`, data);
};

// Delete fee
export const deleteFee = (feeId) => {
  return api.delete(`/account/fees/${feeId}`);
};

// Get all payments
export const getPayments = () => {
  return api.get('/account/payments');
};

// Get payment by ID
export const getPayment = (paymentId) => {
  return api.get(`/account/payments/${paymentId}`);
};

// Record payment
export const recordPayment = (data) => {
  return api.post('/account/payments', data);
};

// Get pending payments
export const getPendingPayments = () => {
  return api.get('/account/payments/pending');
};

// Get fee structures
export const getFeeStructures = () => {
  return api.get('/account/fee-structures');
};

// Create fee structure
export const createFeeStructure = (data) => {
  return api.post('/account/fee-structures', data);
};

// Get dashboard stats
export const getDashboardStats = () => {
  return api.get('/account/dashboard/stats');
};

// Get students with pending fees
export const getPendingStudents = () => {
  return api.get('/account/pending-students');
};

// ============================================
// NEW: Extended Account Management
// ============================================

export const getFeeHistory = (studentId) => api.get(`/account/students/${studentId}/fee-history`);
export const getPaymentMethods = () => api.get('/account/payment-methods');
export const addPaymentMethod = (data) => api.post('/account/payment-methods', data);
export const removePaymentMethod = (methodId) => api.delete(`/account/payment-methods/${methodId}`);
export const processPayment = (feeId, data) => api.post(`/account/fees/${feeId}/pay`, data);
export const getInvoice = (paymentId) => api.get(`/account/payments/${paymentId}/invoice`);
export const downloadInvoice = (paymentId) => api.get(`/account/payments/${paymentId}/invoice/download`, { responseType: 'blob' });
export const sendPaymentReminder = (studentId) => api.post(`/account/students/${studentId}/reminder`);
export const getRevenueReport = (params) => api.get('/account/reports/revenue', { params });
export const getExpenseReport = (params) => api.get('/account/reports/expense', { params });
export const getFinancialSummary = () => api.get('/account/reports/summary');
export const createInstallment = (data) => api.post('/account/installments', data);
export const getInstallments = (studentId) => api.get(`/account/students/${studentId}/installments`);
export const updateInstallment = (installmentId, data) => api.put(`/account/installments/${installmentId}`, data);
