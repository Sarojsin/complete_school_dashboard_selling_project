// =====================
// USE AUTHORITY - TanStack Query Hooks
// Authority Module - Plan 3 Implementation
// =====================

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/authority';
import { authorityToast } from '../lib/toast';

// Query Keys
export const authorityKeys = {
  all: ['authority'] as const,
  dashboard: () => [...authorityKeys.all, 'dashboard'] as const,
  profile: () => [...authorityKeys.all, 'profile'] as const,
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
  groups: () => [...authorityKeys.all, 'groups'] as const,
  analytics: (type) => [...authorityKeys.all, 'analytics', type] as const,
  reports: () => [...authorityKeys.all, 'reports'] as const,
  library: () => [...authorityKeys.all, 'library'] as const,
  attendance: () => [...authorityKeys.all, 'attendance'] as const,
};

// =====================
// QUERY HOOKS
// =====================

// Dashboard & Profile
export const useAuthorityDashboard = () => useQuery({
  queryKey: authorityKeys.dashboard(),
  queryFn: api.getAuthorityDashboard,
  staleTime: 5 * 60 * 1000,
});

export const useAuthorityProfile = () => useQuery({
  queryKey: authorityKeys.profile(),
  queryFn: api.getMyAuthorityProfile,
  staleTime: 5 * 60 * 1000,
});

// Students
export const useAllStudents = (params = {}) => useQuery({
  queryKey: [...authorityKeys.students(), params],
  queryFn: () => api.getAdminStudents(params),
  staleTime: 5 * 60 * 1000,
});

export const useStudentById = (id) => useQuery({
  queryKey: authorityKeys.studentById(id),
  queryFn: () => api.getStudentById(id),
  enabled: !!id,
  staleTime: 5 * 60 * 1000,
});

// Teachers
export const useAllTeachers = (params = {}) => useQuery({
  queryKey: [...authorityKeys.teachers(), params],
  queryFn: () => api.getAdminTeachers(params),
  staleTime: 5 * 60 * 1000,
});

export const useTeacherById = (id) => useQuery({
  queryKey: authorityKeys.teacherById(id),
  queryFn: () => api.getTeacherById(id),
  enabled: !!id,
  staleTime: 5 * 60 * 1000,
});

// Courses
export const useAllCourses = (params = {}) => useQuery({
  queryKey: [...authorityKeys.courses(), params],
  queryFn: () => api.getAdminCourses(params),
  staleTime: 10 * 60 * 1000,
});

export const useCourseById = (id) => useQuery({
  queryKey: authorityKeys.courseById(id),
  queryFn: () => api.getCourseById(id),
  enabled: !!id,
  staleTime: 10 * 60 * 1000,
});

// Departments
export const useAllDepartments = () => useQuery({
  queryKey: authorityKeys.departments(),
  queryFn: api.getAllDepartments,
  staleTime: 10 * 60 * 1000,
});

// Fees
export const useAllFees = (params = {}) => useQuery({
  queryKey: [...authorityKeys.fees(), params],
  queryFn: () => api.getAdminFees(params),
  staleTime: 5 * 60 * 1000,
});

export const useFeeById = (id) => useQuery({
  queryKey: authorityKeys.feeById(id),
  queryFn: () => api.getFeeById(id),
  enabled: !!id,
  staleTime: 5 * 60 * 1000,
});

export const useFeeStructure = () => useQuery({
  queryKey: authorityKeys.feeStructure(),
  queryFn: api.getFeeStructure,
  staleTime: 10 * 60 * 1000,
});

export const usePendingPayments = (params = {}) => useQuery({
  queryKey: [...authorityKeys.fees(), 'pending', params],
  queryFn: () => api.getPendingPayments(params),
  staleTime: 5 * 60 * 1000,
});

// Notices
export const useAllNotices = (params = {}) => useQuery({
  queryKey: [...authorityKeys.notices(), params],
  queryFn: () => api.getAdminNotices(params),
  staleTime: 5 * 60 * 1000,
});

export const useNoticeById = (id) => useQuery({
  queryKey: authorityKeys.noticeById(id),
  queryFn: () => api.getNoticeById(id),
  enabled: !!id,
  staleTime: 5 * 60 * 1000,
});

// Groups
export const useAllGroups = (params = {}) => useQuery({
  queryKey: [...authorityKeys.groups(), params],
  queryFn: () => api.getAllGroups(params),
  staleTime: 10 * 60 * 1000,
});

// Analytics
export const useStudentAnalytics = () => useQuery({
  queryKey: authorityKeys.analytics('students'),
  queryFn: api.getStudentAnalytics,
  staleTime: 10 * 60 * 1000,
});

