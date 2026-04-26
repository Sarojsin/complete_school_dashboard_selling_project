# Implementation Plan - Frontend Missing Services Plan 2: Teacher Module API Integration

This plan details the comprehensive API integration for the Teacher Portal, focusing on connecting all missing backend endpoints to the frontend with premium glassmorphic design while ensuring 100% accurate data flow.

---

## Part 1: Design System Configuration

### 1.1 Tailwind Configuration (Stitch Palette for Teacher)

```javascript
// tailwind.config.js - Teacher Module Extension
module.exports = {
  theme: {
    extend: {
      colors: {
        teacher: {
          primary: '#6366f1',     // Indigo
          success: '#10b981',     // Emerald
          warning: '#f59e0b',     // Amber
          danger: '#ef4444',      // Red
          surface: 'rgba(15, 23, 42, 0.8)',
        }
      },
      animation: {
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-glow': 'pulseGlow 2s infinite',
        'grade-bar': 'gradeBar 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      keyframes: {
        slideInRight: {
          '0%': { transform: 'translateX(20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(99, 102, 241, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(99, 102, 241, 0.6)' },
        }
      }
    }
  }
}
```

### 1.2 Teacher-Specific Glass Components

```css
/* Teacher Module Glass Components */
.teacher-glass-card {
  @apply bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl 
         border border-white/10 shadow-2xl rounded-2xl;
}

.teacher-stat-card {
  @apply teacher-glass-card p-6 relative overflow-hidden;
}

.teacher-stat-card::before {
  content: '';
  @apply absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-500/20 to-transparent 
         rounded-full blur-3xl -translate-y-1/2 translate-x-1/2;
}

.grade-input-glass {
  @apply bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white 
         focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 
         transition-all duration-200 backdrop-blur-sm;
}

.attendance-toggle {
  @apply relative w-14 h-8 rounded-full cursor-pointer transition-all duration-300;
}

.attendance-toggle-active {
  @apply bg-gradient-to-r from-emerald-500 to-emerald-600;
}

.attendance-toggle-inactive {
  @apply bg-white/10;
}
```

---

## Part 2: Service Orchestration Layer (TanStack Query)

### 2.1 Query Keys & Hooks Factory

