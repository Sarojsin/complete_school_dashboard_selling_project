// =====================
// USE CHAT - TanStack Query Hooks
// Chat Module - Plan 5 Implementation
// =====================

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/chat';
import { chatToast } from '../lib/toast';

// Query Keys
export const chatKeys = {
  all: ['chat'] as const,
  contacts: () => [...chatKeys.all, 'contacts'] as const,
  contactById: (id) => [...chatKeys.all, 'contacts', id] as const,
  messages: (contactId) => [...chatKeys.all, 'messages', contactId] as const,
  conversations: () => [...chatKeys.all, 'conversations'] as const,
  conversationById: (id) => [...chatKeys.all, 'conversations', id] as const,
  groups: () => [...chatKeys.all, 'groups'] as const,
  groupById: (id) => [...chatKeys.all, 'groups', id] as const,
  groupMembers: (groupId) => [...chatKeys.all, 'groups', groupId, 'members'] as const,
  groupMessages: (groupId) => [...chatKeys.all, 'groups', groupId, 'messages'] as const,
  unread: () => [...chatKeys.all, 'unread'] as const,
  online: () => [...chatKeys.all, 'online'] as const,
  pinned: () => [...chatKeys.all, 'pinned'] as const,
  archived: () => [...chatKeys.all, 'archived'] as const,
  settings: () => [...chatKeys.all, 'settings'] as const,
  notifications: () => [...chatKeys.all, 'notifications'] as const,
  blocked: () => [...chatKeys.all, 'blocked'] as const,
  search: (query) => [...chatKeys.all, 'search', query] as const,
  typing: (contactId) => [...chatKeys.all, 'typing', contactId] as const,
};

// =====================
// QUERY HOOKS
// =====================

// Contacts
export const useChatContacts = (params = {}) => useQuery({
  queryKey: [...chatKeys.contacts(), params],
  queryFn: () => api.getChatContacts(),
  staleTime: 5 * 60 * 1000,
});

export const useContactById = (contactId) => useQuery({
  queryKey: chatKeys.contactById(contactId),
  queryFn: () => api.getContactById(contactId),
  enabled: !!contactId,
  staleTime: 5 * 60 * 1000,
});

export const useContactOnlineStatus = (contactId) => useQuery({
  queryKey: [...chatKeys.contactById(contactId), 'status'],
  queryFn: () => api.getContactOnlineStatus(contactId),
  enabled: !!contactId,
  staleTime: 30 * 1000, // Check every 30 seconds
});

export const useSearchContacts = (query) => useQuery({
  queryKey: [...chatKeys.contacts(), 'search', query],
  queryFn: () => api.searchContacts(query),
  enabled: !!query,
  staleTime: 1 * 60 * 1000,
});

// Messages
export const useMessages = (contactId, params = {}) => useQuery({
  queryKey: [...chatKeys.messages(contactId), params],
  queryFn: () => api.getMessages(contactId, params),
  enabled: !!contactId,
  staleTime: 1 * 60 * 1000,
});

export const useUnreadMessages = () => useQuery({
  queryKey: chatKeys.unread(),
  queryFn: api.getUnreadMessages,
  staleTime: 1 * 60 * 1000,
});

// Conversations
export const useConversations = (params = {}) => useQuery({
  queryKey: [...chatKeys.conversations(), params],
  queryFn: () => api.getConversations(params),
  staleTime: 5 * 60 * 1000,
});

export const useConversationById = (conversationId) => useQuery({
  queryKey: chatKeys.conversationById(conversationId),
  queryFn: () => api.getConversationById(conversationId),
  enabled: !!conversationId,
  staleTime: 5 * 60 * 1000,
});

export const usePinnedConversations = () => useQuery({
  queryKey: chatKeys.pinned(),
  queryFn: api.getPinnedConversations,
  staleTime: 5 * 60 * 1000,
});

export const useArchivedConversations = () => useQuery({
  queryKey: chatKeys.archived(),
  queryFn: api.getArchivedConversations,
  staleTime: 5 * 60 * 1000,
});

// Chat Groups
export const useChatGroups = () => useQuery({
  queryKey: chatKeys.groups(),
  queryFn: api.getChatGroups,
  staleTime: 10 * 60 * 1000,
});

