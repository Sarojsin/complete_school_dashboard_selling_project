import api from '../../../shared/api/client';

// With missing endpoints from Plan 5

// Get chat contacts
export const getChatContacts = () => api.get('/chat/contacts');
export const searchContacts = (query) => api.get('/chat/contacts', { params: { search: query } });
export const getContactById = (contactId) => api.get(`/chat/contacts/${contactId}`);
export const getContactOnlineStatus = (contactId) => api.get(`/chat/contacts/${contactId}/status`);

// Messages
export const getMessages = (contactId, params) => api.get(`/chat/messages/${contactId}`, { params });
export const sendMessage = (data) => api.post('/chat/messages', data);
export const sendMediaMessage = (formData) => api.post('/chat/messages/media', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const deleteMessage = (messageId) => api.delete(`/chat/messages/${messageId}`);
export const editMessage = (messageId, data) => api.put(`/chat/messages/${messageId}`, data);
export const markAsRead = (contactId) => api.patch(`/chat/messages/${contactId}/read`);
export const markMessageAsRead = (messageId) => api.patch(`/chat/messages/${messageId}/read`);
export const markAllAsRead = () => api.patch('/chat/messages/read-all');
export const getUnreadCount = () => api.get('/chat/unread');
export const getUnreadMessages = () => api.get('/chat/messages/unread');

// Conversations
export const getConversations = (params) => api.get('/chat/conversations', { params });
export const getConversationById = (conversationId) => api.get(`/chat/conversations/${conversationId}`);
export const createConversation = (data) => api.post('/chat/conversations', data);
export const deleteConversation = (conversationId) => api.delete(`/chat/conversations/${conversationId}`);
export const archiveConversation = (conversationId) => api.patch(`/chat/conversations/${conversationId}/archive`);
export const muteConversation = (conversationId, duration) => api.patch(`/chat/conversations/${conversationId}/mute`, { duration });
export const pinConversation = (conversationId) => api.patch(`/chat/conversations/${conversationId}/pin`);
export const getPinnedConversations = () => api.get('/chat/conversations/pinned');
export const getArchivedConversations = () => api.get('/chat/conversations/archived');

// Groups (Chat Groups)
export const getChatGroups = () => api.get('/chat/groups');
export const getChatGroupById = (groupId) => api.get(`/chat/groups/${groupId}`);
export const createChatGroup = (data) => api.post('/chat/groups', data);
export const updateChatGroup = (groupId, data) => api.put(`/chat/groups/${groupId}`, data);
export const deleteChatGroup = (groupId) => api.delete(`/chat/groups/${groupId}`);
export const addGroupMembers = (groupId, data) => api.post(`/chat/groups/${groupId}/members`, data);
export const removeGroupMember = (groupId, userId) => api.delete(`/chat/groups/${groupId}/members/${userId}`);
export const leaveChatGroup = (groupId) => api.post(`/chat/groups/${groupId}/leave`);
export const getGroupMembers = (groupId) => api.get(`/chat/groups/${groupId}/members`);
export const getGroupMessages = (groupId, params) => api.get(`/chat/groups/${groupId}/messages`, { params });
export const sendGroupMessage = (groupId, data) => api.post(`/chat/groups/${groupId}/messages`, data);
export const adminRemoveMessage = (groupId, messageId) => api.delete(`/chat/groups/${groupId}/messages/${messageId}`);

// Typing & Presence
export const sendTypingIndicator = (contactId) => api.post(`/chat/typing/${contactId}`);
export const getTypingStatus = (contactId) => api.get(`/chat/typing/${contactId}`);
export const setOnlineStatus = (status) => api.post('/chat/status', { status });
export const getOnlineUsers = () => api.get('/chat/online');

// Message Search
export const searchMessages = (query, params) => api.get('/chat/search', { params: { q: query, ...params } });
export const searchInConversation = (conversationId, query) => api.get(`/chat/conversations/${conversationId}/search`, { params: { q: query } });

// Attachments
export const uploadAttachment = (formData) => api.post('/chat/attachments', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const getAttachment = (attachmentId) => api.get(`/chat/attachments/${attachmentId}`);
export const deleteAttachment = (attachmentId) => api.delete(`/chat/attachments/${attachmentId}`);
export const downloadAttachment = (attachmentId) => api.get(`/chat/attachments/${attachmentId}/download`, { responseType: 'blob' });

// Notifications & Settings
export const getChatSettings = () => api.get('/chat/settings');
export const updateChatSettings = (data) => api.put('/chat/settings', data);
export const getChatNotifications = (params) => api.get('/chat/notifications', { params });
export const markNotificationAsRead = (notificationId) => api.patch(`/chat/notifications/${notificationId}/read`);
export const clearChatNotifications = () => api.delete('/chat/notifications');

// Block & Report
export const blockUser = (userId) => api.post('/chat/block', { user_id: userId });
export const unblockUser = (userId) => api.delete(`/chat/block/${userId}`);
export const getBlockedUsers = () => api.get('/chat/blocked');
export const reportUser = (data) => api.post('/chat/report', data);
export const reportMessage = (messageId, data) => api.post(`/chat/messages/${messageId}/report`, data);

// Message Reactions
export const addReaction = (messageId, emoji) => api.post(`/chat/messages/${messageId}/reactions`, { emoji });
export const removeReaction = (messageId, emoji) => api.delete(`/chat/messages/${messageId}/reactions/${emoji}`);
export const getReactions = (messageId) => api.get(`/chat/messages/${messageId}/reactions`);

// Read Receipts
export const getReadReceipts = (messageId) => api.get(`/chat/messages/${messageId}/receipts`);
export const updateReadReceipt = (messageId) => api.patch(`/chat/messages/${messageId}/receipt`);

// Message Templates
export const getMessageTemplates = () => api.get('/chat/templates');
export const createMessageTemplate = (data) => api.post('/chat/templates', data);
export const deleteMessageTemplate = (templateId) => api.delete(`/chat/templates/${templateId}`);
export const useMessageTemplate = (templateId, data) => api.post(`/chat/templates/${templateId}/use`, data);
