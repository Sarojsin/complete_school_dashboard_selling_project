import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/account';

export const accountKeys = { all: ['account'], fees: () => [...accountKeys.all, 'fees'], payments: () => [...accountKeys.all, 'payments'], stats: () => [...accountKeys.all, 'stats'], structures: () => [...accountKeys.all, 'structures'] };

export const useFees = (o = {}) => useQuery({ queryKey: accountKeys.fees(), queryFn: api.getFees, ...o });
export const useFee = (id, o = {}) => useQuery({ queryKey: [...accountKeys.fees(), id], queryFn: () => api.getFee(id), enabled: !!id, ...o });
export const usePayments = (o = {}) => useQuery({ queryKey: accountKeys.payments(), queryFn: api.getPayments, ...o });
export const useDashboardStats = (o = {}) => useQuery({ queryKey: accountKeys.stats(), queryFn: api.getDashboardStats, ...o });
export const usePendingStudents = (o = {}) => useQuery({ queryKey: [...accountKeys.all, 'pending'], queryFn: api.getPendingStudents, ...o });
export const useFeeStructures = (o = {}) => useQuery({ queryKey: accountKeys.structures(), queryFn: api.getFeeStructures, ...o });
export const usePendingPayments = (o = {}) => useQuery({ queryKey: [...accountKeys.payments(), 'pending'], queryFn: api.getPendingPayments, ...o });
export const useFeeHistory = (studentId, o = {}) => useQuery({ queryKey: [...accountKeys.all, 'history', studentId], queryFn: () => api.getFeeHistory(studentId), enabled: !!studentId, ...o });
export const useFinancialSummary = (o = {}) => useQuery({ queryKey: [...accountKeys.all, 'summary'], queryFn: api.getFinancialSummary, ...o });

export const useCreateFee = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createFee, onSuccess: () => qc.invalidateQueries({ queryKey: accountKeys.fees() }) }); };
export const useUpdateFee = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateFee(id, data), onSuccess: () => qc.invalidateQueries({ queryKey: accountKeys.fees() }) }); };
export const useDeleteFee = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteFee, onSuccess: () => qc.invalidateQueries({ queryKey: accountKeys.fees() }) }); };
export const useRecordPayment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.recordPayment, onSuccess: () => qc.invalidateQueries({ queryKey: accountKeys.payments() }) }); };
export const useProcessPayment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ feeId, data }) => api.processPayment(feeId, data), onSuccess: () => qc.invalidateQueries({ queryKey: accountKeys.all }) }); };
export const useCreateFeeStructure = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createFeeStructure, onSuccess: () => qc.invalidateQueries({ queryKey: accountKeys.structures() }) }); };
