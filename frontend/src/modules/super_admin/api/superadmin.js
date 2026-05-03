import api from '@shared/api/client';

// Get super admin profile
export const getSuperAdminProfile = () => {
  return api.get('/super-admin/profile');
};

// Get admin dashboard
export const getAdminDashboard = () => {
  return api.get('/admin/dashboard');
};

// Get all users
export const getAllUsers = () => {
  return api.get('/admin/users');
};

// Get user by ID
export const getUserById = (userId) => {
  return api.get(`/admin/users/${userId}`);
};

// Deactivate user
export const deactivateUser = (userId) => {
  return api.put(`/admin/users/${userId}/deactivate`);
};

// Activate user
export const activateUser = (userId) => {
  return api.put(`/admin/users/${userId}/activate`);
};

// Get users by role
export const getUsersByRole = () => {
  return api.get('/admin/users-by-role');
};

// Get all settings
export const getSettings = () => {
  return api.get('/admin/settings');
};

// Get specific setting
export const getSetting = (key) => {
  return api.get(`/admin/settings/${key}`);
};

// Update setting
export const updateSetting = (key, value) => {
  return api.put(`/admin/settings/${key}`, { value });
};

// Get all features
export const getFeatures = () => {
  return api.get('/admin/features');
};

// Toggle feature
export const toggleFeature = (name) => {
  return api.put(`/admin/features/${name}/toggle`);
};

// Get audit logs
export const getAuditLogs = (params) => {
  return api.get('/admin/audit-logs', { params });
};

// Get all backups
export const getBackups = () => {
  return api.get('/admin/backups');
};

// Create backup
export const createBackup = () => {
  return api.post('/admin/backups');
};

// Download backup
export const downloadBackup = (backupId) => {
  return api.get(`/admin/backups/${backupId}/download`, { 
    responseType: 'blob' 
  });
};

// Restore backup
export const restoreBackup = (backupId) => {
  return api.post(`/admin/backups/${backupId}/restore`);
};

// Delete backup
export const deleteBackup = (backupId) => {
  return api.delete(`/admin/backups/${backupId}`);
};

// Get system info
export const getSystemInfo = () => {
  return api.get('/admin/system-info');
};

// Get reports
export const getReports = (type) => {
  return api.get('/admin/reports', { params: { type } });
};

// Generate report
export const generateAdminReport = (data) => {
  return api.post('/admin/reports/generate', data);
};

// Academic Management
export const getAcademicData = () => {
  return api.get('/admin/academic');
};

export const manageAcademic = (data) => {
  return api.put('/admin/academic', data);
};

// Communication
export const getCommunications = () => {
  return api.get('/admin/communications');
};

export const sendCommunication = (data) => {
  return api.post('/admin/communications', data);
};

// Finance
export const getFinanceData = () => {
  return api.get('/admin/finance');
};

export const getFinancialReports = (params) => {
  return api.get('/admin/finance/reports', { params });
};

// Media
export const getMediaFiles = () => {
  return api.get('/admin/media');
};