export const useChatGroupById = (groupId) => useQuery({
  queryKey: chatKeys.groupById(groupId),
  queryFn: () => api.getChatGroupById(groupId),
  enabled: !!groupId,
  staleTime: 10 * 60 * 1000,
});

export const useGroupMembers = (groupId) => useQuery({
  queryKey: chatKeys.groupMembers(groupId),
  queryFn: () => api.getGroupMembers(groupId),
  enabled: !!groupId,
  staleTime: 10 * 60 * 1000,
});

export const useGroupMessages = (groupId, params = {}) => useQuery({
  queryKey: [...chatKeys.groupMessages(groupId), params],
  queryFn: () => api.getGroupMessages(groupId, params),
  enabled: !!groupId,
  staleTime: 1 * 60 * 1000,
});

// Presence
export const useOnlineUsers = () => useQuery({
  queryKey: chatKeys.online(),
  queryFn: api.getOnlineUsers,
  staleTime: 30 * 1000, // Check every 30 seconds
});

export const useTypingStatus = (contactId) => useQuery({
  queryKey: chatKeys.typing(contactId),
  queryFn: () => api.getTypingStatus(contactId),
  enabled: !!contactId,
  staleTime: 10 * 1000, // Check every 10 seconds
});

// Search
export const useSearchMessages = (query, params = {}) => useQuery({
  queryKey: [...chatKeys.search(query), params],
  queryFn: () => api.searchMessages(query, params),
  enabled: !!query,
  staleTime: 5 * 60 * 1000,
});

export const useSearchInConversation = (conversationId, query) => useQuery({
  queryKey: [...chatKeys.conversationById(conversationId), 'search', query],
  queryFn: () => api.searchInConversation(conversationId, query),
  enabled: !!conversationId && !!query,
  staleTime: 5 * 60 * 1000,
});

// Settings & Notifications
export const useChatSettings = () => useQuery({
  queryKey: chatKeys.settings(),
  queryFn: api.getChatSettings,
  staleTime: 10 * 60 * 1000,
});

export const useChatNotifications = (params = {}) => useQuery({
  queryKey: [...chatKeys.notifications(), params],
  queryFn: () => api.getChatNotifications(params),
  staleTime: 5 * 60 * 1000,
});

// Blocked Users
export const useBlockedUsers = () => useQuery({
  queryKey: chatKeys.blocked(),
  queryFn: api.getBlockedUsers,
  staleTime: 10 * 60 * 1000,
});

// Unread Count (Quick Access)
export const useUnreadCount = () => useQuery({
  queryKey: chatKeys.unread(),
  queryFn: api.getUnreadCount,
  staleTime: 1 * 60 * 1000,
});

// =====================
// MUTATION HOOKS
// =====================

// Messages
export const useSendMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.sendMessage,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(variables.contact_id || variables.receiver_id) });
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      chatToast.message.send();
    },
    onError: () => chatToast.message.error(),
  });
};

export const useSendMediaMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.sendMediaMessage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      chatToast.message.send();
    },
    onError: () => chatToast.message.error(),
  });
};

export const useDeleteMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteMessage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages });
      chatToast.message.delete();
    },
    onError: () => chatToast.message.error(),
  });
};

export const useEditMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ messageId, data }) => api.editMessage(messageId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages });
      chatToast.message.update();
    },
    onError: () => chatToast.message.error(),
  });
};

export const useMarkAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.unread() });
      queryClient.invalidateQueries({ queryKey: chatKeys.messages });
    },
  });
};

export const useMarkMessageAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markMessageAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.unread() });
    },
  });
};

export const useMarkAllAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markAllAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.unread() });
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      chatToast.message.readAll();
    },
    onError: () => chatToast.message.error(),
  });
};

// Conversations
export const useCreateConversation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      chatToast.conversation.create();
    },
    onError: () => chatToast.conversation.error(),
  });
};

export const useDeleteConversation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      chatToast.conversation.delete();
    },
    onError: () => chatToast.conversation.error(),
  });
};

export const useArchiveConversation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.archiveConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      queryClient.invalidateQueries({ queryKey: chatKeys.archived() });
      chatToast.conversation.archive();
    },
    onError: () => chatToast.conversation.error(),
  });
};