```javascript
// frontend/src/modules/school/school_teacher/hooks/useTeacher.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/teachers';

// === QUERY KEYS ===
export const teacherKeys = {
  all: ['teacher'] as const,
  profile: () => [...teacherKeys.all, 'profile'] as const,
  profileById: (id: string) => [...teacherKeys.all, 'profile', id] as const,
  courses: () => [...teacherKeys.all, 'courses'] as const,
  myCourses: () => [...teacherKeys.all, 'courses', 'my'] as const,
  students: () => [...teacherKeys.all, 'students'] as const,
  courseStudents: (courseId: string) => [...teacherKeys.all, 'students', courseId] as const,
  grades: () => [...teacherKeys.all, 'grades'] as const,
  courseGrades: (courseId: string) => [...teacherKeys.all, 'grades', courseId] as const,
  attendance: () => [...teacherKeys.all, 'attendance'] as const,
  courseAttendance: (courseId: string) => [...teacherKeys.all, 'attendance', courseId] as const,
  assignments: () => [...teacherKeys.all, 'assignments'] as const,
  myAssignments: () => [...teacherKeys.all, 'assignments', 'my'] as const,
  assignmentSubmissions: (id: string) => [...teacherKeys.all, 'assignments', 'submissions', id] as const,
  tests: () => [...teacherKeys.all, 'tests'] as const,
  myTests: () => [...teacherKeys.all, 'tests', 'my'] as const,
  testResults: (testId: string) => [...teacherKeys.all, 'tests', 'results', testId] as const,
  timetable: () => [...teacherKeys.all, 'timetable'] as const,
  myTimetable: () => [...teacherKeys.all, 'timetable', 'me'] as const,
  videos: () => [...teacherKeys.all, 'videos'] as const,
  myVideos: () => [...teacherKeys.all, 'videos', 'my'] as const,
  notes: () => [...teacherKeys.all, 'notes'] as const,
  myNotes: () => [...teacherKeys.all, 'notes', 'my'] as const,
  dashboard: () => [...teacherKeys.all, 'dashboard'] as const,
};

// === QUERY HOOKS ===
export const useTeacherProfile = () => useQuery({
  queryKey: teacherKeys.profile(),
  queryFn: api.getTeacherProfile,
  staleTime: 5 * 60 * 1000,
});

export const useTeacherById = (teacherId) => useQuery({
  queryKey: teacherKeys.profileById(teacherId),
  queryFn: () => api.getTeacherById(teacherId),
  enabled: !!teacherId,
});

export const useMyCourses = () => useQuery({
  queryKey: teacherKeys.myCourses(),
  queryFn: api.getMyCourses,
  staleTime: 10 * 60 * 1000,
});

export const useCourseStudents = (courseId) => useQuery({
  queryKey: teacherKeys.courseStudents(courseId),
  queryFn: () => api.getCourseStudents(courseId),
  enabled: !!courseId,
});

export const useCourseGrades = (courseId) => useQuery({
  queryKey: teacherKeys.courseGrades(courseId),
  queryFn: () => api.getCourseGrades(courseId),
  enabled: !!courseId,
});

export const useCourseAttendance = (courseId) => useQuery({
  queryKey: teacherKeys.courseAttendance(courseId),
  queryFn: () => api.getCourseAttendance(courseId),
  enabled: !!courseId,
});

export const useCourseAttendanceStats = (courseId) => useQuery({
  queryKey: [...teacherKeys.courseAttendance(courseId), 'stats'],
  queryFn: () => api.getCourseAttendanceStats(courseId),
  enabled: !!courseId,
});

export const useMyAssignments = () => useQuery({
  queryKey: teacherKeys.myAssignments(),
  queryFn: api.getMyAssignments,
  staleTime: 5 * 60 * 1000,
});

export const useAssignmentSubmissions = (assignmentId) => useQuery({
  queryKey: teacherKeys.assignmentSubmissions(assignmentId),
  queryFn: () => api.getAssignmentSubmissions(assignmentId),
  enabled: !!assignmentId,
});

export const useMyTests = () => useQuery({
  queryKey: teacherKeys.myTests(),
  queryFn: api.getMyTests,
  staleTime: 5 * 60 * 1000,
});

export const useTestResults = (testId) => useQuery({
  queryKey: teacherKeys.testResults(testId),
  queryFn: () => api.getTestResults(testId),
  enabled: !!testId,
});

export const useMyTimetable = () => useQuery({
  queryKey: teacherKeys.myTimetable(),
  queryFn: api.getMyTimetable,
  staleTime: 10 * 60 * 1000,
});

export const useMyVideos = () => useQuery({
  queryKey: teacherKeys.myVideos(),
  queryFn: api.getMyVideos,
  staleTime: 5 * 60 * 1000,
});

export const useMyNotes = () => useQuery({
  queryKey: teacherKeys.myNotes(),
  queryFn: api.getMyNotes,
  staleTime: 5 * 60 * 1000,
});

export const useTeacherDashboard = () => useQuery({
  queryKey: teacherKeys.dashboard(),
  queryFn: api.teacherDashboard,
  staleTime: 5 * 60 * 1000,
});
```

### 2.2 Mutation Hooks with Optimistic Updates

