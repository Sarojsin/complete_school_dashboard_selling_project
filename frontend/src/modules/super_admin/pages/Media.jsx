import { useState, useEffect } from 'react';
import { getMediaFiles, uploadMedia, deleteMedia } from '../api/superadmin';
import './AdminPages.css';

const Media = () => {
  const [mediaFiles, setMediaFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadMediaFiles();
  }, []);

  const loadMediaFiles = async () => {
    try {
      const response = await getMediaFiles();
      setMediaFiles(response.data);
    } catch (err) {
      console.error('Failed to load media:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await uploadMedia(formData);
      loadMediaFiles();
    } catch (err) {
      console.error('Failed to upload:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (mediaId) => {
    if (window.confirm('Are you sure you want to delete this file?')) {
      try {
        await deleteMedia(mediaId);
        loadMediaFiles();
      } catch (err) {
        console.error('Failed to delete:', err);
      }
    }
  };

  const filteredFiles = filter === 'all' 
    ? mediaFiles 
    : mediaFiles.filter(f => f.type === filter);

  const getFileIcon = (type) => {
    const icons = {
      image: '🖼️',
      video: '🎬',
      document: '📄',
      audio: '🎵'
    };
    return icons[type] || '📁';
  };

  if (loading) {
    return <div className="admin-loading">Loading media files...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Media Management</h1>
        <p>Manage images, videos, and documents</p>
      </div>

      <div className="content-card">
        <div className="media-header">
          <div className="filter-tabs">
            <button 
              className={`filter-tab ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All ({mediaFiles.length})
            </button>
            <button 
              className={`filter-tab ${filter === 'image' ? 'active' : ''}`}
              onClick={() => setFilter('image')}
            >
              Images
            </button>
            <button 
              className={`filter-tab ${filter === 'video' ? 'active' : ''}`}
              onClick={() => setFilter('video')}
            >
              Videos
            </button>
            <button 
              className={`filter-tab ${filter === 'document' ? 'active' : ''}`}
              onClick={() => setFilter('document')}
            >
              Documents
            </button>
          </div>
          <label className="upload-btn">
            {uploading ? 'Uploading...' : '+ Upload File'}
            <input 
              type="file" 
              hidden 
              accept="image/*,video/*,.pdf,.doc,.docx"
              onChange={handleUpload}
              disabled={uploading}
            />
          </label>
        </div>

        {filteredFiles.length > 0 ? (
          <div className="media-grid">
            {filteredFiles.map((file) => (
              <div key={file.id} className="media-item">
                {file.type === 'image' ? (
                  <img src={file.url} alt={file.name} />
                ) : (
                  <div className="file-icon">
                    <span>{getFileIcon(file.type)}</span>
                  </div>
                )}
                <div className="overlay">
                  <span className="file-name">{file.name}</span>
                  <button 
                    className="delete-btn"
                    onClick={() => handleDelete(file.id)}
                  >
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📁</span>
            <p>No media files found</p>
          </div>
        )}
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Storage Statistics</h3>
        <div className="storage-stats">
          <div className="storage-stat">
            <span className="stat-value">{mediaFiles.length}</span>
            <span className="stat-label">Total Files</span>
          </div>
          <div className="storage-stat">
            <span className="stat-value">
              {Math.round(mediaFiles.reduce((sum, f) => sum + (f.size || 0), 0) / 1024 / 1024)} MB
            </span>
            <span className="stat-label">Total Size</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Media;
