import { useState, useEffect } from 'react';
import { getTeacherNotices, createTeacherNotice, deleteTeacherNotice } from '../api/teachers';
import './TeacherPortal.css';

const TeacherNotices = () => {
  const [loading, setLoading] = useState(true);
  const [notices, setNotices] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    priority: 'normal',
    target_audience: 'students'
  });

  useEffect(() => {
    loadNotices();
  }, []);

  const loadNotices = async () => {
    try {
      const response = await getTeacherNotices();
      setNotices(response.data || response);
    } catch (err) {
      console.error('Failed to load notices:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createTeacherNotice(formData);
      setShowForm(false);
      setFormData({ title: '', content: '', priority: 'normal', target_audience: 'students' });
      loadNotices();
    } catch (err) {
      console.error('Failed to create notice:', err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this notice?')) {
      try {
        await deleteTeacherNotice(id);
        loadNotices();
      } catch (err) {
        console.error('Failed to delete:', err);
      }
    }
  };

  if (loading) {
    return <div className="teacher-loading">Loading notices...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <div>
          <h1>Notices</h1>
          <p>Manage notices for your classes</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Notice'}
        </button>
      </div>

      {showForm && (
        <div className="teacher-card">
          <h3>Create Notice</h3>
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
                </select>
              </div>
              <div className="form-group">
                <label>Target Audience</label>
                <select
                  value={formData.target_audience}
                  onChange={(e) => setFormData({...formData, target_audience: e.target.value})}
                >
                  <option value="students">Students</option>
                  <option value="parents">Parents</option>
                  <option value="all">All</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Content</label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({...formData, content: e.target.value})}
                rows={4}
                required
              />
            </div>
            <button type="submit" className="btn-success">Publish Notice</button>
          </form>
        </div>
      )}

      <div className="teacher-card">
        <h3>My Notices</h3>
        {notices.length > 0 ? (
          <div className="notices-list">
            {notices.map((notice) => (
              <div key={notice.id} className="list-item">
                <div className="list-item-info">
                  <h4>{notice.title}</h4>
                  <p>{notice.content}</p>
                  <span className="notice-meta">
                    {notice.target_audience} • {notice.created_at}
                  </span>
                </div>
                <div className="action-btns">
                  <button className="action-btn danger" onClick={() => handleDelete(notice.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📋</span>
            <p>No notices published</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherNotices;
