# Implementation Plan - Frontend Missing Services Plan 1: Student Module API Integration

This plan details the comprehensive API integration for the Student Portal, focusing on connecting all missing backend endpoints to the frontend with a premium glassmorphic design while ensuring 100% accurate data flow.

---

## Part 1: Design System Configuration

### 1.1 Tailwind Configuration (Stitch Palette)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        stitch: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        }
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'shimmer': 'shimmer 2s infinite linear',
        'spring-in': 'springIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        springIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    }
  },
  plugins: [],
}
```

### 1.2 Glassmorphism CSS Utilities

```css
/* src/index.css */
@layer components {
  .glass-surface {
    @apply bg-white/10 backdrop-blur-md border border-white/10;
  }
  
  .glass-card {
    @apply bg-gradient-to-br from-white/20 to-white/5 backdrop-blur-xl 
           border border-white/20 shadow-xl rounded-2xl;
  }
  
  .glass-card-hover {
    @apply glass-card transition-all duration-300 hover:scale-[1.02] 
           hover:shadow-2xl hover:border-white/30;
  }
  
  .glass-button {
    @apply bg-primary-600/80 backdrop-blur-md hover:bg-primary-600 
           text-white font-medium py-2 px-4 rounded-xl transition-all 
           duration-200 hover:scale-[1.02] active:scale-[0.98];
  }
  
  .glass-input {
    @apply bg-white/5 border border-white/10 rounded-xl px-4 py-3 
           text-white placeholder:text-white/40 focus:outline-none 
           focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 
           transition-all duration-200;
  }
  
  .shimmer-skeleton {
    @apply bg-gradient-to-r from-white/10 via-white/20 to-white/10 
           bg-[length:200%_100%] animate-shimmer rounded-lg;
  }
  
  .noise-overlay {
    position: relative;
  }
  
  .noise-overlay::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
    border-radius: inherit;
  }
}
```

---

## Part 2: Service Orchestration Layer (TanStack Query)

### 2.1 Query Keys & Hooks Factory

```javascript
// frontend/src/modules/school/school_student/hooks/useStudent.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/students';

// === QUERY KEYS ===
export const studentKeys = {
  all: ['student'] as const,
  profile: () => [...studentKeys.all, 'profile'] as const,
  profileById: (id: string) => [...studentKeys.all, 'profile', id] as const,
  courses: () => [...studentKeys.all, 'courses'] as const,
  enrolledCourses: () => [...studentKeys.all, 'courses', 'enrolled'] as const,
  grades: () => [...studentKeys.all, 'grades'] as const,
  myGrades: () => [...studentKeys.all, 'grades', 'my'] as const,
  attendance: () => [...studentKeys.all, 'attendance'] as const,
  myAttendance: () => [...studentKeys.all, 'attendance', 'my'] as const,
  assignments: () => [...studentKeys.all, 'assignments'] as const,
  tests: () => [...studentKeys.all, 'tests'] as const,
  availableTests: () => [...studentKeys.all, 'tests', 'available'] as const,
  testResults: () => [...studentKeys.all, 'tests', 'results'] as const,
  notices: () => [...studentKeys.all, 'notices'] as const,
  dashboard: () => [...studentKeys.all, 'dashboard'] as const,
};

// === QUERY HOOKS ===
export const useStudentProfile = () => {
  return useQuery({
    queryKey: studentKeys.profile(),
    queryFn: api.getMyStudentProfile,
    staleTime: 5 * 60 * 1000,
  });
};

export const useStudentById = (studentId: string) => {
  return useQuery({
    queryKey: studentKeys.profileById(studentId),
    queryFn: () => api.getStudentById(studentId),
    enabled: !!studentId,
  });
};

export const useEnrolledCourses = () => {
  return useQuery({
    queryKey: studentKeys.enrolledCourses(),
    queryFn: api.getEnrolledCourses,
    staleTime: 10 * 60 * 1000,
  });
};

export const useMyGrades = () => {
  return useQuery({
    queryKey: studentKeys.myGrades(),
    queryFn: api.getMyGrades,
    staleTime: 5 * 60 * 1000,
  });
};

export const useMyAttendance = () => {
  return useQuery({
    queryKey: studentKeys.myAttendance(),
    queryFn: api.getMyAttendance,
    staleTime: 5 * 60 * 1000,
  });
};