```javascript
// === MUTATION HOOKS ===
export const useUpdateTeacher = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ teacherId, data }) => api.updateTeacher(teacherId, data),
    onMutate: async ({ teacherId, data }) => {
      await queryClient.cancelQueries({ queryKey: teacherKeys.profileById(teacherId) });
      const previous = queryClient.getQueryData(teacherKeys.profileById(teacherId));
      queryClient.setQueryData(teacherKeys.profileById(teacherId), { ...previous, ...data });
      return { previous };
    },
    onError: (err, { teacherId }, context) => {
      queryClient.setQueryData(teacherKeys.profileById(teacherId), context?.previous);
    },
    onSettled: (data, error, { teacherId }) => {
      queryClient.invalidateQueries({ queryKey: teacherKeys.profile() });
    },
  });
};

// === BULK GRADE OPTIMISTIC UPDATE ===
export const useCreateBulkGrades = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (grades) => api.createBulkGrades(grades),
    onMutate: async (grades) => {
      await queryClient.cancelQueries({ queryKey: teacherKeys.grades() });
      const previousGrades = queryClient.getQueryData(teacherKeys.grades());
      
      // Optimistically add new grades
      const optimisticGrades = grades.map(g => ({ ...g, status: 'pending' }));
      queryClient.setQueryData(teacherKeys.grades(), (old = []) => [...old, ...optimisticGrades]);
      
      return { previousGrades };
    },
    onError: (err, vars, context) => {
      queryClient.setQueryData(teacherKeys.grades(), context?.previousGrades);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: teacherKeys.grades() });
    },
  });
};

// === BULK ATTENDANCE OPTIMISTIC UPDATE ===
export const useBulkMarkAttendance = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ courseId, data }) => api.bulkMarkAttendance({ course_id: courseId, ...data }),
    onMutate: async ({ courseId, records }) => {
      await queryClient.cancelQueries({ queryKey: teacherKeys.courseAttendance(courseId) });
      const previous = queryClient.getQueryData(teacherKeys.courseAttendance(courseId));
      
      queryClient.setQueryData(teacherKeys.courseAttendance(courseId), (old = []) => {
        return old.map(record => {
          const updated = records.find(r => r.student_id === record.student_id);
          return updated ? { ...record, status: updated.status, marked_at: new Date().toISOString() } : record;
        });
      });
      
      return { previous };
    },
    onError: (err, { courseId }, context) => {
      queryClient.setQueryData(teacherKeys.courseAttendance(courseId), context?.previous);
    },
    onSettled: (data, error, { courseId }) => {
      queryClient.invalidateQueries({ queryKey: teacherKeys.courseAttendance(courseId) });
    },
  });
};

// === GRADE SUBMISSION ===
export const useGradeSubmission = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ submissionId, data }) => api.gradeSubmission(submissionId, data),
    onMutate: async ({ submissionId, data }) => {
      await queryClient.cancelQueries({ queryKey: teacherKeys.assignments() });
      const previous = queryClient.getQueryData(teacherKeys.assignments());
      
      queryClient.setQueryData(teacherKeys.assignments(), (old = []) => 
        old.map(sub => sub.id === submissionId ? { ...sub, ...data, graded: true } : sub)
      );
      
      return { previous };
    },
    onError: (err, { submissionId }, context) => {
      queryClient.setQueryData(teacherKeys.assignments(), context?.previous);
    },
    onSettled: (data, error, { submissionId }) => {
      queryClient.invalidateQueries({ queryKey: teacherKeys.assignments() });
    },
  });
};
```

---

## Part 3: The "Stitch" Feedback Loop

### 3.1 Teacher Skeleton Components

```javascript
// frontend/src/components/ui/TeacherSkeleton.jsx
import { motion } from 'framer-motion';

export const TeacherDashboardSkeleton = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[...Array(4)].map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="teacher-glass-card p-6"
        >
          <div className="shimmer-skeleton h-4 w-24 mb-4" />
          <div className="shimmer-skeleton h-8 w-16" />
        </motion.div>
      ))}
    </div>
  </div>
);

export const GradeTableSkeleton = () => (
  <div className="teacher-glass-card p-6">
    {[...Array(5)].map((_, i) => (
      <div key={i} className="flex items-center gap-4 mb-4">
        <div className="shimmer-skeleton h-10 w-10 rounded-full" />
        <div className="shimmer-skeleton h-5 flex-1" />
        <div className="shimmer-skeleton h-5 w-20" />
      </div>
    ))}
  </div>
);

export const AttendanceGridSkeleton = () => (
  <div className="teacher-glass-card p-6">
    <div className="grid grid-cols-8 gap-2">
      {[...Array(24)].map((_, i) => (
        <div key={i} className="shimmer-skeleton h-12 rounded-lg" />
      ))}
    </div>
  </div>
);
```

### 3.2 Teacher Toast Notifications

