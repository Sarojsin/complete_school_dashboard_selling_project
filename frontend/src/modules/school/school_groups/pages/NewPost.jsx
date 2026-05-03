import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const NewPost = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState(null);
  const [content, setContent] = useState('');
  const [attachment, setAttachment] = useState(null);
  const [posting, setPosting] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGroup();
  }, [groupId]);

  const loadGroup = async () => {
    try {
      const response = await fetch(`/api/groups/${groupId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setGroup(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load group');
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      setAttachment(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) {
      setError('Please write something for your post');
      return;
    }

    setPosting(true);
    setError('');

    const formData = new FormData();
    formData.append('content', content);
    if (attachment) {
      formData.append('attachment', attachment);
    }

    try {
      const response = await fetch(`/api/groups/${groupId}/posts`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (response.ok) {
        navigate(`/groups/${groupId}/posts`);
      } else {
        setError('Failed to create post');
      }
    } catch (err) {
      setError('An error occurred while creating the post');
    } finally {
      setPosting(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="new-post-container">
      <div className="page-header">
        <h1>Create New Post</h1>
        <h2 className="group-name">in {group?.name}</h2>
        <button onClick={() => navigate(`/groups/${groupId}/posts`)} className="back-btn">
          ← Back to Posts
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <form onSubmit={handleSubmit} className="new-post-form">
        <div className="form-group">
          <label>What's on your mind?</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Share something with the group..."
            rows="8"
            required
          />
        </div>

        <div className="form-group">
          <label>Attachment (Optional)</label>
          <div className="file-upload">
            <input
              type="file"
              id="attachment"
              onChange={handleFileChange}
              accept="image/*,.pdf,.doc,.docx,.txt"
            />
            {attachment && (
              <div className="selected-file">
                <span>Selected: {attachment.name}</span>
                <button type="button" onClick={() => setAttachment(null)} className="btn-remove">
                  ×
                </button>
              </div>
            )}
          </div>
          <small>Max file size: 10MB. Supported: Images, PDF, DOC, TXT</small>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={posting}>
            {posting ? 'Posting...' : 'Post'}
          </button>
          <button 
            type="button" 
            className="btn-secondary"
            onClick={() => navigate(`/groups/${groupId}/posts`)}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewPost;
