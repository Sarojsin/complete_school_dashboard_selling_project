// =====================
// USE LIBRARY - TanStack Query Hooks
// Library Module - Plan 6 Implementation
// =====================

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/library';
import { libraryToast } from '../lib/toast';

// Query Keys
export const libraryKeys = {
  all: ['library'] as const,
  dashboard: () => [...libraryKeys.all, 'dashboard'] as const,
  stats: () => [...libraryKeys.all, 'stats'] as const,
  books: () => [...libraryKeys.all, 'books'] as const,
  bookById: (id) => [...libraryKeys.all, 'books', id] as const,
  loans: () => [...libraryKeys.all, 'loans'] as const,
  loanById: (id) => [...libraryKeys.all, 'loans', id] as const,
  overdue: () => [...libraryKeys.all, 'overdue'] as const,
  reservations: () => [...libraryKeys.all, 'reservations'] as const,
  categories: () => [...libraryKeys.all, 'categories'] as const,
  settings: () => [...libraryKeys.all, 'settings'] as const,
  reports: () => [...libraryKeys.all, 'reports'] as const,
};

// Query Hooks
export const useLibraryDashboard = () => useQuery({ queryKey: libraryKeys.dashboard(), queryFn: api.getLibraryDashboard, staleTime: 5 * 60 * 1000 });
export const useLibraryStats = () => useQuery({ queryKey: libraryKeys.stats(), queryFn: api.getLibraryStats, staleTime: 10 * 60 * 1000 });
export const useLibraryAnalytics = (params) => useQuery({ queryKey: [...libraryKeys.all, 'analytics', params], queryFn: () => api.getLibraryAnalytics(params), staleTime: 10 * 60 * 1000 });
export const useAllBooks = (params = {}) => useQuery({ queryKey: [...libraryKeys.books(), params], queryFn: () => api.getAllBooks(params), staleTime: 5 * 60 * 1000 });
export const useBookById = (bookId) => useQuery({ queryKey: libraryKeys.bookById(bookId), queryFn: () => api.getBookById(bookId), enabled: !!bookId, staleTime: 5 * 60 * 1000 });
export const useAvailableBooks = (params = {}) => useQuery({ queryKey: [...libraryKeys.books(), 'available', params], queryFn: () => api.getAvailableBooks(params), staleTime: 5 * 60 * 1000 });
export const useBookCategories = () => useQuery({ queryKey: libraryKeys.categories(), queryFn: api.getBookCategories, staleTime: 10 * 60 * 1000 });
export const useSearchBooks = (query, params = {}) => useQuery({ queryKey: [...libraryKeys.books(), 'search', query, params], queryFn: () => api.searchBooks(query, params), enabled: !!query, staleTime: 5 * 60 * 1000 });
export const useAllLoans = (params = {}) => useQuery({ queryKey: [...libraryKeys.loans(), params], queryFn: () => api.getAllLoans(params), staleTime: 5 * 60 * 1000 });
export const useActiveLoans = (params = {}) => useQuery({ queryKey: [...libraryKeys.loans(), 'active', params], queryFn: () => api.getActiveLoans(params), staleTime: 5 * 60 * 1000 });
export const useOverdueLoans = (params = {}) => useQuery({ queryKey: [...libraryKeys.overdue(), params], queryFn: () => api.getOverdueLoans(params), staleTime: 5 * 60 * 1000 });
export const useLoanById = (loanId) => useQuery({ queryKey: libraryKeys.loanById(loanId), queryFn: () => api.getLoanById(loanId), enabled: !!loanId, staleTime: 5 * 60 * 1000 });
export const useStudentLoans = (studentId) => useQuery({ queryKey: [...libraryKeys.all, 'student', studentId], queryFn: () => api.getStudentLoans(studentId), enabled: !!studentId, staleTime: 5 * 60 * 1000 });
export const useStudentBorrowedBooks = (studentId) => useQuery({ queryKey: [...libraryKeys.all, 'student', studentId, 'borrowed'], queryFn: () => api.getStudentBorrowedBooks(studentId), enabled: !!studentId, staleTime: 5 * 60 * 1000 });
export const useStudentOverdueBooks = (studentId) => useQuery({ queryKey: [...libraryKeys.all, 'student', studentId, 'overdue'], queryFn: () => api.getStudentOverdueBooks(studentId), enabled: !!studentId, staleTime: 5 * 60 * 1000 });
export const useReservations = (params = {}) => useQuery({ queryKey: [...libraryKeys.reservations(), params], queryFn: () => api.getReservations(params), staleTime: 5 * 60 * 1000 });
export const useCategories = () => useQuery({ queryKey: libraryKeys.categories(), queryFn: api.getCategories, staleTime: 10 * 60 * 1000 });
export const useAuthors = () => useQuery({ queryKey: [...libraryKeys.all, 'authors'], queryFn: api.getAuthors, staleTime: 10 * 60 * 1000 });
export const usePublishers = () => useQuery({ queryKey: [...libraryKeys.all, 'publishers'], queryFn: api.getPublishers, staleTime: 10 * 60 * 1000 });
export const useLibraryProfile = () => useQuery({ queryKey: [...libraryKeys.all, 'profile'], queryFn: api.getLibraryProfile, staleTime: 10 * 60 * 1000 });
export const useLibrarySettings = () => useQuery({ queryKey: libraryKeys.settings(), queryFn: api.getLibrarySettings, staleTime: 10 * 60 * 1000 });
export const useLibraryReports = (reportType) => useQuery({ queryKey: [...libraryKeys.reports(), reportType], queryFn: () => api.getLibraryReports(reportType), staleTime: 10 * 60 * 1000 });
export const useStudentsList = (params = {}) => useQuery({ queryKey: ['students', params], queryFn: () => api.getStudentsList(params), staleTime: 5 * 60 * 1000 });
export const useTeachersList = (params = {}) => useQuery({ queryKey: ['teachers', params], queryFn: () => api.getTeachersList(params), staleTime: 5 * 60 * 1000 });

