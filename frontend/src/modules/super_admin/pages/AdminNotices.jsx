import { useState, useEffect } from 'react';
import { getAdminNotices, createAdminNotice, deleteAdminNotice } from '../api/superadmin';
import './AdminPages.css';

const AdminNotices = () => {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    priority: 'normal',
    target: 'all',
    schools: []
  });

  useEffect(() => {
    loadNotices();
  }, []);

  const loadNotices = async () => {
    try {
      const response = await getAdminNotices();
      setNotices(response.data);
    } catch (err) {
      console.error('Failed to load notices:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createAdminNotice(formData);
      setShowForm(false);
      setFormData({
        title: '',
        content: '',
        priority: 'normal',
        target: 'all',
        schools: []
      });
      loadNotices();
    } catch (err) {
      console.error('Failed to create notice:', err);
    }
  };

  const handleDelete = async (noticeId) => {
    if (window.confirm('Are you sure you want to delete this notice?')) {
      try {
        await deleteAdminNotice(noticeId);
        loadNotices();
      } catch (err) {
        console.error('Failed to delete notice:', err);
      }
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading notices...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <div>
          <h1>System Notices</h1>
          <p>Manage global notices across all schools</p>
        </div>
        <button className="btn-add" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Create Notice'}
        </button>
      </div>

      {showForm && (
        <div className="content-card">
          <h3>Create New Notice</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label>Content</label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({...formData, content: e.target.value})}
                rows={5}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Priority</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: e.target.value})}
                >
                  <option value="low">Low</option>
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              <div className="form-group">
                <label>Target</label>
                <select
                  value={formData.target}
                  onChange={(e) => setFormData({...formData, target: e.target.value})}
                >
                  <option value="all">All Schools</option>
                  <option value="admins">School Admins Only</option>
                  <option value="teachers">Teachers</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn-submit">Create Notice</button>
          </form>
        </div>
      )}

      <div className="content-card">
        <h3>All Notices</h3>
        {notices.length > 0 ? (
          <div className="notices-list">
            {notices.map((notice) => (
              <div key={notice.id} className="notice-item">
                <div className="notice-content">
                  <div className="notice-header">
                    <span className={`priority-badge ${notice.priority}`}>
                      {notice.priority}
                    </span>
                    <span className="notice-date">{notice.created_at}</span>
                  </div>
                  <h4>{notice.title}</h4>
                  <p>{notice.content}</p>
                  <span className="notice-target">Target: {notice.target}</span>
                </div>
                <button 
                  className="delete-btn"
                  onClick={() => handleDelete(notice.id)}
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-text">No notices found</p>
        )}
      </div>
    </div>
  );
};

export default AdminNotices;