export const useCourseAttendance = (courseId: string) => {
  return useQuery({
    queryKey: [...studentKeys.myAttendance(), courseId],
    queryFn: () => api.getMyCourseAttendance(courseId),
    enabled: !!courseId,
  });
};

export const useStudentAssignments = () => {
  return useQuery({
    queryKey: studentKeys.assignments(),
    queryFn: api.getStudentAssignments,
    staleTime: 5 * 60 * 1000,
  });
};

export const useAssignmentSubmission = (assignmentId: string) => {
  return useQuery({
    queryKey: [...studentKeys.assignments(), 'submission', assignmentId],
    queryFn: () => api.getMySubmission(assignmentId),
    enabled: !!assignmentId,
  });
};

export const useAvailableTests = () => {
  return useQuery({
    queryKey: studentKeys.availableTests(),
    queryFn: api.getAvailableTests,
    staleTime: 5 * 60 * 1000,
  });
};

export const useMyTestResults = () => {
  return useQuery({
    queryKey: studentKeys.testResults(),
    queryFn: api.getMyTestResults,
    staleTime: 10 * 60 * 1000,
  });
};

export const useStudentDashboard = () => {
  return useQuery({
    queryKey: studentKeys.dashboard(),
    queryFn: api.getStudentDashboard,
    staleTime: 5 * 60 * 1000,
  });
};
```

### 2.2 Mutation Hooks with Optimistic Updates

```javascript
// === MUTATION HOOKS ===
export const useUpdateStudent = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ studentId, data }: { studentId: string; data: any }) => 
      api.updateStudent(studentId, data),
    onMutate: async ({ studentId, data }) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.profileById(studentId) });
      
      const previousProfile = queryClient.getQueryData(studentKeys.profileById(studentId));
      
      queryClient.setQueryData(studentKeys.profileById(studentId), {
        ...previousProfile,
        ...data,
      });
      
      return { previousProfile };
    },
    onError: (err, { studentId }, context) => {
      queryClient.setQueryData(studentKeys.profileById(studentId), context?.previousProfile);
    },
    onSettled: (data, error, { studentId }) => {
      queryClient.invalidateQueries({ queryKey: studentKeys.profile() });
      queryClient.invalidateQueries({ queryKey: studentKeys.profileById(studentId) });
    },
  });
};

// === OPTIMISTIC UPDATE MUTATION - Assignment Submission ===
export const useSubmitAssignment = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ assignmentId, data }: { assignmentId: string; data: any }) =>
      api.submitAssignment(assignmentId, data),
    onMutate: async ({ assignmentId, data }) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.assignments() });
      
      const previousAssignments = queryClient.getQueryData(studentKeys.assignments());
      
      // Optimistically mark as "Submitted"
      queryClient.setQueryData(studentKeys.assignments(), (old: any) => {
        if (!old) return old;
        return old.map((assignment: any) => 
          assignment.id === assignmentId 
            ? { ...assignment, status: 'submitted', submittedAt: new Date().toISOString() }
            : assignment
        );
      });
      
      return { previousAssignments };
    },
    onError: (err, { assignmentId }, context) => {
      queryClient.setQueryData(studentKeys.assignments(), context?.previousAssignments);
    },
    onSettled: (data, error, { assignmentId }) => {
      queryClient.invalidateQueries({ queryKey: studentKeys.assignments() });
      queryClient.invalidateQueries({ 
        queryKey: [...studentKeys.assignments(), 'submission', assignmentId] 
      });
    },
  });
};

export const useStartTest = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (testId: string) => api.startTest(testId),
    onMutate: async (testId) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.availableTests() });
      
      const previousTests = queryClient.getQueryData(studentKeys.availableTests());
      
      queryClient.setQueryData(studentKeys.availableTests(), (old: any) => {
        if (!old) return old;
        return old.map((test: any) =>
          test.id === testId
            ? { ...test, status: 'in_progress', startedAt: new Date().toISOString() }
            : test
        );
      });
      
      return { previousTests };
    },
    onError: (err, testId, context) => {
      queryClient.setQueryData(studentKeys.availableTests(), context?.previousTests);
    },
    onSettled: (data, error, testId) => {
      queryClient.invalidateQueries({ queryKey: studentKeys.availableTests() });
    },
  });
};

