import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/superadmin';

// ============================================
// Query Keys
// ============================================

export const superAdminKeys = {
  all: ['superAdmin'] as const,
  dashboard: () => [...superAdminKeys.all, 'dashboard'] as const,
  schools: () => [...superAdminKeys.all, 'schools'] as const,
  schoolById: (id) => [...superAdminKeys.all, 'schools', id] as const,
  schoolStats: (id) => [...superAdminKeys.all, 'schools', id, 'stats'] as const,
  users: () => [...superAdminKeys.all, 'users'] as const,
  userById: (id) => [...superAdminKeys.all, 'users', id] as const,
  roles: () => [...superAdminKeys.all, 'roles'] as const,
  permissions: () => [...superAdminKeys.all, 'permissions'] as const,
  settings: () => [...superAdminKeys.all, 'settings'] as const,
  features: () => [...superAdminKeys.all, 'features'] as const,
  systemHealth: () => [...superAdminKeys.all, 'systemHealth'] as const,
  systemMetrics: () => [...superAdminKeys.all, 'systemMetrics'] as const,
  backups: () => [...superAdminKeys.all, 'backups'] as const,
  notifications: () => [...superAdminKeys.all, 'notifications'] as const,
  analytics: () => [...superAdminKeys.all, 'analytics'] as const,
  apiKeys: () => [...superAdminKeys.all, 'apiKeys'] as const,
  integrations: () => [...superAdminKeys.all, 'integrations'] as const,
  activityLog: () => [...superAdminKeys.all, 'activityLog'] as const,
  database: () => [...superAdminKeys.all, 'database'] as const,
};

// ============================================
// Dashboard Queries
// ============================================

export const useDashboardStats = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.dashboard(),
    queryFn: api.getDashboardStats,
    refetchInterval: 60000,
    ...options,
  });
};

export const useSystemHealth = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.systemHealth(),
    queryFn: api.getSystemHealth,
    refetchInterval: 15000,
    ...options,
  });
};

export const useSystemMetrics = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.systemMetrics(),
    queryFn: api.getSystemMetrics,
    refetchInterval: 30000,
    ...options,
  });
};

export const useActivityLog = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.activityLog(), params],
    queryFn: () => api.getActivityLog(params),
    ...options,
  });
};

// ============================================
// Schools Queries
// ============================================

export const useAllSchools = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.schools(), params],
    queryFn: () => api.getAllSchools(params),
    ...options,
  });
};

export const useSchoolById = (schoolId, options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.schoolById(schoolId),
    queryFn: () => api.getSchoolById(schoolId),
    enabled: !!schoolId,
    ...options,
  });
};

export const useSchoolStats = (schoolId, options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.schoolStats(schoolId),
    queryFn: () => api.getSchoolStats(schoolId),
    enabled: !!schoolId,
    refetchInterval: 30000,
    ...options,
  });
};

// ============================================
// Users Queries
// ============================================

export const useGlobalUsers = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.users(), params],
    queryFn: () => api.getGlobalUsers(params),
    ...options,
  });
};

export const useGlobalUserById = (userId, options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.userById(userId),
    queryFn: () => api.getGlobalUserById(userId),
    enabled: !!userId,
    ...options,
  });
};

export const useUsersBySchool = (schoolId, params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.users(), 'school', schoolId, params],
    queryFn: () => api.getUsersBySchool(schoolId, params),
    enabled: !!schoolId,
    ...options,
  });
};

// ============================================
// Roles & Permissions Queries
// ============================================

export const useRoles = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.roles(),
    queryFn: api.getRoles,
    ...options,
  });
};

export const usePermissions = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.permissions(),
    queryFn: api.getPermissions,
    ...options,
  });
};

// ============================================
// Settings Queries
// ============================================

export const useSystemSettings = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.settings(),
    queryFn: api.getSystemSettings,
    ...options,
  });
};

export const useSystemConfig = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.settings(),
    queryFn: api.getSystemConfig,
    ...options,
  });
};

export const useFeatureFlags = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.features(),
    queryFn: api.getFeatureFlags,
    ...options,
  });
};

export const useFeatureUsage = (featureName, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.features(), 'usage', featureName],
    queryFn: () => api.getFeatureUsage(featureName),
    enabled: !!featureName,
    ...options,
  });
};

// ============================================
// Backups Queries
// ============================================

export const useBackups = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.backups(),
    queryFn: api.getBackups,
    ...options,
  });
};

export const useDatabaseBackups = (options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.database(), 'backups'],
    queryFn: api.getDatabaseBackupList,
    ...options,
  });
};

export const useDatabaseStatus = (options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.database(), 'status'],
    queryFn: api.getDatabaseStatus,
    refetchInterval: 60000,
    ...options,
  });
};

