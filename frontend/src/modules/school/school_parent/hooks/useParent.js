// =====================
// USE PARENT - TanStack Query Hooks
// Parent Module - Plan 4 Implementation
// =====================

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/parents';
import { parentToast } from '../lib/toast';

// Query Keys
export const parentKeys = {
  all: ['parent'] as const,
  dashboard: () => [...parentKeys.all, 'dashboard'] as const,
  profile: () => [...parentKeys.all, 'profile'] as const,
  settings: () => [...parentKeys.all, 'settings'] as const,
  children: () => [...parentKeys.all, 'children'] as const,
  childById: (id) => [...parentKeys.all, 'children', id] as const,
  childAttendance: (id) => [...parentKeys.all, 'children', id, 'attendance'] as const,
  childGrades: (id) => [...parentKeys.all, 'children', id, 'grades'] as const,
  childHomework: (id) => [...parentKeys.all, 'children', id, 'homework'] as const,
  childFees: (id) => [...parentKeys.all, 'children', id, 'fees'] as const,
  childLibrary: (id) => [...parentKeys.all, 'children', id, 'library'] as const,
  notices: () => [...parentKeys.all, 'notices'] as const,
  chat: () => [...parentKeys.all, 'chat'] as const,
  notifications: () => [...parentKeys.all, 'notifications'] as const,
  allParents: () => [...parentKeys.all, 'all'] as const,
  parentById: (id) => [...parentKeys.all, 'all', id] as const,
};

// =====================
// QUERY HOOKS
// =====================

// Profile & Settings
export const useParentProfile = () => useQuery({
  queryKey: parentKeys.profile(),
  queryFn: api.getParentProfile,
  staleTime: 5 * 60 * 1000,
});

export const useParentSettings = () => useQuery({
  queryKey: parentKeys.settings(),
  queryFn: api.getParentSettings,
  staleTime: 10 * 60 * 1000,
});

// Dashboard & Children
export const useParentDashboard = () => useQuery({
  queryKey: parentKeys.dashboard(),
  queryFn: api.getParentDashboard,
  staleTime: 5 * 60 * 1000,
});

export const useChildrenList = () => useQuery({
  queryKey: parentKeys.children(),
  queryFn: api.getChildrenList,
  staleTime: 5 * 60 * 1000,
});

export const useChildById = (childId) => useQuery({
  queryKey: parentKeys.childById(childId),
  queryFn: () => api.getChildById(childId),
  enabled: !!childId,
  staleTime: 5 * 60 * 1000,
});

