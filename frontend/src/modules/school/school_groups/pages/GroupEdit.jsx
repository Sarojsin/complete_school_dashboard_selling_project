import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getGroupById, updateGroup } from '../api/groups';
import '../styles/groups.css';

const GroupEdit = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    group_type: 'class',
    is_private: false
  });

  useEffect(() => { loadGroup(); }, [groupId]);

  const loadGroup = async () => {
    try {
      const response = await getGroupById(groupId);
      setFormData(response.data || response);
    } catch (err) { console.error('Failed:', err); }
    finally { setLoading(false); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateGroup(groupId, formData);
      navigate(`/groups/${groupId}`);
    } catch (err) { console.error('Failed:', err); }
    finally { setSaving(false); }
  };

  if (loading) return <div className="groups-loading">Loading...</div>;

  return (
    <div className="groups-page">
      <button className="back-btn" onClick={() => navigate(-1)}>← Back</button>
      <h1>Edit Group</h1>
      
      <div className="groups-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Group Name</label>
            <input 
              type="text" 
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Description</label>
            <textarea 
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows={4}
            />
          </div>

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
            </select>
          </div>

          <div className="form-group">
            <label>
              <input 
                type="checkbox"
                checked={formData.is_private}
                onChange={(e) => setFormData({...formData, is_private: e.target.checked})}
              />
              Private Group
            </label>
          </div>

          <div className="form-actions">
            <button type="button" className="groups-btn secondary" onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button type="submit" className="groups-btn primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default GroupEdit;
