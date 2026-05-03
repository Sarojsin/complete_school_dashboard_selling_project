import { useState, useEffect } from 'react';
import { getSystemInfo } from '../api/superadmin';
import './AdminPages.css';

const System = () => {
  const [loading, setLoading] = useState(true);
  const [systemInfo, setSystemInfo] = useState(null);

  useEffect(() => {
    loadSystemInfo();
  }, []);

  const loadSystemInfo = async () => {
    try {
      const response = await getSystemInfo();
      setSystemInfo(response.data);
    } catch (err) {
      console.error('Failed to load system info:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading system information...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>System Information</h1>
        <p>View server and application details</p>
      </div>

      <div className="content-card">
        <h3>Server Information</h3>
        <div className="info-grid">
          <div className="info-item">
            <label>Operating System</label>
            <span>{systemInfo?.os || 'Linux'}</span>
          </div>
          <div className="info-item">
            <label>Server Type</label>
            <span>{systemInfo?.server || 'Nginx'}</span>
          </div>
          <div className="info-item">
            <label>Python Version</label>
            <span>{systemInfo?.python_version || '3.10'}</span>
          </div>
          <div className="info-item">
            <label>Database</label>
            <span>{systemInfo?.database || 'PostgreSQL'}</span>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Application Information</h3>
        <div className="info-grid">
          <div className="info-item">
            <label>Application Version</label>
            <span>{systemInfo?.app_version || '1.0.0'}</span>
          </div>
          <div className="info-item">
            <label>Environment</label>
            <span>{systemInfo?.environment || 'Production'}</span>
          </div>
          <div className="info-item">
            <label>Timezone</label>
            <span>{systemInfo?.timezone || 'UTC'}</span>
          </div>
          <div className="info-item">
            <label>Last Updated</label>
            <span>{systemInfo?.last_updated || 'N/A'}</span>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Resource Usage</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.cpu_usage || '0'}%</span>
            <span className="stat-label">CPU Usage</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.memory_usage || '0'}%</span>
            <span className="stat-label">Memory Usage</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.disk_usage || '0'}%</span>
            <span className="stat-label">Disk Usage</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.uptime || '0'}h</span>
            <span className="stat-label">Uptime</span>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>Database Statistics</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.total_users || '0'}</span>
            <span className="stat-label">Total Users</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.total_schools || '0'}</span>
            <span className="stat-label">Schools</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.active_connections || '0'}</span>
            <span className="stat-label">Active Connections</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{systemInfo?.db_size || '0 MB'}</span>
            <span className="stat-label">Database Size</span>
          </div>
        </div>
      </div>

      <div className="content-card" style={{marginTop: '20px'}}>
        <h3>API Endpoints</h3>
        <div className="endpoints-list">
          {systemInfo?.endpoints?.map((endpoint) => (
            <div key={endpoint.path} className="endpoint-item">
              <span className="method-badge">{endpoint.method}</span>
              <span className="path">{endpoint.path}</span>
              <span className={`status-badge ${endpoint.status}`}>
                {endpoint.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default System;
