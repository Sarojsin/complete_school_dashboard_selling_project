// =====================
// USE GROUPS - TanStack Query Hooks
// Groups Module - Plan 7 Implementation
// =====================

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/groups';
import { groupsToast } from '../lib/toast';

export const groupsKeys = { all: ['groups'], list: () => [...groupsKeys.all, 'list'], byId: (id) => [...groupsKeys.all, id], posts: (id) => [...groupsKeys.all, id, 'posts'], members: (id) => [...groupsKeys.all, id, 'members'] };

export const useAllGroups = (params) => useQuery({ queryKey: [...groupsKeys.list(), params], queryFn: () => api.getAllGroups(params), staleTime: 5 * 60 * 1000 });
export const useMyGroups = () => useQuery({ queryKey: [...groupsKeys.all, 'my'], queryFn: api.getMyGroups, staleTime: 5 * 60 * 1000 });
export const useGroupById = (id) => useQuery({ queryKey: groupsKeys.byId(id), queryFn: () => api.getGroupById(id), enabled: !!id, staleTime: 5 * 60 * 1000 });
export const useGroupPosts = (id, params) => useQuery({ queryKey: [...groupsKeys.posts(id), params], queryFn: () => api.getGroupPosts(id, params), enabled: !!id, staleTime: 5 * 60 * 1000 });
export const useGroupMembers = (id, params) => useQuery({ queryKey: [...groupsKeys.members(id), params], queryFn: () => api.getGroupMembers(id, params), enabled: !!id, staleTime: 5 * 60 * 1000 });
export const useSearchGroups = (q) => useQuery({ queryKey: [...groupsKeys.all, 'search', q], queryFn: () => api.searchGroups(q), enabled: !!q, staleTime: 5 * 60 * 1000 });
export const usePendingRequests = (id) => useQuery({ queryKey: [...groupsKeys.all, id, 'requests'], queryFn: () => api.getPendingJoinRequests(id), enabled: !!id, staleTime: 5 * 60 * 1000 });
export const useGroupAnnouncements = (id) => useQuery({ queryKey: [...groupsKeys.all, id, 'announcements'], queryFn: () => api.getGroupAnnouncements(id), enabled: !!id, staleTime: 5 * 60 * 1000 });

export const useCreateGroup = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createGroup, onSuccess: () => { qc.invalidateQueries({ queryKey: groupsKeys.list() }); groupsToast.group.create(); }, onError: () => groupsToast.error() }); };
export const useUpdateGroup = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateGroup(id, data), onSuccess: (_, { id }) => { qc.invalidateQueries({ queryKey: groupsKeys.byId(id) }); groupsToast.group.update(); }, onError: () => groupsToast.error() }); };
export const useDeleteGroup = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteGroup, onSuccess: () => { qc.invalidateQueries({ queryKey: groupsKeys.list() }); groupsToast.group.delete(); }, onError: () => groupsToast.error() }); };
export const useJoinGroup = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.joinGroup, onSuccess: () => { qc.invalidateQueries({ queryKey: groupsKeys.all }); groupsToast.group.join(); }, onError: () => groupsToast.error() }); };
export const useLeaveGroup = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.leaveGroup, onSuccess: () => { qc.invalidateQueries({ queryKey: groupsKeys.all }); groupsToast.group.leave(); }, onError: () => groupsToast.error() }); };
export const useCreatePost = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.createGroupPost(id, data), onSuccess: (_, { id }) => { qc.invalidateQueries({ queryKey: groupsKeys.posts(id) }); groupsToast.post.create(); }, onError: () => groupsToast.error() }); };
export const useDeletePost = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ gid, pid }) => api.deleteGroupPost(gid, pid), onSuccess: (_, { gid }) => { qc.invalidateQueries({ queryKey: groupsKeys.posts(gid) }); groupsToast.post.delete(); }, onError: () => groupsToast.error() }); };
export const useLikePost = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ gid, pid }) => api.likePost(gid, pid), onSuccess: (_, { gid }) => qc.invalidateQueries({ queryKey: groupsKeys.posts(gid) }), onError: () => groupsToast.error() }); };
export const useAddComment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ gid, pid, data }) => api.addComment(gid, pid, data), onSuccess: (_, { gid }) => qc.invalidateQueries({ queryKey: groupsKeys.posts(gid) }), onError: () => groupsToast.error() }); };
export const useAddMember = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.addGroupMember(id, data), onSuccess: (_, { id }) => { qc.invalidateQueries({ queryKey: groupsKeys.members(id) }); groupsToast.member.add(); }, onError: () => groupsToast.error() }); };
export const useRemoveMember = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ gid, uid }) => api.removeGroupMember(gid, uid), onSuccess: (_, { gid }) => { qc.invalidateQueries({ queryKey: groupsKeys.members(gid) }); groupsToast.member.remove(); }, onError: () => groupsToast.error() }); };
export const useApproveRequest = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ gid, rid }) => api.approveJoinRequest(gid, rid), onSuccess: (_, { gid }) => { qc.invalidateQueries({ queryKey: [...groupsKeys.all, gid, 'requests'] }); qc.invalidateQueries({ queryKey: groupsKeys.members(gid) }); groupsToast.request.approve(); }, onError: () => groupsToast.error() }); };
export const useRejectRequest = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ gid, rid }) => api.rejectJoinRequest(gid, rid), onSuccess: (_, { gid }) => { qc.invalidateQueries({ queryKey: [...groupsKeys.all, gid, 'requests'] }); groupsToast.request.reject(); }, onError: () => groupsToast.error() }); };
export const useCreateAnnouncement = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.createAnnouncement(id, data), onSuccess: (_, { id }) => { qc.invalidateQueries({ queryKey: [...groupsKeys.all, id, 'announcements'] }); groupsToast.announcement.create(); }, onError: () => groupsToast.error() }); };

export default { groupsKeys, useAllGroups, useMyGroups, useGroupById, useGroupPosts, useGroupMembers };
