import api from '../../../shared/api/client';

// Get all videos
export const getVideos = (params) => {
  return api.get('/videos', { params });
};

// Get video by ID
export const getVideo = (videoId) => {
  return api.get(`/videos/${videoId}`);
};

// Create video
export const createVideo = (data) => {
  return api.post('/videos', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

// Update video
export const updateVideo = (videoId, data) => {
  return api.put(`/videos/${videoId}`, data);
};

// Delete video
export const deleteVideo = (videoId) => {
  return api.delete(`/videos/${videoId}`);
};

// Get videos by subject
export const getVideosBySubject = (subjectId) => {
  return api.get(`/videos/subject/${subjectId}`);
};

// Get video categories
export const getCategories = () => {
  return api.get('/videos/categories');
};

// ============================================
// NEW: Extended Video Management
// ============================================

export const getVideosByCourse = (courseId) => api.get(`/videos/course/${courseId}`);
export const searchVideos = (query) => api.get('/videos/search', { params: { q: query } });
export const getFeaturedVideos = () => api.get('/videos/featured');
export const getPopularVideos = () => api.get('/videos/popular');
export const getMyVideos = () => api.get('/videos/my');
export const getVideoStreamUrl = (videoId) => api.get(`/videos/${videoId}/stream`);
export const watchVideo = (videoId) => api.put(`/videos/${videoId}/watch`);
export const likeVideo = (videoId) => api.post(`/videos/${videoId}/like`);
export const unlikeVideo = (videoId) => api.delete(`/videos/${videoId}/like`);
export const getVideoComments = (videoId) => api.get(`/videos/${videoId}/comments`);
export const addVideoComment = (videoId, data) => api.post(`/videos/${videoId}/comments`, data);
export const deleteVideoComment = (videoId, commentId) => api.delete(`/videos/${videoId}/comments/${commentId}`);
export const getVideoProgress = (videoId) => api.get(`/videos/${videoId}/progress`);
export const updateVideoProgress = (videoId, seconds) => api.put(`/videos/${videoId}/progress`, { seconds });
export const getVideoAnalytics = (videoId) => api.get(`/videos/${videoId}/analytics`);
export const getRecommendedVideos = (videoId) => api.get(`/videos/${videoId}/recommended`);
export const createPlaylist = (data) => api.post('/videos/playlists', data);
export const getPlaylists = () => api.get('/videos/playlists');
export const addToPlaylist = (playlistId, videoId) => api.post(`/videos/playlists/${playlistId}/add`, { videoId });
