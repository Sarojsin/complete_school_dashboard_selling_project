import { useState, useEffect } from 'react';
import { getNotices, createNotice, deleteNotice } from '../api/examSection';
import './ExamSection.css';

const ExamNotices = () => {
  const [loading, setLoading] = useState(true);
  const [notices, setNotices] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ title: '', content: '', priority: 'normal' });

  useEffect(() => { loadNotices(); }, []);

  const loadNotices = async () => {
    try {
      const response = await getNotices();
      setNotices(response.data || response);
    } catch (err) { console.error('Failed:', err); }
    finally { setLoading(false); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createNotice(formData);
      setShowForm(false);
      setFormData({ title: '', content: '', priority: 'normal' });
      loadNotices();
    } catch (err) { console.error('Failed:', err); }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete notice?')) {
      try { await deleteNotice(id); loadNotices(); }
      catch (err) { console.error('Failed:', err); }
    }
  };

  if (loading) return <div className="exam-loading">Loading...</div>;

  return (
    <div className="exam-page">
      <div className="page-header">
        <div>
          <h1>Exam Notices</h1>
          <p>Manage exam-related announcements</p>
        </div>
        <button className="exam-btn primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Notice'}
        </button>
      </div>

      {showForm && (
        <div className="exam-card">
          <h3>Create Notice</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Title</label>
              <input type="text" value={formData.title} onChange={(e) => setFormData({...formData, title: e.target.value})} required />
            </div>
            <div className="form-group">
              <label>Priority</label>
              <select value={formData.priority} onChange={(e) => setFormData({...formData, priority: e.target.value})}>
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="form-group">
              <label>Content</label>
              <textarea value={formData.content} onChange={(e) => setFormData({...formData, content: e.target.value})} rows={4} required />
            </div>
            <button type="submit" className="exam-btn success">Publish</button>
          </form>
        </div>
      )}

      <div className="exam-card">
        {notices.length > 0 ? notices.map((n) => (
          <div key={n.id} className="notice-item">
            <h4>{n.title}</h4>
            <p>{n.content}</p>
            <span>{n.created_at}</span>
            <button className="exam-btn danger" onClick={() => handleDelete(n.id)}>Delete</button>
          </div>
        )) : (
          <div className="empty-state">
            <span className="empty-icon">📋</span>
            <p>No notices</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExamNotices;