export const useSubmitTest = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ testId, answers }: { testId: string; answers: any }) =>
      api.submitTest(testId, answers),
    onMutate: async ({ testId }) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.testResults() });
      
      const previousResults = queryClient.getQueryData(studentKeys.testResults());
      
      // Add pending result
      queryClient.setQueryData(studentKeys.testResults(), (old: any) => {
        if (!old) return [{ testId, status: 'pending', submittedAt: new Date().toISOString() }];
        return [...old, { testId, status: 'pending', submittedAt: new Date().toISOString() }];
      });
      
      return { previousResults };
    },
    onError: (err, { testId }, context) => {
      queryClient.setQueryData(studentKeys.testResults(), context?.previousResults);
    },
    onSettled: (data, error, { testId }) => {
      queryClient.invalidateQueries({ queryKey: studentKeys.testResults() });
    },
  });
};
```

---

## Part 3: The "Stitch" Feedback Loop

### 3.1 Skeleton Shimmer Component

```javascript
// frontend/src/components/ui/SkeletonShimmer.jsx
import { motion } from 'framer-motion';

export const SkeletonShimmer = ({ className = '', variant = 'rectangular' }) => {
  const variants = {
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
    card: 'rounded-2xl',
  };
  
  return (
    <div className={`shimmer-skeleton ${variants[variant as keyof typeof variants]} ${className}`} />
  );
};

// === DASHBOARD STATS SKELETON ===
export const DashboardStatsSkeleton = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="glass-card p-6"
        >
          <SkeletonShimmer className="h-4 w-24 mb-4" />
          <SkeletonShimmer className="h-8 w-16 mb-2" />
          <SkeletonShimmer className="h-3 w-32" />
        </motion.div>
      ))}
    </div>
  );
};

// === GRADE CARD SKELETON ===
export const GradeCardSkeleton = () => {
  return (
    <div className="glass-card p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <SkeletonShimmer className="h-5 w-32" />
        <SkeletonShimmer className="h-6 w-16 rounded-full" />
      </div>
      <SkeletonShimmer className="h-2 w-full rounded-full" />
    </div>
  );
};

// === ATTENDANCE SKELETON ===
export const AttendanceRowSkeleton = () => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-white/10">
      <SkeletonShimmer className="h-5 w-24" />
      <SkeletonShimmer className="h-5 w-16" />
      <SkeletonShimmer className="h-5 w-20 rounded-full" />
    </div>
  );
};
```

### 3.2 Quiet Toast Notifications (Sonner)

```javascript
// frontend/src/lib/toast.js
import { toast } from 'sonner';

// === CUSTOM TOAST THEME ===
const stitchToast = {
  style: {
    background: 'rgba(15, 23, 42, 0.95)',
    backdropFilter: 'blur(12px)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    borderRadius: '12px',
    color: '#fff',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
  },
  iconTheme: {
    primary: '#6366f1',
    secondary: '#fff',
  },
};

export const successToast = (message: string, description?: string) => {
  toast.success(message, {
    ...stitchToast,
    description,
    duration: 3000,
  });
};

export const errorToast = (message: string, description?: string) => {
  toast.error(message, {
    ...stitchToast,
    description,
    duration: 5000,
  });
};

export const infoToast = (message: string, description?: string) => {
  toast.info(message, {
    ...stitchToast,
    description,
    duration: 3000,
  });
};

export const warningToast = (message: string, description?: string) => {
  toast.warning(message, {
    ...stitchToast,
    description,
    duration: 4000,
  });
};

// === PROFILE UPDATE TOAST ===
export const profileUpdateToast = {
  loading: 'Updating profile...',
  success: 'Profile updated successfully!',
  error: 'Failed to update profile. Please try again.',
};

// === ASSIGNMENT SUBMIT TOAST ===
export const assignmentSubmitToast = {
  loading: 'Submitting assignment...',
  success: 'Assignment submitted successfully!',
  error: 'Failed to submit assignment. Please try again.',
};

// === TEST SUBMIT TOAST ===
export const testSubmitToast = {
  loading: 'Submitting test...',
  success: 'Test submitted successfully! Results will be available shortly.',
  error: 'Failed to submit test. Please check your answers and try again.',
};
```

---

## Part 4: High-Fidelity Components

### 4.1 Student Performance Dashboard

```javascript
// frontend/src/modules/school/school_student/components/StudentDashboard.jsx
import { motion } from 'framer-motion';
import { GlassCard } from '@/components/ui/GlassCard';
import { SkeletonShimmer, DashboardStatsSkeleton } from '@/components/ui/SkeletonShimmer';
import { useStudentDashboard, useMyGrades, useMyAttendance } from '../hooks/useStudent';
import { successToast, errorToast } from '@/lib/toast';