export const useMuteConversation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ conversationId, duration }) => api.muteConversation(conversationId, duration),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      chatToast.conversation.mute();
    },
    onError: () => chatToast.conversation.error(),
  });
};

export const usePinConversation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.pinConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
      queryClient.invalidateQueries({ queryKey: chatKeys.pinned() });
      chatToast.conversation.pin();
    },
    onError: () => chatToast.conversation.error(),
  });
};

// Chat Groups
export const useCreateChatGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createChatGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groups() });
      chatToast.group.create();
    },
    onError: () => chatToast.group.error(),
  });
};

export const useUpdateChatGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, data }) => api.updateChatGroup(groupId, data),
    onSuccess: (_, { groupId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groupById(groupId) });
      chatToast.group.update();
    },
    onError: () => chatToast.group.error(),
  });
};

export const useDeleteChatGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.deleteChatGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groups() });
      chatToast.group.delete();
    },
    onError: () => chatToast.group.error(),
  });
};

export const useAddGroupMembers = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, data }) => api.addGroupMembers(groupId, data),
    onSuccess: (_, { groupId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groupMembers(groupId) });
      chatToast.group.addMember();
    },
    onError: () => chatToast.group.error(),
  });
};

export const useRemoveGroupMember = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, userId }) => api.removeGroupMember(groupId, userId),
    onSuccess: (_, { groupId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groupMembers(groupId) });
      chatToast.group.removeMember();
    },
    onError: () => chatToast.group.error(),
  });
};

export const useLeaveChatGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.leaveChatGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groups() });
      chatToast.group.leave();
    },
    onError: () => chatToast.group.error(),
  });
};

export const useSendGroupMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, data }) => api.sendGroupMessage(groupId, data),
    onSuccess: (_, { groupId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.groupMessages(groupId) });
      chatToast.message.send();
    },
    onError: () => chatToast.message.error(),
  });
};

// Typing
export const useSendTypingIndicator = () => {
  return useMutation({
    mutationFn: api.sendTypingIndicator,
  });
};

// Settings
export const useUpdateChatSettings = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateChatSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.settings() });
      chatToast.settings.update();
    },
    onError: () => chatToast.settings.error(),
  });
};

// Notifications
export const useMarkChatNotificationAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markNotificationAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.notifications() });
    },
  });
};

export const useClearChatNotifications = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.clearChatNotifications,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.notifications() });
      chatToast.notifications.clear();
    },
    onError: () => chatToast.notifications.error(),
  });
};

// Block & Report
export const useBlockUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.blockUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.blocked() });
      queryClient.invalidateQueries({ queryKey: chatKeys.contacts() });
      chatToast.block.block();
    },
    onError: () => chatToast.block.error(),
  });
};

export const useUnblockUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.unblockUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.blocked() });
      chatToast.block.unblock();
    },
    onError: () => chatToast.block.error(),
  });
};

export const useReportUser = () => {
  return useMutation({
    mutationFn: api.reportUser,
    onSuccess: () => chatToast.report.submit(),
    onError: () => chatToast.report.error(),
  });
};

export const useReportMessage = () => {
  return useMutation({
    mutationFn: ({ messageId, data }) => api.reportMessage(messageId, data),
    onSuccess: () => chatToast.report.submit(),
    onError: () => chatToast.report.error(),
  });
};

// Reactions
export const useAddReaction = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ messageId, emoji }) => api.addReaction(messageId, emoji),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages });
    },
  });
};

export const useRemoveReaction = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ messageId, emoji }) => api.removeReaction(messageId, emoji),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages });
    },
  });
};

export default {
  chatKeys,
  useChatContacts,
  useContactById,
  useContactOnlineStatus,
  useSearchContacts,
  useMessages,
  useUnreadMessages,
  useConversations,
  useConversationById,
  usePinnedConversations,
  useArchivedConversations,
  useChatGroups,
  useChatGroupById,
  useGroupMembers,
  useGroupMessages,
  useOnlineUsers,
  useTypingStatus,
  useSearchMessages,
  useSearchInConversation,
  useChatSettings,
  useChatNotifications,
  useBlockedUsers,
  useUnreadCount,
};
