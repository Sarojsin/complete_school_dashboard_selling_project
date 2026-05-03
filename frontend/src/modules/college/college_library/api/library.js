import api from '../../../shared/api/client';

// College Library API endpoints
export const getLibraryDashboardStats = () => api.get('/college/library/dashboard');
export const getBooks = (params) => api.get('/college/library/books', { params });
export const getBorrowedBooks = () => api.get('/college/library/borrowed');
export const getOverdueBooks = () => api.get('/college/library/overdue');
export const addBook = (data) => api.post('/college/library/books', data);
export const issueBook = (data) => api.post('/college/library/issue', data);
export const returnBook = (bookId) => api.post(`/college/library/return/${bookId}`);
