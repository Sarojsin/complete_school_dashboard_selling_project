# Implementation Plan - Frontend Missing Services Plan 8: Super Admin Module API Integration

This plan details the comprehensive API integration for the Super Admin Module with multi-school management, analytics, and system controls.

---

## Part 1: Design System

```javascript
// Super Admin Glass Components
.super-admin-card {
  @apply bg-gradient-to-br from-slate-900/90 to-slate-950/90 backdrop-blur-2xl 
         border border-white/5 shadow-2xl rounded-2xl;
}

.system-health-indicator {
  @apply w-3 h-3 rounded-full;
}

.health-good { @apply bg-emerald-500 shadow-glow-green; }
.health-warning { @apply bg-amber-500 shadow-glow-red; }
.health-critical { @apply bg-red-500 animate-pulse; }
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/super_admin/hooks/useSuperAdmin.js

export const superAdminKeys = {
  all: ['superAdmin'] as const,
  schools: () => [...superAdminKeys.all, 'schools'] as const,
  schoolById: (id) => [...superAdminKeys.all, 'schools', id] as const,
  schoolStats: (id) => [...superAdminKeys.all, 'schools', id, 'stats'] as const,
  users: () => [...superAdminKeys.all, 'users'] as const,
  userById: (id) => [...superAdminKeys.all, 'users', id] as const,
  settings: () => [...superAdminKeys.all, 'settings'] as const,
  features: () => [...superAdminKeys.all, 'features'] as const,
  dashboard: () => [...superAdminKeys.all, 'dashboard'] as const,
  systemHealth: () => [...superAdminKeys.all, 'systemHealth'] as const,
  backups: () => [...superAdminKeys.all, 'backups'] as const,
};

export const useAllSchools = (params) => useQuery({
  queryKey: [...superAdminKeys.schools(), params],
  queryFn: () => api.getAllSchools(params),
});

export const useSchoolById = (id) => useQuery({
  queryKey: superAdminKeys.schoolById(id),
  queryFn: () => api.getSchoolById(id),
  enabled: !!id,
});

export const useSchoolStats = (id) => useQuery({
  queryKey: superAdminKeys.schoolStats(id),
  queryFn: () => api.getSchoolStats(id),
  enabled: !!id,
  refetchInterval: 30000,
});

export const useAllUsers = (params) => useQuery({
  queryKey: [...superAdminKeys.users(), params],
  queryFn: () => api.getAllUsers(params),
});

export const useSystemSettings = () => useQuery({
  queryKey: superAdminKeys.settings(),
  queryFn: api.getSystemSettings,
});

export const useFeatureFlags = () => useQuery({
  queryKey: superAdminKeys.features(),
  queryFn: api.getFeatureFlags,
});

export const useDashboardStats = () => useQuery({
  queryKey: superAdminKeys.dashboard(),
  queryFn: api.getDashboardStats,
  refetchInterval: 60000,
});

export const useSystemHealth = () => useQuery({
  queryKey: superAdminKeys.systemHealth(),
  queryFn: api.getSystemHealth,
  refetchInterval: 15000,
});

export const useBackups = () => useQuery({
  queryKey: superAdminKeys.backups(),
  queryFn: api.getBackups,
});

// Mutations
export const useCreateSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createSchool,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() }),
  });
};

export const useToggleSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, action }) => action === 'activate' ? api.activateSchool(id) : api.deactivateSchool(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: superAdminKeys.schools() }),
  });
};

export const useUpdateSettings = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateSystemSettings,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: superAdminKeys.settings() }),
  });
};

export const useToggleFeature = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.toggleFeature,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: superAdminKeys.features() }),
  });
};

export const useCreateBackup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createBackup,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: superAdminKeys.backups() }),
  });
};

export const useToggleMaintenance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ enabled }) => api.toggleMaintenanceMode(enabled),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: superAdminKeys.systemHealth() }),
  });
};
```

---

## Part 3: Components

### 3.1 System Health Monitor

```javascript
const SystemHealthCard = () => {
  const { data: health } = useSystemHealth();
  
  return (
    <div className="super-admin-card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white font-semibold">System Health</h3>
        <div className={`system-health-indicator ${health?.status === 'good' ? 'health-good' : health?.status === 'warning' ? 'health-warning' : 'health-critical'}`} />
      </div>
      <div className="grid grid-cols-2 gap-4">
        {health?.services?.map((service) => (
          <div key={service.name} className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
            <span className="text-white/60 text-sm">{service.name}</span>
            <span className={`text-xs ${service.status === 'up' ? 'text-emerald-400' : 'text-red-400'}`}>
              {service.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 3.2 School Management Table

```javascript
const SchoolsTable = () => {
  const { data: schools, isLoading } = useAllSchools();
  const { mutate: toggleSchool } = useToggleSchool();
  
  return (
    <div className="super-admin-card overflow-hidden">
      <table className="w-full">
        <thead className="bg-white/5">
          <tr>
            <th className="text-left text-white/60 p-4">School</th>
            <th className="text-left text-white/60 p-4">Users</th>
            <th className="text-left text-white/60 p-4">Status</th>
            <th className="text-left text-white/60 p-4">Actions</th>
          </tr>
        </thead>
        <tbody>
          {schools?.map((school) => (
            <motion.tr
              key={school.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="border-t border-white/5"
            >
              <td className="p-4 text-white">{school.name}</td>
              <td className="p-4 text-white/60">{school.userCount}</td>
              <td className="p-4">
                <span className={`px-2 py-1 rounded-full text-xs ${
                  school.active ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                }`}>
                  {school.active ? 'Active' : 'Inactive'}
                </span>
              </td>
              <td className="p-4">
                <button
                  onClick={() => toggleSchool({ id: school.id, action: school.active ? 'deactivate' : 'activate' })}
                  className="text-white/60 hover:text-white"
                >
                  {school.active ? 'Deactivate' : 'Activate'}
                </button>
              </td>
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query | 9 query hooks + 6 mutations |
| System Health | Real-time monitoring with indicators |
| School Management | Activation/deactivation with optimistic updates |

---

*Last Updated: 2026-03-29*
