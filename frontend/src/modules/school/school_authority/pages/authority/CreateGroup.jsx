import { useState } from 'react';
import { createGroup } from '../../api/authority';
import './AuthorityGroups.css';

const AuthorityCreateGroup = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    group_type: 'class',
    is_private: false,
    members: []
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createGroup(formData);
      setSuccess(true);
      setFormData({
        name: '',
        description: '',
        group_type: 'class',
        is_private: false,
        members: []
      });
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to create group:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="authority-groups-page">
      <div className="page-header">
        <h1>Create Group</h1>
        <p>Create new student/teacher groups</p>
      </div>

      <div className="create-group-card">
        {success && (
          <div className="success-message">
            Group created successfully!
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Group Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="Enter group name"
              required
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Describe the purpose of this group"
              rows={4}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Group Type</label>
              <select
                value={formData.group_type}
                onChange={(e) => setFormData({...formData, group_type: e.target.value})}
              >
                <option value="class">Class Group</option>
                <option value="department">Department</option>
                <option value="club">Club</option>
                <option value="committee">Committee</option>
                <option value="event">Event</option>
              </select>
            </div>

            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={formData.is_private}
                  onChange={(e) => setFormData({...formData, is_private: e.target.checked})}
                />
                <span>Private Group</span>
              </label>
              <p className="help-text">Private groups require approval for members to join</p>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? 'Creating...' : 'Create Group'}
            </button>
          </div>
        </form>
      </div>

      <div className="group-templates">
        <h3>Quick Start Templates</h3>
        <div className="templates-grid">
          <button 
            className="template-card"
            onClick={() => setFormData({...formData, name: 'Grade 10-A', description: 'Class group for Grade 10-A students', group_type: 'class'})}
          >
            <span className="template-icon">👨‍🎓</span>
            <span>Class Group</span>
          </button>
          <button 
            className="template-card"
            onClick={() => setFormData({...formData, name: 'Science Department', description: 'Department group for Science faculty', group_type: 'department'})}
          >
            <span className="template-icon">🔬</span>
            <span>Department</span>
          </button>
          <button 
            className="template-card"
            onClick={() => setFormData({...formData, name: 'Sports Club', description: 'School sports and athletics club', group_type: 'club'})}
          >
            <span className="template-icon">⚽</span>
            <span>Club</span>
          </button>
          <button 
            className="template-card"
            onClick={() => setFormData({...formData, name: 'Event Committee', description: 'Event planning committee', group_type: 'committee'})}
          >
            <span className="template-icon">📅</span>
            <span>Committee</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthorityCreateGroup;