// Mutation Hooks
export const useAddBook = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.addBook, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.books() }); libraryToast.book.add(); }, onError: () => libraryToast.error() }); };
export const useUpdateBook = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateBook(id, data), onSuccess: (_, { id }) => { qc.invalidateQueries({ queryKey: libraryKeys.bookById(id) }); libraryToast.book.update(); }, onError: () => libraryToast.error() }); };
export const useDeleteBook = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteBook, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.books() }); libraryToast.book.delete(); }, onError: () => libraryToast.error() }); };
export const useBulkAddBooks = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.bulkAddBooks, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.books() }); libraryToast.book.bulk(); }, onError: () => libraryToast.error() }); };
export const useIssueBook = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.issueBook, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.loans() }); libraryToast.loan.issue(); }, onError: () => libraryToast.error() }); };
export const useReturnBook = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.returnBook, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.loans() }); libraryToast.loan.return(); }, onError: () => libraryToast.error() }); };
export const useRenewLoan = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.renewLoan(id, data), onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.loans() }); libraryToast.loan.renew(); }, onError: () => libraryToast.error() }); };
export const usePayFine = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.payFine(id, data), onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.loans() }); libraryToast.loan.fine(); }, onError: () => libraryToast.error() }); };
export const useBulkIssueBooks = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.bulkIssueBooks, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.loans() }); libraryToast.loan.bulk(); }, onError: () => libraryToast.error() }); };
export const useCreateReservation = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createReservation, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.reservations() }); libraryToast.reservation.create(); }, onError: () => libraryToast.error() }); };
export const useCancelReservation = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.cancelReservation, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.reservations() }); libraryToast.reservation.cancel(); }, onError: () => libraryToast.error() }); };
export const useFulfillReservation = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.fulfillReservation, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.reservations() }); qc.invalidateQueries({ queryKey: libraryKeys.loans() }); libraryToast.reservation.fulfill(); }, onError: () => libraryToast.error() }); };
export const useCreateCategory = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createCategory, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.categories() }); libraryToast.category.create(); }, onError: () => libraryToast.error() }); };
export const useUpdateCategory = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateCategory(id, data), onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.categories() }); libraryToast.category.update(); }, onError: () => libraryToast.error() }); };
export const useDeleteCategory = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteCategory, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.categories() }); libraryToast.category.delete(); }, onError: () => libraryToast.error() }); };
export const useUpdateLibraryProfile = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.updateLibraryProfile, onSuccess: () => { qc.invalidateQueries({ queryKey: [...libraryKeys.all, 'profile'] }); libraryToast.profile.update(); }, onError: () => libraryToast.error() }); };
export const useUpdateLibrarySettings = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.updateLibrarySettings, onSuccess: () => { qc.invalidateQueries({ queryKey: libraryKeys.settings() }); libraryToast.settings.update(); }, onError: () => libraryToast.error() }); };
export const useSendDueReminders = () => useMutation({ mutationFn: api.sendDueReminders, onSuccess: () => libraryToast.notification.send(), onError: () => libraryToast.error() });
export const useSendOverdueNotices = () => useMutation({ mutationFn: api.sendOverdueNotices, onSuccess: () => libraryToast.notification.send(), onError: () => libraryToast.error() });

export default { libraryKeys, useLibraryDashboard, useLibraryStats, useAllBooks, useBookById, useAvailableBooks, useAllLoans, useActiveLoans, useOverdueLoans, useStudentLoans, useReservations, useCategories, useLibraryProfile, useLibrarySettings };