export const useAttendanceAnalytics = () => useQuery({
  queryKey: authorityKeys.analytics('attendance'),
  queryFn: api.getAttendanceAnalytics,
  staleTime: 10 * 60 * 1000,
});

export const usePerformanceAnalytics = () => useQuery({
  queryKey: authorityKeys.analytics('performance'),
  queryFn: api.getPerformanceAnalytics,
  staleTime: 10 * 60 * 1000,
});

export const useEnrollmentStats = (params = {}) => useQuery({
  queryKey: [...authorityKeys.analytics('enrollment'), params],
  queryFn: () => api.getEnrollmentStats(params),
  staleTime: 10 * 60 * 1000,
});

export const useRevenueStats = (params = {}) => useQuery({
  queryKey: [...authorityKeys.analytics('revenue'), params],
  queryFn: () => api.getRevenueStats(params),
  staleTime: 10 * 60 * 1000,
});

export const useCourseAnalytics = () => useQuery({
  queryKey: authorityKeys.analytics('courses'),
  queryFn: api.getCourseAnalytics,
  staleTime: 10 * 60 * 1000,
});

// Reports
export const useAdminReports = (reportType = 'summary') => useQuery({
  queryKey: [...authorityKeys.reports(), reportType],
  queryFn: () => api.getAdminReports(reportType),
  staleTime: 10 * 60 * 1000,
});

// Library
export const useLibraryStats = () => useQuery({
  queryKey: authorityKeys.library(),
  queryFn: api.getLibraryStats,
  staleTime: 10 * 60 * 1000,
});

export const useOverdueBooks = () => useQuery({
  queryKey: [...authorityKeys.library(), 'overdue'],
  queryFn: api.getOverdueBooks,
  staleTime: 5 * 60 * 1000,
});

// Attendance
export const useAttendanceOverview = (params = {}) => useQuery({
  queryKey: [...authorityKeys.attendance(), 'overview', params],
  queryFn: () => api.getAttendanceOverview(params),
  staleTime: 10 * 60 * 1000,
});

export const useAttendanceReport = (params = {}) => useQuery({
  queryKey: [...authorityKeys.attendance(), 'report', params],
  queryFn: () => api.getAttendanceReport(params),
  staleTime: 10 * 60 * 1000,
});

// =====================
// MUTATION HOOKS
// =====================

// Profile
export const useUpdateAuthorityProfile = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateAuthorityProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.profile() });
      authorityToast.profile.update();
    },
    onError: () => authorityToast.profile.error(),
  });
};

// Students
export const useCreateStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createAdminStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      authorityToast.student.create();
    },
    onError: () => authorityToast.student.error(),
  });
};

export const useUpdateStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateStudent(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      queryClient.invalidateQueries({ queryKey: authorityKeys.studentById(id) });
      authorityToast.student.update();
    },
    onError: () => authorityToast.student.error(),
  });
};

export const useDeleteStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      authorityToast.student.delete();
    },
    onError: () => authorityToast.student.error(),
  });
};

export const useBulkCreateStudents = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkCreateStudents,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      authorityToast.student.bulk();
    },
    onError: () => authorityToast.student.error(),
  });
};

export const useImportStudents = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.importStudentsFromFile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.students() });
      authorityToast.student.bulk();
    },
    onError: () => authorityToast.student.error(),
  });
};

// Teachers
export const useCreateTeacher = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createAdminTeacher,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.teachers() });
      authorityToast.teacher.create();
    },
    onError: () => authorityToast.teacher.error(),
  });
};

export const useUpdateTeacher = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateTeacher(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.teachers() });
      queryClient.invalidateQueries({ queryKey: authorityKeys.teacherById(id) });
      authorityToast.teacher.update();
    },
    onError: () => authorityToast.teacher.error(),
  });
};

export const useDeleteTeacher = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteTeacher,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.teachers() });
      authorityToast.teacher.delete();
    },
    onError: () => authorityToast.teacher.error(),
  });
};

export const useBulkCreateTeachers = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkCreateTeachers,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.teachers() });
      authorityToast.teacher.create();
    },
    onError: () => authorityToast.teacher.error(),
  });
};

// Courses
export const useCreateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createCourse,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.courses() });
      authorityToast.course.create();
    },
    onError: () => authorityToast.course.error(),
  });
};

export const useUpdateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateCourse(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.courses() });
      queryClient.invalidateQueries({ queryKey: authorityKeys.courseById(id) });
      authorityToast.course.update();
    },
    onError: () => authorityToast.course.error(),
  });
};

