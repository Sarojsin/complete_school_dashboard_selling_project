import { useEffect, useState } from 'react';
import { getSettings, updateSetting } from '../api/superadmin';
import '@shared/styles/global.css';
import '../styles/superadmin.css';

export default function Settings() {
  const [settings, setSettings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingKey, setEditingKey] = useState(null);
  const [editValue, setEditValue] = useState('');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const res = await getSettings();
      setSettings(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (setting) => {
    setEditingKey(setting.key);
    setEditValue(setting.value);
  };

  const handleSave = async () => {
    try {
      await updateSetting(editingKey, editValue);
      setSettings(settings.map(s => 
        s.key === editingKey ? { ...s, value: editValue } : s
      ));
      setEditingKey(null);
      alert('Setting updated successfully!');
    } catch (err) {
      alert('Failed to update setting: ' + err.message);
    }
  };

  const handleCancel = () => {
    setEditingKey(null);
    setEditValue('');
  };

  const getInputType = (setting) => {
    if (setting.type === 'boolean') return 'checkbox';
    if (setting.type === 'number') return 'number';
    return 'text';
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
      <div className="page-header">
        <h1>System Settings</h1>
        <p>Configure system settings</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="settings-container">
        <div className="settings-grid">
          {settings.map((setting) => (
            <div key={setting.key} className="setting-card">
              <div className="setting-header">
                <h3>{setting.key.replace(/_/g, ' ').toUpperCase()}</h3>
                {setting.description && (
                  <p className="setting-description">{setting.description}</p>
                )}
              </div>
              
              <div className="setting-value">
                {editingKey === setting.key ? (
                  <div className="edit-form">
                    {setting.type === 'boolean' ? (
                      <input
                        type="checkbox"
                        checked={editValue === 'true' || editValue === true}
                        onChange={(e) => setEditValue(e.target.checked ? 'true' : 'false')}
                      />
                    ) : (
                      <input
                        type={getInputType(setting)}
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                      />
                    )}
                    <div className="edit-actions">
                      <button className="btn btn-sm btn-success" onClick={handleSave}>
                        Save
                      </button>
                      <button className="btn btn-sm btn-secondary" onClick={handleCancel}>
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="value-display">
                    <span className="current-value">
                      {setting.type === 'boolean' 
                        ? (setting.value === 'true' ? '✓ Enabled' : '✗ Disabled')
                        : setting.value
                      }
                    </span>
                    <button 
                      className="btn btn-sm btn-primary"
                      onClick={() => handleEdit(setting)}
                    >
                      Edit
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {settings.length === 0 && (
        <div className="no-data">
          <p>No settings found.</p>
        </div>
      )}
    </div>
  );
}
