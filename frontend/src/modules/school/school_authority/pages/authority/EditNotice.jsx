import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getNotices, updateNotice } from '../../api/authority';
import './AddEdit.css';

const AuthorityEditNotice = () => {
  const { noticeId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    priority: 'medium',
    target_audience: 'all',
    publish_date: '',
    expire_date: ''
  });

  useEffect(() => {
    loadNotice();
  }, [noticeId]);

  const loadNotice = async () => {
    try {
      const response = await getNotices();
      const notice = response.data.find(n => n.id === parseInt(noticeId));
      if (notice) {
        setFormData(notice);
      }
    } catch (err) {
      console.error('Failed to load notice:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateNotice(noticeId, formData);
      navigate('/authority/notices');
    } catch (err) {
      console.error('Failed to update notice:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="edit-loading">Loading notice...</div>;
  }

  return (
    <div className="authority-edit-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1>Edit Notice</h1>
      </div>

      <div className="edit-form-card">
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
              rows={8}
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
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="form-group">
              <label>Target Audience</label>
              <select
                value={formData.target_audience}
                onChange={(e) => setFormData({...formData, target_audience: e.target.value})}
              >
                <option value="all">All</option>
                <option value="students">Students</option>
                <option value="teachers">Teachers</option>
                <option value="parents">Parents</option>
                <option value="staff">Staff</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Publish Date</label>
              <input
                type="date"
                value={formData.publish_date}
                onChange={(e) => setFormData({...formData, publish_date: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Expire Date</label>
              <input
                type="date"
                value={formData.expire_date}
                onChange={(e) => setFormData({...formData, expire_date: e.target.value})}
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="btn-cancel" onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button type="submit" className="btn-submit" disabled={saving}>
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AuthorityEditNotice;