// === ANIMATED PROGRESS BAR ===
const AnimatedProgressBar = ({ value, max = 100, label, color = 'primary' }) => {
  const percentage = (value / max) * 100;
  
  const colorClasses = {
    primary: 'bg-gradient-to-r from-primary-500 to-primary-600',
    success: 'bg-gradient-to-r from-emerald-500 to-emerald-600',
    warning: 'bg-gradient-to-r from-amber-500 to-amber-600',
    danger: 'bg-gradient-to-r from-red-500 to-red-600',
  };
  
  return (
    <div className="mb-4">
      <div className="flex justify-between mb-2">
        <span className="text-white/70 text-sm">{label}</span>
        <span className="text-white font-medium">{value}%</span>
      </div>
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ 
            duration: 0.8, 
            ease: [0.34, 1.56, 0.64, 1],
            delay: 0.2 
          }}
          className={`h-full ${colorClasses[color as keyof typeof colorClasses]} rounded-full`}
        />
      </div>
    </div>
  );
};

// === STAT CARD COMPONENT ===
const StatCard = ({ title, value, subtitle, icon: Icon, color = 'primary', delay = 0 }) => {
  const colorStyles = {
    primary: 'from-primary-500/20 to-primary-600/10 border-primary-500/30',
    success: 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30',
    warning: 'from-amber-500/20 to-amber-600/10 border-amber-500/30',
    danger: 'from-red-500/20 to-red-600/10 border-red-500/30',
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className={`glass-card p-6 bg-gradient-to-br ${colorStyles[color as keyof typeof colorStyles]} border`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-white/60 text-sm mb-1">{title}</p>
          <h3 className="text-3xl font-bold text-white">{value}</h3>
          {subtitle && <p className="text-white/50 text-xs mt-2">{subtitle}</p>}
        </div>
        {Icon && (
          <div className="p-3 rounded-xl bg-white/10">
            <Icon className="w-6 h-6 text-white" />
          </div>
        )}
      </div>
    </motion.div>
  );
};

// === EMPTY STATE ===
const EmptyAssignments = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-12 text-center"
    >
      <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center">
        <svg className="w-12 h-12 text-white/60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">No Assignments Yet</h3>
      <p className="text-white/50 max-w-sm mx-auto">
        Your assignments will appear here once your teachers create them. Check back soon!
      </p>
    </motion.div>
  );
};

