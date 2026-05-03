import api from '../../../shared/api/client';

// With missing endpoints from Plan 6

// Dashboard & Stats
export const getLibraryDashboard = () => api.get('/library/summary');
export const getLibraryStats = () => api.get('/library/stats');
export const getLibraryAnalytics = (params) => api.get('/library/analytics', { params });

// Books
export const getAllBooks = (params) => api.get('/library/books', { params });
export const searchBooks = (query, params) => api.get('/library/books', { params: { search: query, ...params } });
export const getBookById = (bookId) => api.get(`/library/books/${bookId}`);
export const addBook = (data) => api.post('/library/books', data);
export const updateBook = (bookId, data) => api.put(`/library/books/${bookId}`, data);
export const deleteBook = (bookId) => api.delete(`/library/books/${bookId}`);
export const getAvailableBooks = (params) => api.get('/library/books/available', { params });
export const getBookCategories = () => api.get('/library/books/categories');
export const getBookByISBN = (isbn) => api.get(`/library/books/isbn/${isbn}`);
export const bulkAddBooks = (data) => api.post('/library/books/bulk', data);
export const exportBooks = (params) => api.get('/library/books/export', { params, responseType: 'blob' });

// Loans & Returns
export const getAllLoans = (params) => api.get('/library/loans', { params });
export const getActiveLoans = (params) => api.get('/library/loans/active', { params });
export const getOverdueLoans = (params) => api.get('/library/loans/overdue', { params });
export const issueBook = (data) => api.post('/library/loans', data);
export const returnBook = (loanId) => api.post(`/library/loans/${loanId}/return`);
export const getLoanById = (loanId) => api.get(`/library/loans/${loanId}`);
export const calculateFine = (loanId) => api.get(`/library/loans/${loanId}/fine`);
export const payFine = (loanId, data) => api.post(`/library/loans/${loanId}/pay-fine`, data);
export const renewLoan = (loanId, data) => api.post(`/library/loans/${loanId}/renew`, data);
export const getStudentLoans = (studentId) => api.get(`/library/loans/student/${studentId}`);
export const getStudentBorrowedBooks = (studentId) => api.get(`/library/loans/student/${studentId}/borrowed`);
export const getStudentOverdueBooks = (studentId) => api.get(`/library/loans/student/${studentId}/overdue`);
export const bulkIssueBooks = (data) => api.post('/library/loans/bulk', data);

// Reservations
export const getReservations = (params) => api.get('/library/reservations', { params });
export const createReservation = (data) => api.post('/library/reservations', data);
export const cancelReservation = (reservationId) => api.delete(`/library/reservations/${reservationId}`);
export const fulfillReservation = (reservationId) => api.post(`/library/reservations/${reservationId}/fulfill`);

// Categories & Authors
export const getCategories = () => api.get('/library/categories');
export const createCategory = (data) => api.post('/library/categories', data);
export const updateCategory = (categoryId, data) => api.put(`/library/categories/${categoryId}`, data);
export const deleteCategory = (categoryId) => api.delete(`/library/categories/${categoryId}`);
export const getAuthors = () => api.get('/library/authors');
export const createAuthor = (data) => api.post('/library/authors', data);
export const getPublishers = () => api.get('/library/publishers');
export const createPublisher = (data) => api.post('/library/publishers', data);

// Library Profile & Settings
export const getLibraryProfile = () => api.get('/library/profile');
export const updateLibraryProfile = (data) => api.put('/library/profile', data);
export const getLibrarySettings = () => api.get('/library/settings');
export const updateLibrarySettings = (data) => api.put('/library/settings', data);
export const getLibraryHours = () => api.get('/library/hours');
export const updateLibraryHours = (data) => api.put('/library/hours', data);

// Reports
export const getLibraryReports = (reportType) => api.get('/library/reports', { params: { type: reportType } });
export const generateLoanReport = (params) => api.get('/library/reports/loans', { params });
export const generateFineReport = (params) => api.get('/library/reports/fines', { params });
export const generateInventoryReport = () => api.get('/library/reports/inventory');

// Notifications
export const getLibraryNotifications = (params) => api.get('/library/notifications', { params });
export const sendDueReminders = () => api.post('/library/notifications/due-reminders');
export const sendOverdueNotices = () => api.post('/library/notifications/overdue-notices');

// Students List
export const getStudentsList = (params) => api.get('/students/', { params });
export const getTeachersList = (params) => api.get('/teachers/', { params });
