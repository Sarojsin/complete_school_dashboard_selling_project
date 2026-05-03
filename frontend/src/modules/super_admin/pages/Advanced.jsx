import { useState } from 'react';
import './AdminPages.css';

const Advanced = () => {
  const [settings, setSettings] = useState({
    cache_enabled: true,
    cache_ttl: 3600,
    debug_mode: false,
    maintenance_mode: false,
    api_rate_limit: 100,
    max_upload_size: 10,
    session_timeout: 30,
    enable_logging: true,
    log_retention_days: 30,
    enable_caching: true,
    compression_enabled: true,
    cdn_enabled: false
  });

  const handleChange = (key, value) => {
    setSettings({...settings, [key]: value});
  };

  const handleSave = () => {
    console.log('Saving advanced settings:', settings);
    alert('Advanced settings saved!');
  };

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Advanced Settings</h1>
        <p>Configure advanced system settings and optimizations</p>
      </div>

      <div className="content-card">
        <h3>Performance Settings</h3>
        <div className="settings-grid">
          <div className="setting-item">
            <h4>Enable Caching</h4>
            <p>Cache frequently accessed data for better performance</p>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.cache_enabled}
                onChange={(e) => handleChange('cache_enabled', e.target.checked)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <h4>Cache TTL (seconds)</h4>
            <p>Time to live for cached data</p>
            <input 
              type="number" 
              value={settings.cache_ttl}
              onChange={(e) => handleChange('cache_ttl', parseInt(e.target.value))}
            />
          </div>

          <div className="setting-item">
            <h4>Enable Compression</h4>
            <p>Compress responses to reduce bandwidth</p>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.compression_enabled}
                onChange={(e) => handleChange('compression_enabled', e.target.checked)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <h4>Enable CDN</h4>
            <p>Use Content Delivery Network for static files</p>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.cdn_enabled}
                onChange={(e) => handleChange('cdn_enabled', e.target.checked)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>System Settings</h3>
        <div className="settings-grid">
          <div className="setting-item">
            <h4>Debug Mode</h4>
            <p>Enable detailed error messages</p>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.debug_mode}
                onChange={(e) => handleChange('debug_mode', e.target.checked)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <h4>Maintenance Mode</h4>
            <p>Put the system in maintenance mode</p>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.maintenance_mode}
                onChange={(e) => handleChange('maintenance_mode', e.target.checked)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <h4>API Rate Limit</h4>
            <p>Maximum requests per minute</p>
            <input 
              type="number" 
              value={settings.api_rate_limit}
              onChange={(e) => handleChange('api_rate_limit', parseInt(e.target.value))}
            />
          </div>

          <div className="setting-item">
            <h4>Max Upload Size (MB)</h4>
            <p>Maximum file upload size</p>
            <input 
              type="number" 
              value={settings.max_upload_size}
              onChange={(e) => handleChange('max_upload_size', parseInt(e.target.value))}
            />
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Session & Logging</h3>
        <div className="settings-grid">
          <div className="setting-item">
            <h4>Session Timeout (minutes)</h4>
            <p>Auto logout after inactivity</p>
            <input 
              type="number" 
              value={settings.session_timeout}
              onChange={(e) => handleChange('session_timeout', parseInt(e.target.value))}
            />
          </div>

          <div className="setting-item">
            <h4>Enable Logging</h4>
            <p>Log system activities</p>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.enable_logging}
                onChange={(e) => handleChange('enable_logging', e.target.checked)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <h4>Log Retention (days)</h4>
            <p>How long to keep log files</p>
            <input 
              type="number" 
              value={settings.log_retention_days}
              onChange={(e) => handleChange('log_retention_days', parseInt(e.target.value))}
            />
          </div>
        </div>
      </div>

      <button className="btn-submit" style={{marginTop: '20px'}} onClick={handleSave}>
        Save Settings
      </button>
    </div>
  );
};

export default Advanced;
