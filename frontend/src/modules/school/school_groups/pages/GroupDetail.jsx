import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getGroupById, getGroupPosts, createGroupPost, getGroupMembers, leaveGroup, deleteGroup } from '../api/groups';
import '../../../shared/styles/global.css';
import '../styles/groups.css';

export default function GroupDetail() {
  const { groupId } = useParams();
  const [group, setGroup] = useState(null);
  const [posts, setPosts] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newPost, setNewPost] = useState({ title: '', content: '', post_type: 'NOTE' });
  const [posting, setPosting] = useState(false);
  const [activeTab, setActiveTab] = useState('posts');

  useEffect(() => {
    fetchGroupData();
  }, [groupId]);

  const fetchGroupData = async () => {
    try {
      setLoading(true);
      const [groupRes, postsRes, membersRes] = await Promise.all([
        getGroupById(groupId),
        getGroupPosts(groupId),
        getGroupMembers(groupId)
      ]);
      setGroup(groupRes.data);
      setPosts(postsRes.data || []);
      setMembers(membersRes.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    try {
      setPosting(true);
      await createGroupPost(groupId, newPost);
      setNewPost({ title: '', content: '', post_type: 'NOTE' });
      fetchGroupData();
      alert('Post created successfully!');
    } catch (err) {
      alert('Failed to create post: ' + err.message);
    } finally {
      setPosting(false);
    }
  };

  const handleLeave = async () => {
    if (!window.confirm('Are you sure you want to leave this group?')) return;
    try {
      await leaveGroup(groupId);
      alert('Left group successfully!');
      window.location.href = '/groups';
    } catch (err) {
      alert('Failed to leave group: ' + err.message);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this group?')) return;
    try {
      await deleteGroup(groupId);
      alert('Group deleted successfully!');
      window.location.href = '/groups';
    } catch (err) {
      alert('Failed to delete group: ' + err.message);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString();
  };

  const getPostTypeColor = (type) => {
    const colors = {
      NOTICE: '#dc3545',
      NOTE: '#28a745',
      LINK: '#007bff'
    };
    return colors[type] || '#6c757d';
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="group-detail-header">
        <Link to="/groups" className="back-link">← Back to Groups</Link>
        <h1>{group?.name}</h1>
        <p>{group?.description}</p>
        <div className="group-meta">
          <span>Code: <code>{group?.code}</code></span>
          <span>Category: <span className="category-badge">{group?.category}</span></span>
          <span>Members: {members.length}</span>
        </div>
        <div className="group-actions">
          <button className="btn btn-warning" onClick={handleLeave}>Leave Group</button>
          {group?.is_admin && (
            <button className="btn btn-danger" onClick={handleDelete}>Delete Group</button>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'posts' ? 'active' : ''}`}
          onClick={() => setActiveTab('posts')}
        >
          Posts
        </button>
        <button 
          className={`tab ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          Members ({members.length})
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {activeTab === 'posts' && (
        <div className="posts-section">
          {/* Create Post Form */}
          <div className="create-post-form">
            <h3>Create New Post</h3>
            <form onSubmit={handleCreatePost}>
              <input
                type="text"
                placeholder="Post title..."
                value={newPost.title}
                onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
                required
              />
              <textarea
                placeholder="Write your post content..."
                value={newPost.content}
                onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
                required
                rows="4"
              />
              <select
                value={newPost.post_type}
                onChange={(e) => setNewPost({ ...newPost, post_type: e.target.value })}
              >
                <option value="NOTE">📝 Note</option>
                <option value="NOTICE">📢 Notice</option>
                <option value="LINK">🔗 Link</option>
              </select>
              <button type="submit" className="btn btn-success" disabled={posting}>
                {posting ? 'Posting...' : 'Post'}
              </button>
            </form>
          </div>

          {/* Posts List */}
          <div className="posts-list">
            <h3>Recent Posts</h3>
            {posts.length > 0 ? (
              posts.map((post) => (
                <div key={post.id} className="post-card">
                  <div className="post-header">
                    <span 
                      className="post-type-badge"
                      style={{ backgroundColor: getPostTypeColor(post.post_type) }}
                    >
                      {post.post_type}
                    </span>
                    <span className="post-author">{post.author_name}</span>
                    <span className="post-date">{formatDate(post.created_at)}</span>
                  </div>
                  <h4>{post.title}</h4>
                  <p className="post-content">{post.content}</p>
                  {post.attachment_url && (
                    <a href={post.attachment_url} className="post-attachment" target="_blank">
                      📎 View Attachment
                    </a>
                  )}
                </div>
              ))
            ) : (
              <div className="no-data">No posts yet. Be the first to post!</div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'members' && (
        <div className="members-section">
          <h3>Group Members</h3>
          <div className="members-grid">
            {members.map((member) => (
              <div key={member.id} className="member-card">
                <div className="member-avatar">
                  {member.name?.charAt(0) || 'M'}
                </div>
                <div className="member-info">
                  <h4>{member.name}</h4>
                  <p>{member.email}</p>
                  <span className="member-role">{member.role}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
