import { useState, useEffect } from 'react';
import { getVideos, deleteVideo } from '../api/videos';
import './styles/videos.css';

const VideosDashboard = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(() => {
    loadVideos();
  }, [selectedCategory]);

  const loadVideos = async () => {
    try {
      setLoading(true);
      const params = selectedCategory !== 'all' ? { category: selectedCategory } : {};
      const response = await getVideos(params);
      setVideos(response.data || []);
    } catch (err) {
      console.error('Failed to load videos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (videoId) => {
    if (window.confirm('Are you sure you want to delete this video?')) {
      try {
        await deleteVideo(videoId);
        loadVideos();
      } catch (err) {
        console.error('Failed to delete video:', err);
      }
    }
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const filteredVideos = videos.filter(video =>
    video.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    video.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const categories = [...new Set(videos.map(v => v.category))];

  if (loading) {
    return <div className="videos-loading">Loading videos...</div>;
  }

  return (
    <div className="videos-dashboard">
      <div className="videos-header">
        <div className="header-content">
          <h1>Educational Videos</h1>
          <p>Watch and learn from video tutorials</p>
        </div>
        <button className="btn-primary">+ Upload Video</button>
      </div>

      <div className="videos-toolbar">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search videos..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="category-filters">
          <button
            className={selectedCategory === 'all' ? 'active' : ''}
            onClick={() => setSelectedCategory('all')}
          >
            All
          </button>
          {categories.map(category => (
            <button
              key={category}
              className={selectedCategory === category ? 'active' : ''}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      <div className="videos-content">
        {selectedVideo ? (
          <div className="video-player-container">
            <button className="back-btn" onClick={() => setSelectedVideo(null)}>
              ← Back to Videos
            </button>
            <div className="video-player">
              <video 
                controls 
                src={selectedVideo.url}
                poster={selectedVideo.thumbnail}
              >
                Your browser does not support video playback.
              </video>
            </div>
            <div className="video-details">
              <h2>{selectedVideo.title}</h2>
              <div className="video-meta">
                <span>👁️ {selectedVideo.views} views</span>
                <span>📅 {formatDate(selectedVideo.uploaded_at)}</span>
                <span>⏱️ {formatDuration(selectedVideo.duration)}</span>
              </div>
              <p className="description">{selectedVideo.description}</p>
              <div className="video-tags">
                {selectedVideo.tags?.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="videos-grid">
            {filteredVideos.length === 0 ? (
              <div className="empty-state">
                <span className="empty-icon">🎬</span>
                <h3>No Videos Found</h3>
                <p>No videos available for the selected criteria</p>
              </div>
            ) : (
              filteredVideos.map(video => (
                <div 
                  key={video.id} 
                  className="video-card"
                  onClick={() => setSelectedVideo(video)}
                >
                  <div className="thumbnail">
                    <img 
                      src={video.thumbnail || '/images/video-placeholder.jpg'} 
                      alt={video.title}
                      onError={(e) => {
                        e.target.src = 'https://via.placeholder.com/320x180?text=Video';
                      }}
                    />
                    <span className="duration">{formatDuration(video.duration)}</span>
                    <div className="play-overlay">▶</div>
                  </div>
                  <div className="video-info">
                    <h4>{video.title}</h4>
                    <p className="category">{video.category}</p>
                    <div className="video-stats">
                      <span>👁️ {video.views}</span>
                      <span>📅 {formatDate(video.uploaded_at)}</span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideosDashboard;
