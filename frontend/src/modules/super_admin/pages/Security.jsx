import { useState, useEffect } from 'react';
import { getSecuritySettings, updateSecuritySettings } from '../api/superadmin';
import './AdminPages.css';

const Security = () => {
  const [loading, setLoading] = useState(true);
  const [settings, setSettings] = useState({
    password_min_length: 8,
    password_require_uppercase: true,
    password_require_lowercase: true,
    password_require_numbers: true,
    password_require_special: false,
    session_timeout: 30,
    max_login_attempts: 5,
    lockout_duration: 15,
    enable_2fa: false,
    require_email_verification: true,
    ip_whitelist_enabled: false,
    ip_whitelist: '',
    enable_captcha: true,
    audit_logging: true,
    data_encryption: true
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await getSecuritySettings();
      setSettings(response.data);
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = (key) => {
    setSettings({...settings, [key]: !settings[key]});
  };

  const handleChange = (key, value) => {
    setSettings({...settings, [key]: value});
  };

  const handleSave = async () => {
    try {
      await updateSecuritySettings(settings);
      alert('Security settings saved successfully!');
    } catch (err) {
      console.error('Failed to save:', err);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading security settings...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Security Settings</h1>
        <p>Configure security policies and protections</p>
      </div>

      <div className="content-card">
        <div className="security-section">
          <h3>Password Policy</h3>
          
          <div className="security-option">
            <div className="info">
              <h4>Minimum Password Length</h4>
              <p>Minimum number of characters required</p>
            </div>
            <input 
              type="number" 
              value={settings.password_min_length}
              onChange={(e) => handleChange('password_min_length', parseInt(e.target.value))}
              style={{width: '80px'}}
            />
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Require Uppercase Letters</h4>
              <p>Passwords must contain uppercase letters</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.password_require_uppercase}
                onChange={() => handleToggle('password_require_uppercase')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Require Lowercase Letters</h4>
              <p>Passwords must contain lowercase letters</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.password_require_lowercase}
                onChange={() => handleToggle('password_require_lowercase')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Require Numbers</h4>
              <p>Passwords must contain numbers</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.password_require_numbers}
                onChange={() => handleToggle('password_require_numbers')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <div className="security-section">
          <h3>Account Security</h3>
          
          <div className="security-option">
            <div className="info">
              <h4>Max Login Attempts</h4>
              <p>Number of failed attempts before lockout</p>
            </div>
            <input 
              type="number" 
              value={settings.max_login_attempts}
              onChange={(e) => handleChange('max_login_attempts', parseInt(e.target.value))}
              style={{width: '80px'}}
            />
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Lockout Duration (minutes)</h4>
              <p>Time account stays locked after max attempts</p>
            </div>
            <input 
              type="number" 
              value={settings.lockout_duration}
              onChange={(e) => handleChange('lockout_duration', parseInt(e.target.value))}
              style={{width: '80px'}}
            />
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Session Timeout (minutes)</h4>
              <p>Auto logout after inactivity</p>
            </div>
            <input 
              type="number" 
              value={settings.session_timeout}
              onChange={(e) => handleChange('session_timeout', parseInt(e.target.value))}
              style={{width: '80px'}}
            />
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Two-Factor Authentication</h4>
              <p>Enable 2FA for all users</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.enable_2fa}
                onChange={() => handleToggle('enable_2fa')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Email Verification</h4>
              <p>Require email verification for new accounts</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.require_email_verification}
                onChange={() => handleToggle('require_email_verification')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <div className="security-section">
          <h3>System Security</h3>
          
          <div className="security-option">
            <div className="info">
              <h4>Enable CAPTCHA</h4>
              <p>Show CAPTCHA on login and registration</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.enable_captcha}
                onChange={() => handleToggle('enable_captcha')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Audit Logging</h4>
              <p>Log all user activities</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.audit_logging}
                onChange={() => handleToggle('audit_logging')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="security-option">
            <div className="info">
              <h4>Data Encryption</h4>
              <p>Encrypt sensitive data at rest</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.data_encryption}
                onChange={() => handleToggle('data_encryption')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <button className="btn-submit" style={{marginTop: '20px'}} onClick={handleSave}>
        Save Security Settings
      </button>
    </div>
  );
};

export default Security;
