import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/students';

// =====================
// QUERY KEYS
// =====================
export const studentKeys = {
  all: ['student'] || [],
  profile: () => [...studentKeys.all, 'profile'] || [],
  profileById: (id) => [...studentKeys.all, 'profile', id] || [],
  courses: () => [...studentKeys.all, 'courses'] || [],
  enrolledCourses: () => [...studentKeys.all, 'courses', 'enrolled'] || [],
  grades: () => [...studentKeys.all, 'grades'] || [],
  myGrades: () => [...studentKeys.all, 'grades', 'my'] || [],
  attendance: () => [...studentKeys.all, 'attendance'] || [],
  myAttendance: () => [...studentKeys.all, 'attendance', 'my'] || [],
  courseAttendance: (courseId) => [...studentKeys.all, 'attendance', 'course', courseId] || [],
  assignments: () => [...studentKeys.all, 'assignments'] || [],
  assignmentSubmission: (id) => [...studentKeys.all, 'assignments', 'submission', id] || [],
  tests: () => [...studentKeys.all, 'tests'] || [],
  availableTests: () => [...studentKeys.all, 'tests', 'available'] || [],
  testDetails: (id) => [...studentKeys.all, 'tests', 'details', id] || [],
  testResults: () => [...studentKeys.all, 'tests', 'results'] || [],
  testResult: (id) => [...studentKeys.all, 'tests', 'result', id] || [],
  notices: () => [...studentKeys.all, 'notices'] || [],
  dashboard: () => [...studentKeys.all, 'dashboard'] || [],
};

// =====================
// QUERY HOOKS
// =====================

// Profile
export const useStudentProfile = () => {
  return useQuery({
    queryKey: studentKeys.profile(),
    queryFn: async () => {
      const response = await api.getMyStudentProfile();
      return response.data; // Return just the data
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useStudentById = (studentId) => {
  return useQuery({
    queryKey: studentKeys.profileById(studentId),
    queryFn: () => api.getStudentById(studentId),
    enabled: !!studentId,
  });
};

// Courses
export const useEnrolledCourses = () => {
  return useQuery({
    queryKey: studentKeys.enrolledCourses(),
    queryFn: api.getEnrolledCourses,
    staleTime: 10 * 60 * 1000,
  });
};

// Grades
export const useMyGrades = () => {
  return useQuery({
    queryKey: studentKeys.myGrades(),
    queryFn: api.getMyGrades,
    staleTime: 5 * 60 * 1000,
  });
};

// Attendance
export const useMyAttendance = () => {
  return useQuery({
    queryKey: studentKeys.myAttendance(),
    queryFn: api.getMyAttendance,
    staleTime: 5 * 60 * 1000,
  });
};

export const useCourseAttendance = (courseId) => {
  return useQuery({
    queryKey: studentKeys.courseAttendance(courseId),
    queryFn: () => api.getMyCourseAttendance(courseId),
    enabled: !!courseId,
  });
};

// Assignments
export const useStudentAssignments = () => {
  return useQuery({
    queryKey: studentKeys.assignments(),
    queryFn: api.getStudentAssignments,
    staleTime: 5 * 60 * 1000,
  });
};

export const useAssignmentSubmission = (assignmentId) => {
  return useQuery({
    queryKey: studentKeys.assignmentSubmission(assignmentId),
    queryFn: () => api.getMySubmission(assignmentId),
    enabled: !!assignmentId,
  });
};

// Tests
export const useAvailableTests = () => {
  return useQuery({
    queryKey: studentKeys.availableTests(),
    queryFn: api.getAvailableTests,
    staleTime: 5 * 60 * 1000,
  });
};

export const useTestDetails = (testId) => {
  return useQuery({
    queryKey: studentKeys.testDetails(testId),
    queryFn: () => api.getTestDetails(testId),
    enabled: !!testId,
  });
};

export const useMyTestResults = () => {
  return useQuery({
    queryKey: studentKeys.testResults(),
    queryFn: api.getMyTestResults,
    staleTime: 10 * 60 * 1000,
  });
};

export const useTestResult = (testId) => {
  return useQuery({
    queryKey: studentKeys.testResult(testId),
    queryFn: () => api.getTestResult(testId),
    enabled: !!testId,
  });
};

// Notices
export const useStudentNotices = () => {
  return useQuery({
    queryKey: studentKeys.notices(),
    queryFn: api.getStudentNotices,
    staleTime: 5 * 60 * 1000,
  });
};

// Dashboard
export const useStudentDashboard = () => {
  return useQuery({
    queryKey: studentKeys.dashboard(),
    queryFn: api.getStudentDashboard,
    staleTime: 5 * 60 * 1000,
  });
};

// =====================
// MUTATION HOOKS
// =====================

// Update Student Profile
export const useUpdateStudent = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ studentId, data }) => api.updateStudent(studentId, data),
    onMutate: async ({ studentId, data }) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.profileById(studentId) });
      
      const previousProfile = queryClient.getQueryData(studentKeys.profileById(studentId));
      
      queryClient.setQueryData(studentKeys.profileById(studentId), {
        ...previousProfile,
        data,
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

// Submit Assignment (Optimistic Update)
export const useSubmitAssignment = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ assignmentId, data }) => api.submitAssignment(assignmentId, data),
    onMutate: async ({ assignmentId }) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.assignments() });
      
      const previousAssignments = queryClient.getQueryData(studentKeys.assignments());
      
      // Optimistically mark as "Submitted"
      queryClient.setQueryData(studentKeys.assignments(), (old) => {
        if (!old) return old;
        return {
          ...old,
          data: old.data?.map((assignment) => 
            assignment.id === assignmentId 
              ? { ...assignment, status: 'submitted', submittedAt: new Date().toISOString() }
              : assignment
          ),
        };
      });
      
      return { previousAssignments };
    },
    onError: (err, { assignmentId }, context) => {
      queryClient.setQueryData(studentKeys.assignments(), context?.previousAssignments);
    },
    onSettled: (data, error, { assignmentId }) => {
      queryClient.invalidateQueries({ queryKey: studentKeys.assignments() });
      queryClient.invalidateQueries({ 
        queryKey: studentKeys.assignmentSubmission(assignmentId) 
      });
    },
  });
};

// Start Test
export const useStartTest = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (testId) => api.startTest(testId),
    onMutate: async (testId) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.availableTests() });
      
      const previousTests = queryClient.getQueryData(studentKeys.availableTests());
      
      queryClient.setQueryData(studentKeys.availableTests(), (old) => {
        if (!old) return old;
        return {
          ...old,
          data: old.data?.map((test) =>
            test.id === testId
              ? { ...test, status: 'in_progress', startedAt: new Date().toISOString() }
              : test
          ),
        };
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

// Submit Test
export const useSubmitTest = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ testId, answers }) => api.submitTest(testId, answers),
    onMutate: async ({ testId }) => {
      await queryClient.cancelQueries({ queryKey: studentKeys.testResults() });
      
      const previousResults = queryClient.getQueryData(studentKeys.testResults());
      
      // Add pending result
      queryClient.setQueryData(studentKeys.testResults(), (old) => {
        if (!old) return { data: [{ testId, status: 'pending', submittedAt: new Date().toISOString() }] };
        return {
          ...old,
          data: [...(old.data || []), { testId, status: 'pending', submittedAt: new Date().toISOString() }],
        };
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
