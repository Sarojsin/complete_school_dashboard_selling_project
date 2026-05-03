import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '../api/videos';

export const videoKeys = { all: ['videos'], list: (p) => [...videoKeys.all, 'list', p], byId: (id) => [...videoKeys.all, id], byCourse: (id) => [...videoKeys.all, 'course', id], search: (q) => [...videoKeys.all, 'search', q], my: () => [...videoKeys.all, 'my'], featured: () => [...videoKeys.all, 'featured'], popular: () => [...videoKeys.all, 'popular'] };

export const useVideos = (p = {}, o = {}) => useQuery({ queryKey: videoKeys.list(p), queryFn: () => api.getVideos(p), ...o });
export const useVideo = (id, o = {}) => useQuery({ queryKey: videoKeys.byId(id), queryFn: () => api.getVideo(id), enabled: !!id, ...o });
export const useVideosByCourse = (courseId, o = {}) => useQuery({ queryKey: videoKeys.byCourse(courseId), queryFn: () => api.getVideosByCourse(courseId), enabled: !!courseId, ...o });
export const useSearchVideos = (q, o = {}) => useQuery({ queryKey: videoKeys.search(q), queryFn: () => api.searchVideos(q), enabled: !!q, ...o });
export const useFeaturedVideos = (o = {}) => useQuery({ queryKey: videoKeys.featured(), queryFn: api.getFeaturedVideos, ...o });
export const usePopularVideos = (o = {}) => useQuery({ queryKey: videoKeys.popular(), queryFn: api.getPopularVideos, ...o });
export const useMyVideos = (o = {}) => useQuery({ queryKey: videoKeys.my(), queryFn: api.getMyVideos, ...o });
export const useVideoCategories = (o = {}) => useQuery({ queryKey: [...videoKeys.all, 'categories'], queryFn: api.getCategories, ...o });
export const useVideoProgress = (videoId, o = {}) => useQuery({ queryKey: [...videoKeys.byId(videoId), 'progress'], queryFn: () => api.getVideoProgress(videoId), enabled: !!videoId, ...o });
export const useVideoComments = (videoId, o = {}) => useQuery({ queryKey: [...videoKeys.byId(videoId), 'comments'], queryFn: () => api.getVideoComments(videoId), enabled: !!videoId, ...o });
export const useRecommendedVideos = (videoId, o = {}) => useQuery({ queryKey: [...videoKeys.byId(videoId), 'recommended'], queryFn: () => api.getRecommendedVideos(videoId), enabled: !!videoId, ...o });
export const usePlaylists = (o = {}) => useQuery({ queryKey: [...videoKeys.all, 'playlists'], queryFn: api.getPlaylists, ...o });

export const useCreateVideo = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createVideo, onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useUpdateVideo = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ id, data }) => api.updateVideo(id, data), onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useDeleteVideo = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.deleteVideo, onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useLikeVideo = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.likeVideo, onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useWatchVideo = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.watchVideo, onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useAddVideoComment = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ videoId, data }) => api.addVideoComment(videoId, data), onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useUpdateVideoProgress = () => { const qc = useQueryClient(); return useMutation({ mutationFn: ({ videoId, seconds }) => api.updateVideoProgress(videoId, seconds), onSuccess: () => qc.invalidateQueries({ queryKey: videoKeys.all }) }); };
export const useCreatePlaylist = () => { const qc = useQueryClient(); return useMutation({ mutationFn: api.createPlaylist, onSuccess: () => qc.invalidateQueries({ queryKey: [...videoKeys.all, 'playlists'] }) }); };
