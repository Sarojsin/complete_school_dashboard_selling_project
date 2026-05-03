import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const GroupPosts = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newPost, setNewPost] = useState('');
  const [posting, setPosting] = useState(false);

  useEffect(() => {
    loadGroup();
    loadPosts();
  }, [groupId]);

  const loadGroup = async () => {
    try {
      const response = await fetch(`/api/groups/${groupId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setGroup(data);
    } catch (err) {
      setError('Failed to load group');
    }
  };

  const loadPosts = async () => {
    try {
      const response = await fetch(`/api/groups/${groupId}/posts`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setPosts(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load posts');
      setLoading(false);
    }
  };

  const handleSubmitPost = async (e) => {
    e.preventDefault();
    if (!newPost.trim()) return;

    setPosting(true);
    try {
      const response = await fetch(`/api/groups/${groupId}/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ content: newPost })
      });

      if (response.ok) {
        setNewPost('');
        loadPosts();
      } else {
        setError('Failed to create post');
      }
    } catch (err) {
      setError('An error occurred');
    } finally {
      setPosting(false);
    }
  };

  const handleDeletePost = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this post?')) return;

    try {
      const response = await fetch(`/api/groups/posts/${postId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      if (response.ok) {
        setPosts(posts.filter(p => p.id !== postId));
      } else {
        setError('Failed to delete post');
      }
    } catch (err) {
      setError('An error occurred');
    }
  };

  const handleLike = async (postId) => {
    try {
      const response = await fetch(`/api/groups/posts/${postId}/like`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      if (response.ok) {
        loadPosts();
      }
    } catch (err) {
      console.error('Failed to like post');
    }
  };

  if (loading) {
    return <div className="loading">Loading posts...</div>;
  }

  return (
    <div className="group-posts-container">
      <div className="page-header">
        <h1>{group?.name} - Posts</h1>
        <button onClick={() => navigate(`/groups/${groupId}`)} className="back-btn">
          ← Back to Group
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="new-post-section">
        <form onSubmit={handleSubmitPost} className="post-form">
          <textarea
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
            placeholder="Write something..."
            rows="4"
          />
          <button type="submit" className="btn-primary" disabled={posting || !newPost.trim()}>
            {posting ? 'Posting...' : 'Post'}
          </button>
        </form>
      </div>

      <div className="posts-list">
        {posts.length === 0 ? (
          <div className="no-posts">
            <p>No posts yet. Be the first to post!</p>
          </div>
        ) : (
          posts.map(post => (
            <div key={post.id} className="post-card">
              <div className="post-header">
                <div className="post-author">
                  <img 
                    src={post.author_avatar || '/default-avatar.png'} 
                    alt={post.author_name}
                    className="author-avatar"
                  />
                  <div className="author-info">
                    <span className="author-name">{post.author_name}</span>
                    <span className="post-date">{new Date(post.created_at).toLocaleString()}</span>
                  </div>
                </div>
                {post.is_owner && (
                  <button 
                    onClick={() => handleDeletePost(post.id)}
                    className="btn-delete"
                  >
                    Delete
                  </button>
                )}
              </div>
              
              <div className="post-content">
                <p>{post.content}</p>
              </div>

              {post.attachment_url && (
                <div className="post-attachment">
                  <a href={post.attachment_url} target="_blank" rel="noopener noreferrer">
                    View Attachment
                  </a>
                </div>
              )}

              <div className="post-actions">
                <button onClick={() => handleLike(post.id)} className="btn-like">
                  ♥ {post.likes_count || 0} Likes
                </button>
                <button 
                  onClick={() => navigate(`/groups/${groupId}/posts/${post.id}`)}
                  className="btn-comment"
                >
                  💬 {post.comments_count || 0} Comments
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default GroupPosts;
