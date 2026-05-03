import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/students';

export const placementKeys = { all: ['placement'], drives: () => [...placementKeys.all, 'drives'], jobs: () => [...placementKeys.all, 'jobs'], stats: () => [...placementKeys.all, 'stats'] };

export const usePlacements = (o = {}) => useQuery({ queryKey: placementKeys.all, queryFn: api.getPlacements, ...o });
export const usePlacementDrives = (o = {}) => useQuery({ queryKey: placementKeys.drives(), queryFn: api.getPlacementDrives, ...o });
export const useDriveDetails = (id, o = {}) => useQuery({ queryKey: [...placementKeys.drives(), id], queryFn: () => api.getDriveDetails(id), enabled: !!id, ...o });
export const useRegisteredDrives = (o = {}) => useQuery({ queryKey: [...placementKeys.drives(), 'registered'], queryFn: api.getRegisteredDrives, ...o });
export const useJobListings = (o = {}) => useQuery({ queryKey: placementKeys.jobs(), queryFn: api.getJobListings, ...o });
export const useJobDetails = (id, o = {}) => useQuery({ queryKey: [...placementKeys.jobs(), id], queryFn: () => api.getJobDetails(id), enabled: !!id, ...o });
export const useAppliedJobs = (o = {}) => useQuery({ queryKey: [...placementKeys.all, 'applied'], queryFn: api.getAppliedJobs, ...o });
export const usePlacementStats = (o = {}) => useQuery({ queryKey: placementKeys.stats(), queryFn: api.getPlacementStats, ...o });
export const useCompanyList = (o = {}) => useQuery({ queryKey: [...placementKeys.all, 'companies'], queryFn: api.getCompanyList, ...o });
export const useInterviewResults = (o = {}) => useQuery({ queryKey: [...placementKeys.all, 'interviews'], queryFn: api.getInterviewResults, ...o });

export const useRegisterForDrive = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.registerForDrive, onSuccess: () => qc.invalidateQueries({ queryKey: placementKeys.drives() }) }); };
export const useApplyForJob = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.applyForJob, onSuccess: () => qc.invalidateQueries({ queryKey: placementKeys.jobs() }) }); };
export const useUploadResume = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.uploadResume, onSuccess: () => qc.invalidateQueries({ queryKey: placementKeys.all }) }); };