export const useDeleteCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteCourse,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.courses() });
      authorityToast.course.delete();
    },
    onError: () => authorityToast.course.error(),
  });
};

export const useAssignTeacherToCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ courseId, teacherId }) => api.assignTeacherToCourse(courseId, teacherId),
    onSuccess: (_, { courseId }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.courseById(courseId) });
      authorityToast.course.assign();
    },
    onError: () => authorityToast.course.error(),
  });
};

// Departments
export const useCreateDepartment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createDepartment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.departments() });
      authorityToast.department.create();
    },
    onError: () => authorityToast.department.error(),
  });
};

export const useUpdateDepartment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateDepartment(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.departments() });
      authorityToast.department.update();
    },
    onError: () => authorityToast.department.error(),
  });
};

export const useDeleteDepartment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteDepartment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.departments() });
      authorityToast.department.delete();
    },
    onError: () => authorityToast.department.error(),
  });
};

// Fees
export const useCreateFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createFee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
      authorityToast.fee.create();
    },
    onError: () => authorityToast.fee.error(),
  });
};

export const useUpdateFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateFee(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
      queryClient.invalidateQueries({ queryKey: authorityKeys.feeById(id) });
      authorityToast.fee.update();
    },
    onError: () => authorityToast.fee.error(),
  });
};

export const useDeleteFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteFee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
      authorityToast.fee.delete();
    },
    onError: () => authorityToast.fee.error(),
  });
};

export const useCreateFeeStructure = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createFeeStructure,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.feeStructure() });
      authorityToast.fee.create();
    },
    onError: () => authorityToast.fee.error(),
  });
};

export const useUpdateFeeStructure = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateFeeStructure(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.feeStructure() });
      authorityToast.fee.update();
    },
    onError: () => authorityToast.fee.error(),
  });
};

export const useBulkAssignFees = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkAssignFees,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
      authorityToast.fee.bulkAssign();
    },
    onError: () => authorityToast.fee.error(),
  });
};

export const useRecordPayment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ feeId, data }) => api.recordPayment(feeId, data),
    onSuccess: (_, { feeId }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
      queryClient.invalidateQueries({ queryKey: authorityKeys.feeById(feeId) });
      queryClient.invalidateQueries({ queryKey: authorityKeys.fees() });
      authorityToast.fee.payment();
    },
    onError: () => authorityToast.fee.error(),
  });
};

// Notices
export const useCreateNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createNotice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.notices() });
      authorityToast.notice.create();
    },
    onError: () => authorityToast.notice.error(),
  });
};

export const useUpdateNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateNotice(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.notices() });
      queryClient.invalidateQueries({ queryKey: authorityKeys.noticeById(id) });
      authorityToast.notice.update();
    },
    onError: () => authorityToast.notice.error(),
  });
};

export const useDeleteNotice = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteNotice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.notices() });
      authorityToast.notice.delete();
    },
    onError: () => authorityToast.notice.error(),
  });
};

export const useToggleNoticeStatus = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.toggleNoticeStatus,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.notices() });
      authorityToast.notice.toggle();
    },
    onError: () => authorityToast.notice.error(),
  });
};

// Groups
export const useCreateGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.groups() });
      authorityToast.group.create();
    },
    onError: () => authorityToast.group.error(),
  });
};

export const useUpdateGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateGroup(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.groups() });
      authorityToast.group.update();
    },
    onError: () => authorityToast.group.error(),
  });
};

export const useDeleteGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.groups() });
      authorityToast.group.delete();
    },
    onError: () => authorityToast.group.error(),
  });
};

export const useManageGroupMembers = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, data }) => api.manageGroupMembers(groupId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: authorityKeys.groups() });
      authorityToast.group.members();
    },
    onError: () => authorityToast.group.error(),
  });
};

// Reports
export const useGenerateReport = () => {
  return useMutation({
    mutationFn: api.generateReport,
    onSuccess: () => authorityToast.report.generate(),
    onError: () => authorityToast.report.error(),
  });
};

export default {
  authorityKeys,
  useAuthorityDashboard,
  useAuthorityProfile,
  useAllStudents,
  useStudentById,
  useAllTeachers,
  useTeacherById,
  useAllCourses,
  useCourseById,
  useAllDepartments,
  useAllFees,
  useFeeById,
  useFeeStructure,
  useAllNotices,
  useNoticeById,
  useAllGroups,
  useStudentAnalytics,
  useAttendanceAnalytics,
  usePerformanceAnalytics,
  useEnrollmentStats,
  useRevenueStats,
  useCourseAnalytics,
  useAdminReports,
  useLibraryStats,
  useOverdueBooks,
  useAttendanceOverview,
  useAttendanceReport,
};
