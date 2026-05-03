import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createNotice } from '../../api/authority';
import './AddEdit.css';

const AddNotice = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    priority: 'normal',
    target_audience: 'all',
    publish_date: '',
    expiry_date: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createNotice(formData);
      navigate('/authority/notices');
    } catch (err) {
      console.error('Failed to create notice:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-edit-page">
      <div className="page-header">
        <h1>Create New Notice</h1>
      </div>

      <form onSubmit={handleSubmit} className="add-form">
        <div className="form-section">
          <h2>Notice Details</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Title *</label>
              <input type="text" name="title" value={formData.title} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Priority</label>
              <select name="priority" value={formData.priority} onChange={handleChange}>
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div className="form-group">
              <label>Target Audience</label>
              <select name="target_audience" value={formData.target_audience} onChange={handleChange}>
                <option value="all">All</option>
                <option value="students">Students</option>
                <option value="teachers">Teachers</option>
                <option value="parents">Parents</option>
                <option value="staff">Staff</option>
              </select>
            </div>
            <div className="form-group">
              <label>Publish Date</label>
              <input type="date" name="publish_date" value={formData.publish_date} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Expiry Date</label>
              <input type="date" name="expiry_date" value={formData.expiry_date} onChange={handleChange} />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Content</h2>
          <div className="form-group">
            <textarea 
              name="content" 
              value={formData.content} 
              onChange={handleChange} 
              rows="8"
              placeholder="Write your notice content here..."
              required
            ></textarea>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={() => navigate('/authority/notices')}>Cancel</button>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Publishing...' : 'Publish Notice'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddNotice;
