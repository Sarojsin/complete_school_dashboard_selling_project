import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getFeatureDetail, updateFeature } from '../api/superadmin';
import './AdminPages.css';

const FeatureDetail = () => {
  const { featureName } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [feature, setFeature] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadFeature();
  }, [featureName]);

  const loadFeature = async () => {
    try {
      const response = await getFeatureDetail(featureName);
      setFeature(response.data);
    } catch (err) {
      console.error('Failed to load feature:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async () => {
    setSaving(true);
    try {
      await updateFeature(featureName, { enabled: !feature.enabled });
      setFeature({...feature, enabled: !feature.enabled});
    } catch (err) {
      console.error('Failed to update feature:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading feature details...</div>;
  }

  if (!feature) {
    return <div className="admin-loading">Feature not found</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1>{feature.display_name || feature.name}</h1>
      </div>

      <div className="content-card">
        <div className="feature-header">
          <div className="feature-info">
            <h3>{feature.display_name}</h3>
            <p>{feature.description}</p>
          </div>
          <label className="toggle-switch large">
            <input 
              type="checkbox" 
              checked={feature.enabled}
              onChange={handleToggle}
              disabled={saving}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Feature Settings</h3>
        <div className="settings-list">
          <div className="setting-row">
            <div className="setting-info">
              <h4>Module Name</h4>
              <p>Internal identifier for this feature</p>
            </div>
            <span className="setting-value">{feature.name}</span>
          </div>

          <div className="setting-row">
            <div className="setting-info">
              <h4>Category</h4>
              <p>Feature category</p>
            </div>
            <span className="setting-value">{feature.category}</span>
          </div>

          <div className="setting-row">
            <div className="setting-info">
              <h4>Version</h4>
              <p>Current feature version</p>
            </div>
            <span className="setting-value">{feature.version || '1.0.0'}</span>
          </div>

          <div className="setting-row">
            <div className="setting-info">
              <h4>Required Role</h4>
              <p>Minimum role required to access</p>
            </div>
            <span className="setting-value">{feature.required_role || 'admin'}</span>
          </div>

          <div className="setting-row">
            <div className="setting-info">
              <h4>Created Date</h4>
              <p>When this feature was added</p>
            </div>
            <span className="setting-value">{feature.created_at || 'N/A'}</span>
          </div>

          <div className="setting-row">
            <div className="setting-info">
              <h4>Last Updated</h4>
              <p>Last modification date</p>
            </div>
            <span className="setting-value">{feature.updated_at || 'N/A'}</span>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Feature Configuration</h3>
        {feature.config && Object.keys(feature.config).length > 0 ? (
          <div className="config-form">
            {Object.entries(feature.config).map(([key, value]) => (
              <div key={key} className="config-item">
                <label>{key}</label>
                {typeof value === 'boolean' ? (
                  <label className="toggle-switch">
                    <input type="checkbox" checked={value} />
                    <span className="toggle-slider"></span>
                  </label>
                ) : (
                  <input 
                    type={typeof value === 'number' ? 'number' : 'text'} 
                    value={value} 
                  />
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-text">No configuration options available</p>
        )}
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Usage Statistics</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-value">{feature.usage_count || 0}</span>
            <span className="stat-label">Active Users</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{feature.total_usage || 0}</span>
            <span className="stat-label">Total Usage</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{feature.uptime || '99.9%'}</span>
            <span className="stat-label">Uptime</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeatureDetail;
