import { useState, useEffect } from 'react';
import api from '../../../shared/api/client';
import './Forum.css';

const Forum = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newPost, setNewPost] = useState({ title: '', content: '' });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      const response = await api.get('/student/forum/posts');
      setPosts(response.data || []);
    } catch (err) {
      console.error('Failed to load posts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/student/forum/posts', newPost);
      setNewPost({ title: '', content: '' });
      setShowForm(false);
      loadPosts();
    } catch (err) {
      console.error('Failed to create post:', err);
    }
  };

  const handleLike = async (postId) => {
    try {
      await api.post(`/student/forum/posts/${postId}/like`);
      loadPosts();
    } catch (err) {
      console.error('Failed to like post:', err);
    }
  };

  const getAvatarUrl = (avatar) => {
    if (!avatar) return '/images/default-avatar.png';
    return avatar.startsWith('http') ? avatar : `/uploads/avatars/${avatar}`;
  };

  const formatDate = (date) => {
    const d = new Date(date);
    const now = new Date();
    const diff = now - d;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return d.toLocaleDateString();
  };

  if (loading) {
    return <div className="forum-loading">Loading forum...</div>;
  }

  return (
    <div className="forum-page">
      <div className="page-header">
        <div>
          <h1>Student Forum</h1>
          <p>Discuss topics with your classmates</p>
        </div>
        <button 
          className="new-post-btn"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ New Post'}
        </button>
      </div>

      {showForm && (
        <div className="new-post-form">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Post Title"
              value={newPost.title}
              onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
              required
            />
            <textarea
              placeholder="What's on your mind?"
              value={newPost.content}
              onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
              rows="4"
              required
            />
            <button type="submit" className="submit-btn">Post</button>
          </form>
        </div>
      )}

      <div className="posts-list">
        {posts.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">💬</span>
            <h3>No Posts Yet</h3>
            <p>Be the first to start a discussion!</p>
          </div>
        ) : (
          posts.map((post, index) => (
            <div key={index} className="post-card">
              <div className="post-header">
                <img 
                  src={getAvatarUrl(post.author_avatar)} 
                  alt={post.author_name}
                  className="author-avatar"
                  onError={(e) => {
                    e.target.src = '/images/default-avatar.png';
                  }}
                />
                <div className="author-info">
                  <span className="author-name">{post.author_name}</span>
                  <span className="post-time">{formatDate(post.created_at)}</span>
                </div>
              </div>
              <div className="post-content">
                <h3>{post.title}</h3>
                <p>{post.content}</p>
              </div>
              <div className="post-actions">
                <button 
                  className={`like-btn ${post.liked ? 'liked' : ''}`}
                  onClick={() => handleLike(post.id)}
                >
                  {post.liked ? '❤️' : '🤍'} {post.likes || 0}
                </button>
                <button className="comment-btn">
                  💬 {post.comments || 0} Comments
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Forum;
