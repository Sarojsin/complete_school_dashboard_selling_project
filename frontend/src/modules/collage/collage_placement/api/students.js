import api from '../../../shared/api/client';

export const getStudents = () => api.get('/school/students/');
export const getMyStudentProfile = () => api.get('/school/students/me');

// ============================================
// NEW: Extended Placement API
// ============================================

export const getPlacements = () => api.get('/placement/');
export const getPlacementDrives = () => api.get('/placement/drives');
export const getDriveDetails = (driveId) => api.get(`/placement/drives/${driveId}`);
export const registerForDrive = (driveId) => api.post(`/placement/drives/${driveId}/register`);
export const getRegisteredDrives = () => api.get('/placement/drives/registered');
export const getAppliedJobs = () => api.get('/placement/applications');
export const applyForJob = (jobId) => api.post('/placement/jobs/apply', { jobId });
export const getJobListings = () => api.get('/placement/jobs');
export const getJobDetails = (jobId) => api.get(`/placement/jobs/${jobId}`);
export const getPlacementStats = () => api.get('/placement/stats');
export const getCompanyList = () => api.get('/placement/companies');
export const getStudentResume = () => api.get('/placement/resume');
export const uploadResume = (formData) => api.post('/placement/resume', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const scheduleInterview = (driveId, data) => api.post(`/placement/drives/${driveId}/interview`, data);
export const getInterviewResults = () => api.get('/placement/interviews');
