# Implementation Plan - Frontend Missing Services Plan 3: Authority Module API Integration

This plan details the comprehensive API integration for the Authority & Admin Portal, focusing on connecting all missing backend endpoints to the frontend with a premium glassmorphic "Command Center" design.

---

## Part 1: Design System Configuration

### 1.1 Authority-Specific Tailwind Configuration

```javascript
// tailwind.config.js - Authority Module
module.exports = {
  theme: {
    extend: {
      colors: {
        authority: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',    // Sky blue
          600: '#0284c7',
          700: '#0369a1',
          danger: '#dc2626',
          success: '#16a34a',
          warning: '#ca8a04',
        }
      },
      boxShadow: {
        'glow-blue': '0 0 20px rgba(14, 165, 233, 0.3)',
        'glow-green': '0 0 20px rgba(22, 163, 74, 0.3)',
        'glow-red': '0 0 20px rgba(220, 38, 38, 0.3)',
      }
    }
  }
}
```

### 1.2 Authority Glass Components

```css
.authority-card {
  @apply bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl 
         border border-white/10 shadow-2xl rounded-2xl;
}

.authority-table {
  @apply w-full border-collapse;
}

.authority-table th {
  @apply text-left text-white/60 text-sm font-medium px-4 py-3 border-b border-white/10;
}

.authority-table td {
  @apply px-4 py-3 border-b border-white/5 text-white;
}

.authority-table tr:hover td {
  @apply bg-white/5;
}

.admin-stat-card {
  @apply authority-card p-6 relative overflow-hidden;
}

.admin-stat-card::after {
  content: '';
  @apply absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-current to-transparent;
}
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_authority/hooks/useAuthority.js

// === QUERY KEYS ===
export const authorityKeys = {
  all: ['authority'] as const,
  students: () => [...authorityKeys.all, 'students'] as const,
  studentById: (id) => [...authorityKeys.all, 'students', id] as const,
  teachers: () => [...authorityKeys.all, 'teachers'] as const,
  teacherById: (id) => [...authorityKeys.all, 'teachers', id] as const,
  courses: () => [...authorityKeys.all, 'courses'] as const,
  courseById: (id) => [...authorityKeys.all, 'courses', id] as const,
  departments: () => [...authorityKeys.all, 'departments'] as const,
  fees: () => [...authorityKeys.all, 'fees'] as const,
  feeById: (id) => [...authorityKeys.all, 'fees', id] as const,
  feeStructure: () => [...authorityKeys.all, 'fee-structure'] as const,
  notices: () => [...authorityKeys.all, 'notices'] as const,
  noticeById: (id) => [...authorityKeys.all, 'notices', id] as const,
  dashboard: () => [...authorityKeys.all, 'dashboard'] as const,
  analytics: (type) => [...authorityKeys.all, 'analytics', type] as const,
};

// === QUERY HOOKS ===
export const useAllStudents = (params) => useQuery({
  queryKey: [...authorityKeys.students(), params],
  queryFn: () => api.getAllStudents(params),
  staleTime: 5 * 60 * 1000,
});

export const useStudentById = (id) => useQuery({
  queryKey: authorityKeys.studentById(id),
  queryFn: () => api.getStudentById(id),
  enabled: !!id,
});

export const useAllTeachers = (params) => useQuery({
  queryKey: [...authorityKeys.teachers(), params],
  queryFn: () => api.getAllTeachers(params),
  staleTime: 5 * 60 * 1000,
});

export const useTeacherById = (id) => useQuery({
  queryKey: authorityKeys.teacherById(id),
  queryFn: () => api.getTeacherById(id),
  enabled: !!id,
});

export const useAllCourses = (params) => useQuery({
  queryKey: [...authorityKeys.courses(), params],
  queryFn: () => api.getAllCourses(params),
  staleTime: 10 * 60 * 1000,
});

export const useAllDepartments = () => useQuery({
  queryKey: authorityKeys.departments(),
  queryFn: api.getAllDepartments,
  staleTime: 10 * 60 * 1000,
});

export const useAllFees = (params) => useQuery({
  queryKey: [...authorityKeys.fees(), params],
  queryFn: () => api.getAllFees(params),
  staleTime: 5 * 60 * 1000,
});

export const useFeeStructure = () => useQuery({
  queryKey: authorityKeys.feeStructure(),
  queryFn: api.getFeeStructure,
  staleTime: 10 * 60 * 1000,
});

export const useAllNotices = (params) => useQuery({
  queryKey: [...authorityKeys.notices(), params],
  queryFn: () => api.getAllNotices(params),
  staleTime: 5 * 60 * 1000,
});

export const useDashboardStats = () => useQuery({
  queryKey: authorityKeys.dashboard(),
  queryFn: api.getDashboardStats,
  staleTime: 5 * 60 * 1000,
});

export const useEnrollmentStats = (params) => useQuery({
  queryKey: authorityKeys.analytics('enrollment'),
  queryFn: () => api.getEnrollmentStats(params),
  staleTime: 10 * 60 * 1000,
});

export const useRevenueStats = (params) => useQuery({
  queryKey: authorityKeys.analytics('revenue'),
  queryFn: () => api.getRevenueStats(params),
  staleTime: 10 * 60 * 1000,
});
```