export const uploadMedia = (formData) => {
  return api.post('/admin/media/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const deleteMedia = (mediaId) => {
  return api.delete(`/admin/media/${mediaId}`);
};

// Notices
export const getAdminNotices = () => {
  return api.get('/admin/notices');
};

export const createAdminNotice = (data) => {
  return api.post('/admin/notices', data);
};

export const updateAdminNotice = (noticeId, data) => {
  return api.put(`/admin/notices/${noticeId}`, data);
};

export const deleteAdminNotice = (noticeId) => {
  return api.delete(`/admin/notices/${noticeId}`);
};

// Security
export const getSecuritySettings = () => {
  return api.get('/admin/security');
};

export const updateSecuritySettings = (data) => {
  return api.put('/admin/security', data);
};

// Feature Detail
export const getFeatureDetail = (featureName) => {
  return api.get(`/admin/features/${featureName}`);
};

export const updateFeature = (featureName, data) => {
  return api.put(`/admin/features/${featureName}`, data);
};

// ============================================
// NEW: Schools Management (Multi-school)
// ============================================

export const getAllSchools = (params) => {
  return api.get('/super-admin/schools', { params });
};

export const getSchoolById = (schoolId) => {
  return api.get(`/super-admin/schools/${schoolId}`);
};

export const getSchoolStats = (schoolId) => {
  return api.get(`/super-admin/schools/${schoolId}/stats`);
};

export const createSchool = (data) => {
  return api.post('/super-admin/schools', data);
};

export const updateSchool = (schoolId, data) => {
  return api.put(`/super-admin/schools/${schoolId}`, data);
};

export const deleteSchool = (schoolId) => {
  return api.delete(`/super-admin/schools/${schoolId}`);
};

export const activateSchool = (schoolId) => {
  return api.put(`/super-admin/schools/${schoolId}/activate`);
};

export const deactivateSchool = (schoolId) => {
  return api.put(`/super-admin/schools/${schoolId}/deactivate`);
};

// ============================================
// NEW: Dashboard & Analytics
// ============================================

export const getDashboardStats = () => {
  return api.get('/super-admin/dashboard/stats');
};

export const getSystemHealth = () => {
  return api.get('/super-admin/system/health');
};

export const getSystemMetrics = () => {
  return api.get('/super-admin/system/metrics');
};

export const getActivityLog = (params) => {
  return api.get('/super-admin/activity-log', { params });
};

// ============================================
// NEW: Feature Flags Management
// ============================================

export const getFeatureFlags = () => {
  return api.get('/super-admin/features/flags');
};

export const updateFeatureFlag = (featureName, enabled) => {
  return api.put(`/super-admin/features/flags/${featureName}`, { enabled });
};

export const getFeatureUsage = (featureName) => {
  return api.get(`/super-admin/features/usage/${featureName}`);
};

// ============================================
// NEW: System Settings
// ============================================

export const getSystemSettings = () => {
  return api.get('/super-admin/settings');
};

export const updateSystemSettings = (data) => {
  return api.put('/super-admin/settings', data);
};

export const getSystemConfig = () => {
  return api.get('/super-admin/system/config');
};

export const updateSystemConfig = (data) => {
  return api.put('/super-admin/system/config', data);
};

// ============================================
// NEW: Maintenance Mode
// ============================================

export const toggleMaintenanceMode = (enabled) => {
  return api.put('/super-admin/system/maintenance', { enabled });
};

export const getMaintenanceStatus = () => {
  return api.get('/super-admin/system/maintenance');
};

// ============================================
// NEW: User Management (Global)
// ============================================

export const getGlobalUsers = (params) => {
  return api.get('/super-admin/users', { params });
};

export const getGlobalUserById = (userId) => {
  return api.get(`/super-admin/users/${userId}`);
};

export const updateGlobalUser = (userId, data) => {
  return api.put(`/super-admin/users/${userId}`, data);
};

export const deleteGlobalUser = (userId) => {
  return api.delete(`/super-admin/users/${userId}`);
};

export const getUsersBySchool = (schoolId, params) => {
  return api.get(`/super-admin/schools/${schoolId}/users`, { params });
};

// ============================================
// NEW: Roles & Permissions
// ============================================

export const getRoles = () => {
  return api.get('/super-admin/roles');
};

export const createRole = (data) => {
  return api.post('/super-admin/roles', data);
};

export const updateRole = (roleId, data) => {
  return api.put(`/super-admin/roles/${roleId}`, data);
};

export const deleteRole = (roleId) => {
  return api.delete(`/super-admin/roles/${roleId}`);
};

export const getPermissions = () => {
  return api.get('/super-admin/permissions');
};

// ============================================
// NEW: Database & Backups
// ============================================

export const getDatabaseStatus = () => {
  return api.get('/super-admin/database/status');
};

export const runDatabaseMigration = () => {
  return api.post('/super-admin/database/migrate');
};

export const getDatabaseBackupList = () => {
  return api.get('/super-admin/database/backups');
};

export const createDatabaseBackup = () => {
  return api.post('/super-admin/database/backups');
};

export const restoreDatabaseBackup = (backupId) => {
  return api.post(`/super-admin/database/backups/${backupId}/restore`);
};

// ============================================
// NEW: API Keys & Integrations
// ============================================

export const getApiKeys = () => {
  return api.get('/super-admin/api-keys');
};

export const createApiKey = (data) => {
  return api.post('/super-admin/api-keys', data);
};

export const revokeApiKey = (keyId) => {
  return api.delete(`/super-admin/api-keys/${keyId}`);
};

export const getIntegrations = () => {
  return api.get('/super-admin/integrations');
};

export const configureIntegration = (integrationId, data) => {
  return api.put(`/super-admin/integrations/${integrationId}`, data);
};

// ============================================
// NEW: Notifications & Messages
// ============================================

export const getNotifications = (params) => {
  return api.get('/super-admin/notifications', { params });
};

export const sendNotification = (data) => {
  return api.post('/super-admin/notifications', data);
};

export const markNotificationRead = (notificationId) => {
  return api.put(`/super-admin/notifications/${notificationId}/read`);
};

export const deleteNotification = (notificationId) => {
  return api.delete(`/super-admin/notifications/${notificationId}`);
};

// ============================================
// NEW: Reports & Analytics
// ============================================

export const getGlobalAnalytics = (params) => {
  return api.get('/super-admin/analytics', { params });
};

export const getSchoolAnalytics = (schoolId, params) => {
  return api.get(`/super-admin/schools/${schoolId}/analytics`, { params });
};

export const generateReport = (type, params) => {
  return api.get(`/super-admin/reports/${type}`, { params });
};

export const exportReport = (type, format) => {
  return api.get(`/super-admin/reports/${type}/export`, { 
    params: { format },
    responseType: 'blob' 
  });
};