export const useChildProfile = (studentId) => useQuery({
  queryKey: parentKeys.childById(studentId),
  queryFn: () => api.getChildProfile(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildTimetable = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'timetable'],
  queryFn: () => api.getChildTimetable(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildCourses = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'courses'],
  queryFn: () => api.getChildCourses(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildTeachers = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'teachers'],
  queryFn: () => api.getChildTeachers(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

// Child Attendance
export const useChildAttendance = (studentId, params = {}) => useQuery({
  queryKey: [...parentKeys.childAttendance(studentId), params],
  queryFn: () => api.getChildAttendance(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildAttendanceSummary = (studentId) => useQuery({
  queryKey: [...parentKeys.childAttendance(studentId), 'summary'],
  queryFn: () => api.getChildAttendanceSummary(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildAttendanceRate = (studentId) => useQuery({
  queryKey: [...parentKeys.childAttendance(studentId), 'rate'],
  queryFn: () => api.getChildAttendanceRate(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

// Child Grades
export const useChildGrades = (studentId) => useQuery({
  queryKey: parentKeys.childGrades(studentId),
  queryFn: () => api.getChildGrades(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildGradeHistory = (studentId) => useQuery({
  queryKey: [...parentKeys.childGrades(studentId), 'history'],
  queryFn: () => api.getChildGradeHistory(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildGPA = (studentId) => useQuery({
  queryKey: [...parentKeys.childGrades(studentId), 'gpa'],
  queryFn: () => api.getChildGPA(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

// Child Homework & Assignments
export const useChildHomework = (studentId) => useQuery({
  queryKey: parentKeys.childHomework(studentId),
  queryFn: () => api.getChildHomework(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildHomeworkDetails = (studentId, homeworkId) => useQuery({
  queryKey: [...parentKeys.childHomework(studentId), homeworkId],
  queryFn: () => api.getChildHomeworkDetails(studentId, homeworkId),
  enabled: !!studentId && !!homeworkId,
  staleTime: 5 * 60 * 1000,
});

export const useChildAssignments = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'assignments'],
  queryFn: () => api.getChildAssignments(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

// Child Tests
export const useChildTests = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'tests'],
  queryFn: () => api.getChildTests(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildTestResults = (studentId, testId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'tests', testId],
  queryFn: () => api.getChildTestResults(studentId, testId),
  enabled: !!studentId && !!testId,
  staleTime: 5 * 60 * 1000,
});

// Child Fees
export const useChildFees = (studentId) => useQuery({
  queryKey: parentKeys.childFees(studentId),
  queryFn: () => api.getChildFees(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildFeeDetails = (studentId, feeId) => useQuery({
  queryKey: [...parentKeys.childFees(studentId), feeId],
  queryFn: () => api.getChildFeeDetails(studentId, feeId),
  enabled: !!studentId && !!feeId,
  staleTime: 5 * 60 * 1000,
});

export const useChildPaymentHistory = (studentId) => useQuery({
  queryKey: [...parentKeys.childFees(studentId), 'payments'],
  queryFn: () => api.getChildPaymentHistory(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildFeeStructure = () => useQuery({
  queryKey: [...parentKeys.all, 'fee-structure'],
  queryFn: api.getChildFeeStructure,
  staleTime: 10 * 60 * 1000,
});

// Child Library
export const useChildBorrowedBooks = (studentId) => useQuery({
  queryKey: [...parentKeys.childLibrary(studentId), 'borrowed'],
  queryFn: () => api.getChildBorrowedBooks(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

export const useChildLibraryHistory = (studentId) => useQuery({
  queryKey: [...parentKeys.childLibrary(studentId), 'history'],
  queryFn: () => api.getChildLibraryHistory(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildOverdueBooks = (studentId) => useQuery({
  queryKey: [...parentKeys.childLibrary(studentId), 'overdue'],
  queryFn: () => api.getChildOverdueBooks(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

// Notices
export const useParentNotices = (params = {}) => useQuery({
  queryKey: [...parentKeys.notices(), params],
  queryFn: () => api.getParentNotices(),
  staleTime: 5 * 60 * 1000,
});

export const useNoticeById = (noticeId) => useQuery({
  queryKey: [...parentKeys.notices(), noticeId],
  queryFn: () => api.getNoticeById(noticeId),
  enabled: !!noticeId,
  staleTime: 5 * 60 * 1000,
});

// Chat
export const useChatContacts = () => useQuery({
  queryKey: parentKeys.chat(),
  queryFn: api.getChatContacts,
  staleTime: 5 * 60 * 1000,
});

export const useMessages = (contactId) => useQuery({
  queryKey: [...parentKeys.chat(), 'messages', contactId],
  queryFn: () => api.getMessages(contactId),
  enabled: !!contactId,
  staleTime: 1 * 60 * 1000,
});

export const useUnreadMessageCount = () => useQuery({
  queryKey: [...parentKeys.chat(), 'unread'],
  queryFn: api.getUnreadMessageCount,
  staleTime: 1 * 60 * 1000,
});

// Notifications
export const useParentNotifications = (params = {}) => useQuery({
  queryKey: [...parentKeys.notifications(), params],
  queryFn: () => api.getParentNotifications(params),
  staleTime: 5 * 60 * 1000,
});

export const useNotificationSettings = () => useQuery({
  queryKey: [...parentKeys.notifications(), 'settings'],
  queryFn: api.getNotificationSettings,
  staleTime: 10 * 60 * 1000,
});

// Child Performance
export const useChildPerformanceOverview = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'performance'],
  queryFn: () => api.getChildPerformanceOverview(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildRank = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'rank'],
  queryFn: () => api.getChildRank(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildProgress = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'progress'],
  queryFn: () => api.getChildProgress(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

// Child Groups
export const useChildGroups = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'groups'],
  queryFn: () => api.getChildGroups(studentId),
  enabled: !!studentId,
  staleTime: 10 * 60 * 1000,
});

export const useChildAnnouncements = (studentId) => useQuery({
  queryKey: [...parentKeys.childById(studentId), 'announcements'],
  queryFn: () => api.getChildAnnouncements(studentId),
  enabled: !!studentId,
  staleTime: 5 * 60 * 1000,
});

// Admin: All Parents
export const useAllParents = (params = {}) => useQuery({
  queryKey: [...parentKeys.allParents(), params],
  queryFn: () => api.getAllParents(params),
  staleTime: 5 * 60 * 1000,
});

export const useParentById = (parentId) => useQuery({
  queryKey: parentKeys.parentById(parentId),
  queryFn: () => api.getParentById(parentId),
  enabled: !!parentId,
  staleTime: 5 * 60 * 1000,
});

export const useParentLinkedStudents = (parentId) => useQuery({
  queryKey: [...parentKeys.parentById(parentId), 'students'],
  queryFn: () => api.getParentLinkedStudents(parentId),
  enabled: !!parentId,
  staleTime: 5 * 60 * 1000,
});

// =====================
// MUTATION HOOKS
// =====================

// Profile
export const useUpdateParentProfile = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateParentProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.profile() });
      parentToast.profile.update();
    },
    onError: () => parentToast.profile.error(),
  });
};

export const useUpdateParentSettings = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateParentSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.settings() });
      parentToast.settings.update();
    },
    onError: () => parentToast.settings.error(),
  });
};

export const useChangeParentPassword = () => {
  return useMutation({
    mutationFn: api.changeParentPassword,
    onSuccess: () => parentToast.password.change(),
    onError: () => parentToast.password.error(),
  });
};

// Notices
export const useMarkNoticeAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markNoticeAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.notices() });
    },
  });
};

// Chat
export const useSendMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.sendMessage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.chat() });
      parentToast.message.send();
    },
    onError: () => parentToast.message.error(),
  });
};

export const useMarkMessageAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markMessageAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.chat() });
    },
  });
};

// Notifications
export const useMarkNotificationAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markNotificationAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.notifications() });
    },
  });
};