### 2.2 Mutation Hooks

```javascript
// === MUTATIONS ===
export const useCreateStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      successToast('Student created successfully');
    },
    onError: () => errorToast('Failed to create student'),
  });
};

export const useUpdateStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateStudent(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      successToast('Student updated successfully');
    },
  });
};

export const useDeleteStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      successToast('Student deleted');
    },
  });
};

export const useBulkCreateStudents = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkCreateStudents,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
    },
  });
};

export const useCreateTeacher = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createTeacher,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.teachers() });
    },
  });
};

export const useCreateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createCourse,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.courses() });
    },
  });
};

export const useCreateFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createFee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
    },
  });
};

export const useCreateNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createNotice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.notices() });
    },
  });
};
```

---

## Part 3: Feedback Components

### 3.1 Authority Skeleton Components

```javascript
export const AuthorityDashboardSkeleton = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="authority-card p-6">
          <div className="shimmer-skeleton h-4 w-24 mb-4" />
          <div className="shimmer-skeleton h-8 w-16" />
        </div>
      ))}
    </div>
    <div className="authority-card p-6">
      <div className="shimmer-skeleton h-6 w-48 mb-4" />
      <div className="space-y-3">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="shimmer-skeleton h-12 w-full" />
        ))}
      </div>
    </div>
  </div>
);

export const DataTableSkeleton = ({ rows = 5 }) => (
  <div className="authority-card p-0 overflow-hidden">
    <div className="shimmer-skeleton h-12 w-full border-b border-white/10" />
    {[...Array(rows)].map((_, i) => (
      <div key={i} className="shimmer-skeleton h-16 w-full border-b border-white/5" />
    ))}
  </div>
);
```

### 3.2 Authority Toast Notifications

```javascript
export const authorityToast = {
  student: {
    create: { success: 'Student created successfully', error: 'Failed to create student' },
    update: { success: 'Student updated', error: 'Failed to update student' },
    delete: { success: 'Student deleted', error: 'Failed to delete student' },
    bulk: { success: 'Students imported successfully', error: 'Failed to import students' },
  },
  teacher: {
    create: { success: 'Teacher added', error: 'Failed to add teacher' },
    update: { success: 'Teacher updated', error: 'Failed to update teacher' },
    delete: { success: 'Teacher removed', error: 'Failed to remove teacher' },
  },
  course: {
    create: { success: 'Course created', error: 'Failed to create course' },
    update: { success: 'Course updated', error: 'Failed to update course' },
  },
  fee: {
    create: { success: 'Fee structure updated', error: 'Failed to update fees' },
  },
  notice: {
    create: { success: 'Notice published', error: 'Failed to publish notice' },
    delete: { success: 'Notice removed', error: 'Failed to remove notice' },
  },
};
```

---

## Part 4: High-Fidelity Authority Components

### 4.1 Admin Command Center Dashboard

```javascript
// frontend/src/modules/school/school_authority/components/AuthorityDashboard.jsx
import { motion } from 'framer-motion';

// === ANALYTICS CHART CARD ===
const AnalyticsCard = ({ title, children, delay = 0 }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay }}
    className="authority-card p-6"
  >
    <h3 className="text-white font-semibold mb-4">{title}</h3>
    {children}
  </motion.div>
);

// === STAT CARD WITH TREND ===
const StatCard = ({ label, value, trend, trendValue, color = 'blue', icon: Icon, delay = 0 }) => {
  const colors = {
    blue: 'from-authority-500/20 to-authority-600/10 border-authority-500/30',
    green: 'from-green-500/20 to-green-600/10 border-green-500/30',
    red: 'from-red-500/20 to-red-600/10 border-red-500/30',
    amber: 'from-amber-500/20 to-amber-600/10 border-amber-500/30',
  };
  
  const iconColors = {
    blue: 'text-authority-400',
    green: 'text-green-400',
    red: 'text-red-400',
    amber: 'text-amber-400',
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay }}
      className={`authority-card p-6 bg-gradient-to-br ${colors[color]} border`}
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-white/60 text-sm">{label}</p>
          <p className="text-3xl font-bold text-white mt-2">{value}</p>
          {trend && (
            <p className={`text-sm mt-2 ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
              {trend === 'up' ? '↑' : '↓'} {trendValue}% from last month
            </p>
          )}
        </div>
        {Icon && <Icon className={`w-8 h-8 ${iconColors[color]}`} />}
      </div>
    </motion.div>
  );
};

