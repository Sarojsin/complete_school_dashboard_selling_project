import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const ViewPost = () => {
  const { groupId, postId } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [posting, setPosting] = useState(false);

  useEffect(() => {
    loadPost();
    loadComments();
  }, [postId]);

  const loadPost = async () => {
    try {
      const response = await fetch(`/api/groups/posts/${postId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setPost(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load post');
      setLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const response = await fetch(`/api/groups/posts/${postId}/comments`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setComments(data);
    } catch (err) {
      console.error('Failed to load comments');
    }
  };

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setPosting(true);
    try {
      const response = await fetch(`/api/groups/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ content: newComment })
      });

      if (response.ok) {
        setNewComment('');
        loadComments();
      } else {
        setError('Failed to post comment');
      }
    } catch (err) {
      setError('An error occurred');
    } finally {
      setPosting(false);
    }
  };

  const handleLike = async () => {
    try {
      const response = await fetch(`/api/groups/posts/${postId}/like`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      if (response.ok) {
        loadPost();
      }
    } catch (err) {
      console.error('Failed to like post');
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm('Delete this comment?')) return;

    try {
      const response = await fetch(`/api/groups/comments/${commentId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      if (response.ok) {
        setComments(comments.filter(c => c.id !== commentId));
      }
    } catch (err) {
      console.error('Failed to delete comment');
    }
  };

  if (loading) {
    return <div className="loading">Loading post...</div>;
  }

  if (error && !post) {
    return <div className="alert alert-error">{error}</div>;
  }

  return (
    <div className="view-post-container">
      <div className="page-header">
        <button onClick={() => navigate(`/groups/${groupId}/posts`)} className="back-btn">
          ← Back to Posts
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="post-detail">
        <div className="post-header">
          <div className="post-author">
            <img 
              src={post?.author_avatar || '/default-avatar.png'} 
              alt={post?.author_name}
              className="author-avatar"
            />
            <div className="author-info">
              <span className="author-name">{post?.author_name}</span>
              <span className="post-date">{new Date(post?.created_at).toLocaleString()}</span>
            </div>
          </div>
          {post?.is_owner && (
            <button 
              onClick={() => navigate(`/groups/${groupId}/posts/${postId}/edit`)}
              className="btn-edit"
            >
              Edit
            </button>
          )}
        </div>

        <div className="post-content">
          <p>{post?.content}</p>
        </div>

        {post?.attachment_url && (
          <div className="post-attachment">
            <a href={post.attachment_url} target="_blank" rel="noopener noreferrer">
              View Attachment
            </a>
          </div>
        )}

        <div className="post-stats">
          <span>{post?.likes_count || 0} Likes</span>
          <span>{comments.length} Comments</span>
        </div>

        <div className="post-actions">
          <button onClick={handleLike} className="btn-like">
            ♥ Like
          </button>
        </div>
      </div>

      <div className="comments-section">
        <h3>Comments ({comments.length})</h3>

        <form onSubmit={handleSubmitComment} className="comment-form">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
            rows="3"
          />
          <button type="submit" className="btn-primary" disabled={posting || !newComment.trim()}>
            {posting ? 'Posting...' : 'Comment'}
          </button>
        </form>

        <div className="comments-list">
          {comments.length === 0 ? (
            <p className="no-comments">No comments yet.</p>
          ) : (
            comments.map(comment => (
              <div key={comment.id} className="comment-card">
                <div className="comment-header">
                  <div className="comment-author">
                    <img 
                      src={comment.author_avatar || '/default-avatar.png'} 
                      alt={comment.author_name}
                      className="comment-avatar"
                    />
                    <div className="comment-info">
                      <span className="author-name">{comment.author_name}</span>
                      <span className="comment-date">{new Date(comment.created_at).toLocaleString()}</span>
                    </div>
                  </div>
                  {comment.is_owner && (
                    <button 
                      onClick={() => handleDeleteComment(comment.id)}
                      className="btn-delete"
                    >
                      Delete
                    </button>
                  )}
                </div>
                <div className="comment-content">
                  <p>{comment.content}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ViewPost;
