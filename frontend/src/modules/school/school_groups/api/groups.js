import api from '../../../shared/api/client';

// With missing endpoints from Plan 7

// Groups
export const getAllGroups = (params) => api.get('/groups/', { params });
export const getGroupById = (groupId) => api.get(`/groups/${groupId}`);
export const createGroup = (data) => api.post('/groups/', data);
export const updateGroup = (groupId, data) => api.put(`/groups/${groupId}`, data);
export const deleteGroup = (groupId) => api.delete(`/groups/${groupId}`);
export const joinGroup = (code) => api.post('/groups/join', { code });
export const leaveGroup = (groupId) => api.post(`/groups/${groupId}/leave`);
export const getMyGroups = () => api.get('/groups/my');
export const searchGroups = (query, params) => api.get('/groups/', { params: { search: query, ...params } });
export const getGroupByCode = (code) => api.get(`/groups/code/${code}`);
export const getPublicGroups = () => api.get('/groups/public');
export const getGroupSettings = (groupId) => api.get(`/groups/${groupId}/settings`);
export const updateGroupSettings = (groupId, data) => api.put(`/groups/${groupId}/settings`, data);
export const getGroupAnalytics = (groupId) => api.get(`/groups/${groupId}/analytics`);
export const exportGroupMembers = (groupId) => api.get(`/groups/${groupId}/export`, { responseType: 'blob' });

// Posts
export const getGroupPosts = (groupId, params) => api.get(`/groups/${groupId}/posts`, { params });
export const getPostById = (groupId, postId) => api.get(`/groups/${groupId}/posts/${postId}`);
export const createGroupPost = (groupId, data) => api.post(`/groups/${groupId}/posts`, data);
export const updateGroupPost = (groupId, postId, data) => api.put(`/groups/${groupId}/posts/${postId}`, data);
export const deleteGroupPost = (groupId, postId) => api.delete(`/groups/${groupId}/posts/${postId}`);
export const likePost = (groupId, postId) => api.post(`/groups/${groupId}/posts/${postId}/like`);
export const unlikePost = (groupId, postId) => api.delete(`/groups/${groupId}/posts/${postId}/like`);
export const getPostComments = (groupId, postId) => api.get(`/groups/${groupId}/posts/${postId}/comments`);
export const addComment = (groupId, postId, data) => api.post(`/groups/${groupId}/posts/${postId}/comments`, data);
export const deleteComment = (groupId, postId, commentId) => api.delete(`/groups/${groupId}/posts/${postId}/comments/${commentId}`);
export const pinPost = (groupId, postId) => api.patch(`/groups/${groupId}/posts/${postId}/pin`);
export const reportPost = (groupId, postId, data) => api.post(`/groups/${groupId}/posts/${postId}/report`, data);

// Members
export const getGroupMembers = (groupId, params) => api.get(`/groups/${groupId}/members`, { params });
export const addGroupMember = (groupId, data) => api.post(`/groups/${groupId}/members`, data);
export const addGroupMembers = (groupId, data) => api.post(`/groups/${groupId}/members/bulk`, data);
export const removeGroupMember = (groupId, userId) => api.delete(`/groups/${groupId}/members/${userId}`);
export const updateMemberRole = (groupId, userId, data) => api.patch(`/groups/${groupId}/members/${userId}/role`, data);
export const promoteToAdmin = (groupId, userId) => api.post(`/groups/${groupId}/members/${userId}/promote`);
export const demoteFromAdmin = (groupId, userId) => api.post(`/groups/${groupId}/members/${userId}/demote`);
export const getPendingJoinRequests = (groupId) => api.get(`/groups/${groupId}/join-requests`);
export const approveJoinRequest = (groupId, requestId) => api.post(`/groups/${groupId}/join-requests/${requestId}/approve`);
export const rejectJoinRequest = (groupId, requestId) => api.post(`/groups/${groupId}/join-requests/${requestId}/reject`);
export const banMember = (groupId, userId) => api.post(`/groups/${groupId}/members/${userId}/ban`);
export const unbanMember = (groupId, userId) => api.delete(`/groups/${groupId}/members/${userId}/ban`);
export const getBannedMembers = (groupId) => api.get(`/groups/${groupId}/banned`);

// Announcements
export const getGroupAnnouncements = (groupId) => api.get(`/groups/${groupId}/announcements`);
export const createAnnouncement = (groupId, data) => api.post(`/groups/${groupId}/announcements`, data);
export const deleteAnnouncement = (groupId, announcementId) => api.delete(`/groups/${groupId}/announcements/${announcementId}`);