```javascript
// frontend/src/lib/teacherToast.js
import { toast } from 'sonner';

export const gradeToast = {
  loading: 'Submitting grades...',
  success: (count) => `Successfully graded ${count} student(s)!`,
  error: 'Failed to submit grades. Please try again.',
};

export const attendanceToast = {
  loading: 'Marking attendance...',
  success: (present, total) => `Attendance marked: ${present}/${total} present`,
  error: 'Failed to mark attendance. Please try again.',
};

export const assignmentToast = {
  loading: 'Publishing assignment...',
  success: 'Assignment published successfully!',
  error: 'Failed to publish assignment.',
};

export const courseToast = {
  create: { loading: 'Creating course...', success: 'Course created!', error: 'Failed to create course.' },
  update: { loading: 'Updating course...', success: 'Course updated!', error: 'Failed to update course.' },
  delete: { loading: 'Deleting course...', success: 'Course deleted!', error: 'Failed to delete course.' },
};

export const testToast = {
  create: { loading: 'Creating test...', success: 'Test created!', error: 'Failed to create test.' },
  publish: { loading: 'Publishing results...', success: 'Results published!', error: 'Failed to publish results.' },
};
```

---

## Part 4: High-Fidelity Teacher Components

### 4.1 Teacher Command Center Dashboard

```javascript
// frontend/src/modules/school/school_teacher/components/TeacherDashboard.jsx
import { motion } from 'framer-motion';
import { useTeacherDashboard, useMyCourses, useMyTests, useMyAssignments } from '../hooks/useTeacher';

// === ANIMATED GRADE BAR ===
const AnimatedGradeBar = ({ students }) => {
  return (
    <div className="space-y-3">
      {students.slice(0, 8).map((student, index) => (
        <motion.div
          key={student.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.05 }}
          className="flex items-center gap-3"
        >
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
            {student.name.charAt(0)}
          </div>
          <div className="flex-1">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-white">{student.name}</span>
              <span className="text-white/60">{student.grade}%</span>
            </div>
            <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${student.grade}%` }}
                transition={{ duration: 0.6, delay: index * 0.1, ease: 'easeOut' }}
                className={`h-full rounded-full ${
                  student.grade >= 90 ? 'bg-emerald-500' :
                  student.grade >= 70 ? 'bg-primary-500' : 'bg-amber-500'
                }`}
              />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

// === QUICK ACTION BUTTON ===
const QuickActionButton = ({ icon: Icon, label, color, onClick, delay = 0 }) => {
  const colorClasses = {
    primary: 'from-primary-600 to-primary-700 hover:from-primary-500 hover:to-primary-600',
    success: 'from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600',
    warning: 'from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600',
    purple: 'from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600',
  };
  
  return (
    <motion.button
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay }}
      onClick={onClick}
      className={`p-4 rounded-2xl bg-gradient-to-br ${colorClasses[color]} 
                 text-white shadow-lg hover:shadow-xl transition-all duration-200 
                 hover:scale-105 active:scale-95 flex flex-col items-center gap-2`}
    >
      <Icon className="w-6 h-6" />
      <span className="text-sm font-medium">{label}</span>
    </motion.button>
  );
};

// === ATTENDANCE QUICK GRID ===
const AttendanceQuickGrid = ({ students, onMark }) => {
  return (
    <div className="grid grid-cols-4 gap-2">
      {students.map((student, index) => (
        <motion.button
          key={student.id}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.02 }}
          onClick={() => onMark(student.id)}
          className={`p-3 rounded-xl text-center transition-all duration-200 ${
            student.status === 'present' 
              ? 'bg-emerald-500/30 border-2 border-emerald-500/50' 
              : student.status === 'absent'
              ? 'bg-red-500/30 border-2 border-red-500/50'
              : 'bg-white/5 border-2 border-white/10 hover:border-white/30'
          }`}
        >
          <p className="text-white text-xs font-medium truncate">{student.name}</p>
          <p className={`text-lg font-bold ${
            student.status === 'present' ? 'text-emerald-400' :
            student.status === 'absent' ? 'text-red-400' : 'text-white/40'
          }`}>
            {student.status === 'present' ? 'P' : student.status === 'absent' ? 'A' : '-'}
          </p>
        </motion.button>
      ))}
    </div>
  );
};

