import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createGroup } from '../api/groups';
import '../../../shared/styles/global.css';
import '../styles/groups.css';

export default function CreateGroup() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: 'GENERAL',
    is_private: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ 
      ...prev, 
      [name]: type === 'checkbox' ? checked : value 
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const res = await createGroup(formData);
      alert('Group created successfully!');
      navigate(`/groups/${res.data.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { value: 'GENERAL', label: '📝 General' },
    { value: 'NOTICE', label: '📢 Notice' },
    { value: 'STUDY', label: '📚 Study' },
    { value: 'PROJECT', label: '💻 Project' },
    { value: 'SOCIAL', label: '🎉 Social' }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Create New Group</h1>
        <p>Create a new student group for collaboration</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form className="create-group-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Group Information</h3>
          
          <div className="form-group">
            <label>Group Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Enter group name"
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Describe your group..."
            />
          </div>

          <div className="form-group">
            <label>Category</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
            >
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="is_private"
                checked={formData.is_private}
                onChange={handleChange}
              />
              <span>Private Group (requires approval to join)</span>
            </label>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-success" disabled={loading}>
            {loading ? 'Creating...' : 'Create Group'}
          </button>
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => navigate('/groups')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