export const useMaintenanceStatus = (options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.systemHealth(), 'maintenance'],
    queryFn: api.getMaintenanceStatus,
    ...options,
  });
};

// ============================================
// Notifications Queries
// ============================================

export const useNotifications = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.notifications(), params],
    queryFn: () => api.getNotifications(params),
    ...options,
  });
};

// ============================================
// Analytics Queries
// ============================================

export const useGlobalAnalytics = (params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.analytics(), params],
    queryFn: () => api.getGlobalAnalytics(params),
    ...options,
  });
};

export const useSchoolAnalytics = (schoolId, params = {}, options = {}) => {
  return useQuery({
    queryKey: [...superAdminKeys.analytics(), 'school', schoolId, params],
    queryFn: () => api.getSchoolAnalytics(schoolId, params),
    enabled: !!schoolId,
    ...options,
  });
};

// ============================================
// API Keys & Integrations Queries
// ============================================

export const useApiKeys = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.apiKeys(),
    queryFn: api.getApiKeys,
    ...options,
  });
};

export const useIntegrations = (options = {}) => {
  return useQuery({
    queryKey: superAdminKeys.integrations(),
    queryFn: api.getIntegrations,
    ...options,
  });
};

// ============================================
// Mutations - Schools
// ============================================

export const useCreateSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createSchool,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() });
    },
  });
};

export const useUpdateSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ schoolId, data }) => api.updateSchool(schoolId, data),
    onSuccess: (_, { schoolId }) => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() });
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schoolById(schoolId) });
    },
  });
};

export const useDeleteSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteSchool,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() });
    },
  });
};

export const useActivateSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.activateSchool,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() });
    },
  });
};

export const useDeactivateSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deactivateSchool,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() });
    },
  });
};

export const useToggleSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ schoolId, action }) => 
      action === 'activate' ? api.activateSchool(schoolId) : api.deactivateSchool(schoolId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() });
    },
  });
};

// ============================================
// Mutations - Users
// ============================================

export const useUpdateGlobalUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ userId, data }) => api.updateGlobalUser(userId, data),
    onSuccess: (_, { userId }) => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.users() });
      queryClient.invalidateQueries({ queryKey: superAdminKeys.userById(userId) });
    },
  });
};

export const useDeleteGlobalUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteGlobalUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.users() });
    },
  });
};

export const useActivateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.activateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.users() });
    },
  });
};

export const useDeactivateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deactivateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.users() });
    },
  });
};

// ============================================
// Mutations - Roles
// ============================================

export const useCreateRole = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createRole,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.roles() });
    },
  });
};

export const useUpdateRole = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ roleId, data }) => api.updateRole(roleId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.roles() });
    },
  });
};

export const useDeleteRole = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteRole,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.roles() });
    },
  });
};

// ============================================
// Mutations - Settings
// ============================================

export const useUpdateSystemSettings = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateSystemSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.settings() });
    },
  });
};

export const useUpdateSystemConfig = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateSystemConfig,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.settings() });
    },
  });
};

export const useToggleFeatureFlag = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ featureName, enabled }) => api.updateFeatureFlag(featureName, enabled),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.features() });
    },
  });
};

export const useToggleFeature = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.toggleFeature,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.features() });
    },
  });
};

// ============================================
// Mutations - Maintenance
// ============================================

export const useToggleMaintenanceMode = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.toggleMaintenanceMode,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.systemHealth() });
    },
  });
};

// ============================================
// Mutations - Backups
// ============================================

export const useCreateBackup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createBackup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.backups() });
    },
  });
};

export const useCreateDatabaseBackup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createDatabaseBackup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [...superAdminKeys.database(), 'backups'] });
    },
  });
};

export const useRestoreDatabaseBackup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.restoreDatabaseBackup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.database() });
    },
  });
};

export const useRunDatabaseMigration = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.runDatabaseMigration,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.database() });
    },
  });
};

// ============================================
// Mutations - Notifications
// ============================================

export const useSendNotification = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.sendNotification,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.notifications() });
    },
  });
};

export const useMarkNotificationRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markNotificationRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.notifications() });
    },
  });
};

export const useDeleteNotification = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteNotification,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.notifications() });
    },
  });
};

// ============================================
// Mutations - API Keys
// ============================================

export const useCreateApiKey = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createApiKey,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.apiKeys() });
    },
  });
};

export const useRevokeApiKey = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.revokeApiKey,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.apiKeys() });
    },
  });
};

// ============================================
// Mutations - Integrations
// ============================================

export const useConfigureIntegration = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ integrationId, data }) => api.configureIntegration(integrationId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: superAdminKeys.integrations() });
    },
  });
};