// === MAIN TEACHER DASHBOARD ===
export const TeacherDashboard = () => {
  const { data: dashboard, isLoading } = useTeacherDashboard();
  const { data: courses } = useMyCourses();
  const { data: tests } = useMyTests();
  const { data: assignments } = useMyAssignments();
  
  if (isLoading) return <TeacherDashboardSkeleton />;
  
  const quickActions = [
    { icon: ClipboardCheck, label: 'Take Attendance', color: 'primary', action: 'attendance' },
    { icon: Grade, label: 'Submit Grades', color: 'success', action: 'grades' },
    { icon: FileText, label: 'Create Assignment', color: 'warning', action: 'assignment' },
    { icon: Clock, label: 'Create Test', color: 'purple', action: 'test' },
  ];
  
  return (
    <div className="space-y-8 p-6">
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="teacher-glass-card p-8 bg-gradient-to-r from-primary-900/50 to-purple-900/50"
      >
        <h1 className="text-3xl font-bold text-white mb-2">
          Welcome back, {dashboard?.teacherName || 'Teacher'}!
        </h1>
        <p className="text-white/60">You have {dashboard?.pendingGrading || 0} assignments to grade</p>
      </motion.div>
      
      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <QuickActionButton key={action.label} {...action} delay={index * 0.1} />
          ))}
        </div>
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Students', value: dashboard?.totalStudents || 0, color: 'primary' },
          { label: 'Active Courses', value: courses?.length || 0, color: 'purple' },
          { label: 'Pending Tests', value: tests?.filter(t => !t.published)?.length || 0, color: 'warning' },
          { label: 'Assignments', value: assignments?.length || 0, color: 'success' },
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            className="teacher-stat-card"
          >
            <p className="text-white/60 text-sm">{stat.label}</p>
            <p className="text-3xl font-bold text-white mt-1">{stat.value}</p>
          </motion.div>
        ))}
      </div>
      
      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Grade Overview */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="teacher-glass-card p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-4">Grade Overview</h2>
          <AnimatedGradeBar students={dashboard?.recentGrades || []} />
        </motion.div>
        
        {/* Today's Schedule */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="teacher-glass-card p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-4">Today's Classes</h2>
          <div className="space-y-3">
            {dashboard?.todaySchedule?.map((slot, index) => (
              <motion.div
                key={slot.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="flex items-center gap-4 p-3 rounded-xl bg-white/5"
              >
                <div className="text-white/60 text-sm font-mono">{slot.time}</div>
                <div className="flex-1">
                  <p className="text-white font-medium">{slot.course}</p>
                  <p className="text-white/40 text-xs">{slot.room}</p>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs ${
                  slot.status === 'upcoming' ? 'bg-primary-500/20 text-primary-400' :
                  slot.status === 'ongoing' ? 'bg-emerald-500/20 text-emerald-400' :
                  'bg-white/10 text-white/40'
                }`}>
                  {slot.status}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};
```

---

## Part 5: Execution Strategy

### 5.1 Global Loading & Tab Navigation

```javascript
// Teacher Module Page Navigation with smooth transitions
const teacherTabs = [
  { id: 'dashboard', label: 'Dashboard', icon: Home },
  { id: 'courses', label: 'Courses', icon: BookOpen },
  { id: 'students', label: 'Students', icon: Users },
  { id: 'grades', label: 'Grades', icon: Award },
  { id: 'attendance', label: 'Attendance', icon: Calendar },
  { id: 'assignments', label: 'Assignments', icon: FileText },
  { id: 'tests', label: 'Tests', icon: Clock },
  { id: 'timetable', label: 'Timetable', icon: Calendar },
  { id: 'resources', label: 'Resources', icon: Folder },
];

export const TeacherPortal = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
      {/* Sidebar Navigation */}
      <aside className="fixed left-0 top-0 h-full w-64 glass-surface z-50">
        <div className="p-4">
          <h2 className="text-xl font-bold text-white mb-6">Teacher Portal</h2>
          <nav className="space-y-2">
            {teacherTabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white'
                    : 'text-white/60 hover:text-white hover:bg-white/10'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="ml-64 p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {/* Render active component */}
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
| TanStack Query Hooks | 14 query hooks + 4 mutation hooks with optimistic updates |
| Tailwind Config | Teacher-specific colors, animations, glass utilities |
| Framer Motion | Staggered reveals, grade bars, schedule animations |
| Toast Notifications | Grade, attendance, assignment, course, test toasts |
| Skeleton Components | Dashboard, grade table, attendance grid |
| Navigation | Sidebar with smooth tab transitions |

---

*Last Updated: 2026-03-29*