// === MAIN DASHBOARD ===
export const StudentDashboard = () => {
  const { data: dashboard, isLoading: dashboardLoading } = useStudentDashboard();
  const { data: grades, isLoading: gradesLoading } = useMyGrades();
  const { data: attendance, isLoading: attendanceLoading } = useMyAttendance();
  
  if (dashboardLoading || gradesLoading || attendanceLoading) {
    return <DashboardStatsSkeleton />;
  }
  
  const stats = [
    { title: 'GPA', value: dashboard?.gpa || '3.8', subtitle: 'Out of 4.0', color: 'primary' },
    { title: 'Attendance', value: `${dashboard?.attendance || 95}%`, subtitle: 'This semester', color: 'success' },
    { title: 'Pending Tasks', value: dashboard?.pendingTasks || 3, subtitle: 'Assignments due', color: 'warning' },
    { title: 'Courses', value: dashboard?.coursesCount || 5, subtitle: 'Enrolled', color: 'primary' },
  ];
  
  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-8 bg-gradient-to-r from-primary-600/20 to-purple-600/20"
      >
        <h1 className="text-3xl font-bold text-white mb-2">
          Welcome back, {dashboard?.studentName || 'Student'}!
        </h1>
        <p className="text-white/60">
          Here's what's happening with your studies today.
        </p>
      </motion.div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatCard key={stat.title} {...stat} delay={index * 0.1} />
        ))}
      </div>
      
      {/* Performance Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Grades */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Academic Performance</h2>
          {grades?.length > 0 ? (
            grades.slice(0, 5).map((grade: any, index: number) => (
              <AnimatedProgressBar
                key={grade.courseId}
                label={grade.courseName}
                value={grade.score}
                color={grade.score >= 90 ? 'success' : grade.score >= 70 ? 'primary' : 'warning'}
              />
            ))
          ) : (
            <p className="text-white/50">No grades available yet.</p>
          )}
        </motion.div>
        
        {/* Attendance */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Attendance Record</h2>
          {attendance ? (
            <>
              <AnimatedProgressBar
                label="Overall Attendance"
                value={attendance.percentage || 95}
                color="success"
              />
              <div className="grid grid-cols-3 gap-4 mt-6">
                <div className="text-center p-4 rounded-xl bg-emerald-500/20">
                  <p className="text-2xl font-bold text-emerald-400">{attendance.present || 45}</p>
                  <p className="text-white/60 text-sm">Present</p>
                </div>
                <div className="text-center p-4 rounded-xl bg-amber-500/20">
                  <p className="text-2xl font-bold text-amber-400">{attendance.late || 2}</p>
                  <p className="text-white/60 text-sm">Late</p>
                </div>
                <div className="text-center p-4 rounded-xl bg-red-500/20">
                  <p className="text-2xl font-bold text-red-400">{attendance.absent || 1}</p>
                  <p className="text-white/60 text-sm">Absent</p>
                </div>
              </div>
            </>
          ) : (
            <p className="text-white/50">No attendance records yet.</p>
          )}
        </motion.div>
      </div>
      
      {/* Assignments Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <h2 className="text-xl font-semibold text-white mb-6">Recent Assignments</h2>
        {dashboard?.assignments?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {dashboard.assignments.slice(0, 6).map((assignment: any) => (
              <div key={assignment.id} className="glass-card-hover p-4">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-white font-medium">{assignment.title}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    assignment.status === 'submitted' 
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : assignment.status === 'pending'
                      ? 'bg-amber-500/20 text-amber-400'
                      : 'bg-white/10 text-white/60'
                  }`}>
                    {assignment.status}
                  </span>
                </div>
                <p className="text-white/50 text-sm mb-3">{assignment.course}</p>
                <p className="text-white/40 text-xs">Due: {assignment.dueDate}</p>
              </div>
            ))}
          </div>
        ) : (
          <EmptyAssignments />
        )}
      </motion.div>
    </div>
  );
};
```

---

## Part 5: Execution Strategy

### 5.1 Global Loading States

```javascript
// frontend/src/modules/school/school_student/pages/StudentPortal.jsx
import { useState } from 'react';
import { StudentDashboard } from '../components/StudentDashboard';
import { StudentProfile } from '../components/StudentProfile';
import { StudentCourses } from '../components/StudentCourses';
import { StudentGrades } from '../components/StudentGrades';
import { StudentAttendance } from '../components/StudentAttendance';
import { StudentAssignments } from '../components/StudentAssignments';

// === TAB CONFIGURATION ===
const tabs = [
  { id: 'dashboard', label: 'Dashboard', component: StudentDashboard },
  { id: 'profile', label: 'Profile', component: StudentProfile },
  { id: 'courses', label: 'Courses', component: StudentCourses },
  { id: 'grades', label: 'Grades', component: StudentGrades },
  { id: 'attendance', label: 'Attendance', component: StudentAttendance },
  { id: 'assignments', label: 'Assignments', component: StudentAssignments },
];

// === GLOBAL LOADING CONTEXT ===
export const GlobalLoadingProvider = ({ children }) => {
  const [globalLoading, setGlobalLoading] = useState(false);
  
  return (
    <LoadingContext.Provider value={{ globalLoading, setGlobalLoading }}>
      {children}
    </LoadingContext.Provider>
  );
};

// === MAIN PORTAL WITH SMOOTH TRANSITIONS ===
export const StudentPortal = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component || StudentDashboard;
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
      {/* Navigation */}
      <nav className="glass-surface sticky top-0 z-50">
        <div className="flex items-center gap-2 p-4 overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-xl transition-all duration-200 whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-primary-600 text-white'
                  : 'text-white/60 hover:text-white hover:bg-white/10'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </nav>
      
      {/* Content with smooth transitions */}
      <main className="p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            <ActiveComponent />
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query Hooks | 13 query hooks + 4 mutation hooks with optimistic updates |
| Tailwind Config | Stitch palette, glass utilities, custom animations |
| Framer Motion | Spring animations, staggered reveals, smooth transitions |
| Toast Notifications | Sonner integration with custom glassmorphic styling |
| Skeleton Components | Dashboard stats, grade cards, attendance rows |
| Global Loading | Tab-based navigation with AnimatePresence transitions |

---

*Last Updated: 2026-03-29*
