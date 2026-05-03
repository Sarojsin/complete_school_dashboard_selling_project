import { useEffect, useState } from 'react';
import { getBackups, createBackup, restoreBackup, deleteBackup } from '../api/superadmin';
import '@shared/styles/global.css';
import '../styles/superadmin.css';

export default function Backups() {
  const [backups, setBackups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchBackups();
  }, []);

  const fetchBackups = async () => {
    try {
      setLoading(true);
      const res = await getBackups();
      setBackups(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBackup = async () => {
    try {
      setCreating(true);
      await createBackup();
      alert('Backup created successfully!');
      fetchBackups();
    } catch (err) {
      alert('Failed to create backup: ' + err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleRestore = async (backupId) => {
    if (!window.confirm('Are you sure you want to restore this backup? This will overwrite current data.')) return;
    try {
      await restoreBackup(backupId);
      alert('Backup restored successfully!');
    } catch (err) {
      alert('Failed to restore backup: ' + err.message);
    }
  };

  const handleDelete = async (backupId) => {
    if (!window.confirm('Are you sure you want to delete this backup?')) return;
    try {
      await deleteBackup(backupId);
      setBackups(backups.filter(b => b.id !== backupId));
      alert('Backup deleted successfully!');
    } catch (err) {
      alert('Failed to delete backup: ' + err.message);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const formatSize = (bytes) => {
    if (!bytes) return 'N/A';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
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
        <h1>Backup Management</h1>
        <p>Create and manage system backups</p>
      </div>

      {/* Create Backup Button */}
      <div className="backup-actions">
        <button 
          className="btn btn-success"
          onClick={handleCreateBackup}
          disabled={creating}
        >
          {creating ? 'Creating...' : '+ Create New Backup'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Backups List */}
      <div className="backups-container">
        <table className="data-table backups-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Filename</th>
              <th>Size</th>
              <th>Created</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {backups.map((backup) => (
              <tr key={backup.id}>
                <td>{backup.id}</td>
                <td>{backup.filename}</td>
                <td>{formatSize(backup.size)}</td>
                <td>{formatDate(backup.created_at)}</td>
                <td>
                  <span className={`status-badge ${backup.status}`}>
                    {backup.status}
                  </span>
                </td>
                <td>
                  <div className="action-buttons">
                    <button 
                      className="btn btn-sm btn-primary"
                      onClick={() => window.open(`/admin/backups/${backup.id}/download`)}
                    >
                      Download
                    </button>
                    <button 
                      className="btn btn-sm btn-success"
                      onClick={() => handleRestore(backup.id)}
                      disabled={backup.status !== 'completed'}
                    >
                      Restore
                    </button>
                    <button 
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(backup.id)}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {backups.length === 0 && (
        <div className="no-data">
          <p>No backups found. Create a new backup to get started.</p>
        </div>
      )}
    </div>
  );
}
