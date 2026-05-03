import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/teachers';

// =====================
// QUERY KEYS
// =====================
export const teacherKeys = {
  all: ['teacher'],
  profile: () => [...teacherKeys.all, 'profile'],
  profileById: (id) => [...teacherKeys.all, 'profile', id],
  courses: () => [...teacherKeys.all, 'courses'],
  myCourses: () => [...teacherKeys.all, 'courses', 'my'],
  students: () => [...teacherKeys.all, 'students'],
  courseStudents: (courseId) => [...teacherKeys.all, 'students', courseId],
  grades: () => [...teacherKeys.all, 'grades'],
  courseGrades: (courseId) => [...teacherKeys.all, 'grades', courseId],
  attendance: () => [...teacherKeys.all, 'attendance'],
  courseAttendance: (courseId) => [...teacherKeys.all, 'attendance', courseId],
  courseAttendanceStats: (courseId) => [...teacherKeys.all, 'attendance', courseId, 'stats'],
  assignments: () => [...teacherKeys.all, 'assignments'],
  myAssignments: () => [...teacherKeys.all, 'assignments', 'my'],
  assignmentSubmissions: (id) => [...teacherKeys.all, 'assignments', 'submissions', id],
  tests: () => [...teacherKeys.all, 'tests'],
  myTests: () => [...teacherKeys.all, 'tests', 'my'],
  testResults: (testId) => [...teacherKeys.all, 'tests', 'results', testId],
  timetable: () => [...teacherKeys.all, 'timetable'],
  myTimetable: () => [...teacherKeys.all, 'timetable', 'me'],
  videos: () => [...teacherKeys.all, 'videos'],
  myVideos: () => [...teacherKeys.all, 'videos', 'my'],
  notes: () => [...teacherKeys.all, 'notes'],
  myNotes: () => [...teacherKeys.all, 'notes', 'my'],
  dashboard: () => [...teacherKeys.all, 'dashboard'],
};

// =====================
// QUERY HOOKS
// =====================

// Profile
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

// Courses
export const useMyCourses = () => useQuery({
  queryKey: teacherKeys.myCourses(),
  queryFn: api.getMyCourses,
  staleTime: 10 * 60 * 1000,
});

export const useCourseStudents = (courseId) => useQuery({
  queryKey: teacherKeys.courseStudents(courseId),
  queryFn: () => api.getTeacherStudents(courseId),
  enabled: !!courseId,
});

// Grades
export const useCourseGrades = (courseId) => useQuery({
  queryKey: teacherKeys.courseGrades(courseId),
  queryFn: () => api.getCourseGrades(courseId),
  enabled: !!courseId,
});

// Attendance
export const useCourseAttendance = (courseId) => useQuery({
  queryKey: teacherKeys.courseAttendance(courseId),
  queryFn: () => api.getCourseAttendance(courseId),
  enabled: !!courseId,
});

export const useCourseAttendanceStats = (courseId) => useQuery({
  queryKey: teacherKeys.courseAttendanceStats(courseId),
  queryFn: () => api.getCourseAttendanceStats(courseId),
  enabled: !!courseId,
});

// Assignments
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

// Tests
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

// Timetable
export const useMyTimetable = () => useQuery({
  queryKey: teacherKeys.myTimetable(),
  queryFn: api.getMyTimetable,
  staleTime: 10 * 60 * 1000,
});

// Videos
export const useMyVideos = () => useQuery({
  queryKey: teacherKeys.myVideos(),
  queryFn: api.getMyVideos,
  staleTime: 5 * 60 * 1000,
});

// Notes
export const useMyNotes = () => useQuery({
  queryKey: teacherKeys.myNotes(),
  queryFn: api.getMyNotes,
  staleTime: 5 * 60 * 1000,
});

// Dashboard
export const useTeacherDashboard = () => useQuery({
  queryKey: teacherKeys.dashboard(),
  queryFn: api.getTeacherDashboard,
  staleTime: 5 * 60 * 1000,
});

// =====================
// MUTATION HOOKS
// =====================

// Update Teacher Profile
export const useUpdateTeacher = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ teacherId, data }) => api.updateTeacher(teacherId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teacherKeys.profile() });
    },
  });
};

// Bulk Grades
export const useCreateBulkGrades = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (grades) => api.createBulkGrades(grades),
    onMutate: async (grades) => {
      await queryClient.cancelQueries({ queryKey: teacherKeys.grades() });
      const previousGrades = queryClient.getQueryData(teacherKeys.grades());
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

// Bulk Attendance
export const useBulkMarkAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ courseId, records }) => api.bulkMarkAttendance({ course_id: courseId, records }),
    onMutate: async ({ courseId, records }) => {
      await queryClient.cancelQueries({ queryKey: teacherKeys.courseAttendance(courseId) });
      const previous = queryClient.getQueryData(teacherKeys.courseAttendance(courseId));
      queryClient.setQueryData(teacherKeys.courseAttendance(courseId), (old = []) => 
        old.map(record => {
          const updated = records.find(r => r.student_id === record.student_id);
          return updated ? { ...record, ...updated, marked_at: new Date().toISOString() } : record;
        })
      );
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

// Grade Submission
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

// Create/Update/Delete Course
export const useCreateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createAssignment,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.courses() }),
  });
};

export const useUpdateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ courseId, data }) => api.updateCourse(courseId, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.courses() }),
  });
};

export const useDeleteCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteCourse,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.courses() }),
  });
};

// Create/Update/Delete Assignment
export const useCreateAssignment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createAssignment,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.assignments() }),
  });
};

export const useUpdateAssignment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateAssignment(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.assignments() }),
  });
};

export const useDeleteAssignment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteAssignment,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.assignments() }),
  });
};

// Create/Update/Delete Test
export const useCreateTest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createTest,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.tests() }),
  });
};

export const useUpdateTest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateTest(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.tests() }),
  });
};

export const useDeleteTest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteTest,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: teacherKeys.tests() }),
  });
};
