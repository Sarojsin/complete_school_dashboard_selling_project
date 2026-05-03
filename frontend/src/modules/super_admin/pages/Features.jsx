import { useEffect, useState } from 'react';
import { getFeatures, toggleFeature } from '../api/superadmin';
import '@shared/styles/global.css';
import '../styles/superadmin.css';

export default function Features() {
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchFeatures();
  }, []);

  const fetchFeatures = async () => {
    try {
      setLoading(true);
      const res = await getFeatures();
      setFeatures(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (featureName, currentStatus) => {
    try {
      await toggleFeature(featureName);
      setFeatures(features.map(f => 
        f.name === featureName ? { ...f, enabled: !currentStatus } : f
      ));
      alert(`Feature ${!currentStatus ? 'enabled' : 'disabled'} successfully!`);
    } catch (err) {
      alert('Failed to toggle feature: ' + err.message);
    }
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
        <h1>Feature Management</h1>
        <p>Enable or disable system features</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="features-grid">
        {features.map((feature) => (
          <div key={feature.name} className={`feature-card ${feature.enabled ? 'enabled' : 'disabled'}`}>
            <div className="feature-header">
              <h3>{feature.name.replace(/_/g, ' ')}</h3>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={feature.enabled}
                  onChange={() => handleToggle(feature.name, feature.enabled)}
                />
                <span className="slider"></span>
              </label>
            </div>
            
            <div className="feature-status">
              <span className={`status-badge ${feature.enabled ? 'enabled' : 'disabled'}`}>
                {feature.enabled ? '✓ Enabled' : '✗ Disabled'}
              </span>
            </div>
            
            {feature.description && (
              <p className="feature-description">{feature.description}</p>
            )}
            
            {feature.config && (
              <div className="feature-config">
                <h4>Configuration:</h4>
                <pre>{JSON.stringify(feature.config, null, 2)}</pre>
              </div>
            )}
          </div>
        ))}
      </div>

      {features.length === 0 && (
        <div className="no-data">
          <p>No features found.</p>
        </div>
      )}
    </div>
  );
}
