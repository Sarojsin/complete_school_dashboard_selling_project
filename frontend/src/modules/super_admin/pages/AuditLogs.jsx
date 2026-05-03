import { useEffect, useState } from 'react';
import { getAuditLogs } from '../api/superadmin';
import '@shared/styles/global.css';
import '../styles/superadmin.css';

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    user_id: '',
    action: '',
    start_date: '',
    end_date: ''
  });
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchLogs();
  }, [page, filters]);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const params = {
        page,
        ...filters
      };
      // Remove empty filters
      Object.keys(params).forEach(key => {
        if (!params[key]) delete params[key];
      });
      
      const res = await getAuditLogs(params);
      setLogs(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    setPage(1);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const getActionColor = (action) => {
    if (!action) return '';
    const actionLower = action.toLowerCase();
    if (actionLower.includes('create') || actionLower.includes('add')) return 'action-create';
    if (actionLower.includes('update') || actionLower.includes('edit')) return 'action-update';
    if (actionLower.includes('delete') || actionLower.includes('remove')) return 'action-delete';
    if (actionLower.includes('login') || actionLower.includes('auth')) return 'action-auth';
    return '';
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
        <h1>Audit Logs</h1>
        <p>View system activity logs</p>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="filter-row">
          <div className="filter-group">
            <label>User ID</label>
            <input
              type="text"
              name="user_id"
              value={filters.user_id}
              onChange={handleFilterChange}
              placeholder="Filter by user ID"
            />
          </div>
          <div className="filter-group">
            <label>Action</label>
            <select name="action" value={filters.action} onChange={handleFilterChange}>
              <option value="">All Actions</option>
              <option value="create">Create</option>
              <option value="update">Update</option>
              <option value="delete">Delete</option>
              <option value="login">Login</option>
              <option value="logout">Logout</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Start Date</label>
            <input
              type="date"
              name="start_date"
              value={filters.start_date}
              onChange={handleFilterChange}
            />
          </div>
          <div className="filter-group">
            <label>End Date</label>
            <input
              type="date"
              name="end_date"
              value={filters.end_date}
              onChange={handleFilterChange}
            />
          </div>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Logs Table */}
      <div className="logs-container">
        <table className="data-table logs-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Action</th>
              <th>Resource</th>
              <th>IP Address</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.user_email || `User #${log.user_id}`}</td>
                <td>
                  <span className={`action-badge ${getActionColor(log.action)}`}>
                    {log.action}
                  </span>
                </td>
                <td>{log.resource || 'N/A'}</td>
                <td>{log.ip_address || 'N/A'}</td>
                <td>{formatDate(log.timestamp)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="pagination">
        <button 
          className="btn btn-sm"
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span className="page-info">Page {page}</span>
        <button 
          className="btn btn-sm"
          onClick={() => setPage(p => p + 1)}
          disabled={logs.length < 20}
        >
          Next
        </button>
      </div>

      {logs.length === 0 && (
        <div className="no-data">
          <p>No audit logs found.</p>
        </div>
      )}
    </div>
  );
}