export const useMarkAllNotificationsAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markAllNotificationsAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.notifications() });
      parentToast.notifications.readAll();
    },
    onError: () => parentToast.notifications.error(),
  });
};

export const useUpdateNotificationSettings = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateNotificationSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [...parentKeys.notifications(), 'settings'] });
      parentToast.settings.update();
    },
    onError: () => parentToast.settings.error(),
  });
};

// Admin: Parents
export const useCreateParent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createParent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.allParents() });
      parentToast.admin.create();
    },
    onError: () => parentToast.admin.error(),
  });
};

export const useUpdateParent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => api.updateParent(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: parentKeys.allParents() });
      queryClient.invalidateQueries({ queryKey: parentKeys.parentById(id) });
      parentToast.admin.update();
    },
    onError: () => parentToast.admin.error(),
  });
};

export const useDeleteParent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteParent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.allParents() });
      parentToast.admin.delete();
    },
    onError: () => parentToast.admin.error(),
  });
};

export const useLinkStudentToParent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ parentId, studentId }) => api.linkStudentToParent(parentId, studentId),
    onSuccess: (_, { parentId }) => {
      queryClient.invalidateQueries({ queryKey: parentKeys.parentById(parentId) });
      parentToast.admin.link();
    },
    onError: () => parentToast.admin.error(),
  });
};

export const useUnlinkStudentFromParent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ parentId, studentId }) => api.unlinkStudentFromParent(parentId, studentId),
    onSuccess: (_, { parentId }) => {
      queryClient.invalidateQueries({ queryKey: parentKeys.parentById(parentId) });
      parentToast.admin.unlink();
    },
    onError: () => parentToast.admin.error(),
  });
};

export default {
  parentKeys,
  useParentProfile,
  useParentSettings,
  useParentDashboard,
  useChildrenList,
  useChildById,
  useChildProfile,
  useChildTimetable,
  useChildCourses,
  useChildTeachers,
  useChildAttendance,
  useChildAttendanceSummary,
  useChildAttendanceRate,
  useChildGrades,
  useChildGradeHistory,
  useChildGPA,
  useChildHomework,
  useChildHomeworkDetails,
  useChildAssignments,
  useChildTests,
  useChildTestResults,
  useChildFees,
  useChildFeeDetails,
  useChildPaymentHistory,
  useChildFeeStructure,
  useChildBorrowedBooks,
  useChildLibraryHistory,
  useChildOverdueBooks,
  useParentNotices,
  useNoticeById,
  useChatContacts,
  useMessages,
  useUnreadMessageCount,
  useParentNotifications,
  useNotificationSettings,
  useChildPerformanceOverview,
  useChildRank,
  useChildProgress,
  useChildGroups,
  useChildAnnouncements,
  useAllParents,
  useParentById,
  useParentLinkedStudents,
};