// === DATA TABLE WITH SEARCH ===
export const DataTable = ({ columns, data, onRowClick, loading }) => (
  <div className="authority-card overflow-hidden">
    <table className="authority-table">
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key}>{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {loading ? (
          <tr><td colSpan={columns.length} className="text-center py-8"><DataTableSkeleton /></td></tr>
        ) : data?.length === 0 ? (
          <tr><td colSpan={columns.length} className="text-center py-8 text-white/40">No data available</td></tr>
        ) : (
          data.map((row, index) => (
            <motion.tr
              key={row.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: index * 0.05 }}
              onClick={() => onRowClick?.(row)}
              className="cursor-pointer"
            >
              {columns.map((col) => (
                <td key={col.key}>{col.render ? col.render(row[col.key], row) : row[col.key]}</td>
              ))}
            </motion.tr>
          ))
        )}
      </tbody>
    </table>
  </div>
);

// === MAIN AUTHORITY DASHBOARD ===
export const AuthorityDashboard = () => {
  const { data: stats, isLoading } = useDashboardStats();
  const { data: enrollment } = useEnrollmentStats();
  const { data: revenue } = useRevenueStats();
  
  if (isLoading) return <AuthorityDashboardSkeleton />;
  
  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="authority-card p-8 bg-gradient-to-r from-authority-900/50 to-purple-900/50"
      >
        <h1 className="text-3xl font-bold text-white">Admin Command Center</h1>
        <p className="text-white/60 mt-2">School Management Dashboard</p>
      </motion.div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard label="Total Students" value={stats?.totalStudents || 0} trend="up" trendValue={12} color="blue" icon={Users} delay={0} />
        <StatCard label="Total Teachers" value={stats?.totalTeachers || 0} trend="up" trendValue={5} color="green" icon={UserCheck} delay={0.1} />
        <StatCard label="Total Revenue" value={`$${stats?.revenue?.toLocaleString() || 0}`} trend="up" trendValue={8} color="amber" icon={DollarSign} delay={0.2} />
        <StatCard label="Active Courses" value={stats?.activeCourses || 0} color="blue" icon={BookOpen} delay={0.3} />
      </div>
      
      {/* Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnalyticsCard title="Enrollment Trends" delay={0.4}>
          {/* Enrollment Chart */}
          <div className="h-48 flex items-end gap-2">
            {enrollment?.monthly?.map((value, i) => (
              <motion.div
                key={i}
                initial={{ height: 0 }}
                animate={{ height: `${value}%` }}
                transition={{ delay: 0.5 + i * 0.1, duration: 0.5 }}
                className="flex-1 bg-gradient-to-t from-authority-500 to-authority-400 rounded-t-lg"
              />
            ))}
          </div>
        </AnalyticsCard>
        
        <AnalyticsCard title="Revenue Overview" delay={0.5}>
          {/* Revenue Chart */}
          <div className="space-y-4">
            {revenue?.sources?.map((source, i) => (
              <div key={source.name} className="flex items-center gap-4">
                <span className="text-white/60 w-24 text-sm">{source.name}</span>
                <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${source.percentage}%` }}
                    transition={{ delay: 0.6 + i * 0.1 }}
                    className="h-full bg-gradient-to-r from-authority-500 to-authority-400 rounded-full"
                  />
                </div>
                <span className="text-white text-sm w-16 text-right">${source.amount}</span>
              </div>
            ))}
          </div>
        </AnalyticsCard>
      </div>
      
      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Add Student', icon: UserPlus, action: 'student' },
          { label: 'Add Teacher', icon: UserCheck, action: 'teacher' },
          { label: 'Create Course', icon: BookOpen, action: 'course' },
          { label: 'Publish Notice', icon: Bell, action: 'notice' },
        ].map((action, i) => (
          <motion.button
            key={action.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 + i * 0.1 }}
            className="authority-card p-4 hover:bg-white/10 transition-colors text-center"
          >
            <action.icon className="w-6 h-6 text-authority-400 mx-auto mb-2" />
            <span className="text-white text-sm">{action.label}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
};
```

---

## Part 5: Execution Strategy

### 5.1 Sidebar Navigation with Collapsible Sections

```javascript
const adminNavSections = [
  {
    title: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    ]
  },
  {
    title: 'User Management',
    items: [
      { id: 'students', label: 'Students', icon: Users },
      { id: 'teachers', label: 'Teachers', icon: UserCheck },
      { id: 'parents', label: 'Parents', icon: Family },
    ]
  },
  {
    title: 'Academic',
    items: [
      { id: 'courses', label: 'Courses', icon: BookOpen },
      { id: 'classes', label: 'Classes', icon: LayoutGrid },
      { id: 'timetable', label: 'Timetable', icon: Calendar },
    ]
  },
  {
    title: 'Finance',
    items: [
      { id: 'fees', label: 'Fees', icon: DollarSign },
      { id: 'payments', label: 'Payments', icon: CreditCard },
    ]
  },
];
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query Hooks | 12 query hooks + 8 mutation hooks |
| Tailwind Config | Authority colors, glow shadows |
| Framer Motion | Animated stats, charts, tables |
| Toast Notifications | Student, teacher, course, fee, notice toasts |
| Components | Command center dashboard, data tables, analytics |

---

*Last Updated: 2026-03-29*
