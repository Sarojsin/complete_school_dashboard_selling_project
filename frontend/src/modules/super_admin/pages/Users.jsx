import { useEffect, useState } from 'react';
import { getAllUsers, getUsersByRole, deactivateUser, activateUser } from '../api/superadmin';
import '@shared/styles/global.css';
import '../styles/superadmin.css';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [userStats, setUserStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [usersRes, statsRes] = await Promise.all([
        getAllUsers(),
        getUsersByRole()
      ]);
      setUsers(usersRes.data || []);
      setUserStats(statsRes.data || {});
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDeactivate = async (userId) => {
    if (!window.confirm('Are you sure you want to deactivate this user?')) return;
    try {
      await deactivateUser(userId);
      setUsers(users.map(u => u.id === userId ? { ...u, is_active: false } : u));
      alert('User deactivated successfully!');
    } catch (err) {
      alert('Failed to deactivate user: ' + err.message);
    }
  };

  const handleActivate = async (userId) => {
    try {
      await activateUser(userId);
      setUsers(users.map(u => u.id === userId ? { ...u, is_active: true } : u));
      alert('User activated successfully!');
    } catch (err) {
      alert('Failed to activate user: ' + err.message);
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      user.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.first_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.last_name?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    
    return matchesSearch && matchesRole;
  });

  const roles = ['all', 'student', 'teacher', 'parent', 'authority', 'admin', 'hod', 'exam_section', 'library', 'account'];

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
        <h1>User Management</h1>
        <p>Manage all system users</p>
      </div>

      {/* User Stats */}
      <div className="stats-grid">
        {Object.entries(userStats).map(([role, count]) => (
          <div key={role} className="stat-card">
            <h3>{role.charAt(0).toUpperCase() + role.slice(1)}s</h3>
            <p className="stat-value">{count}</p>
          </div>
        ))}
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Search and Filter */}
      <div className="toolbar">
        <input
          type="text"
          placeholder="Search users..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        
        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          className="role-filter"
        >
          {roles.map(role => (
            <option key={role} value={role}>
              {role === 'all' ? 'All Roles' : role.charAt(0).toUpperCase() + role.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Users Table */}
      <div className="users-table-container">
        <table className="data-table users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.first_name} {user.last_name}</td>
                <td>{user.email}</td>
                <td>
                  <span className="role-badge">
                    {user.role}
                  </span>
                </td>
                <td>
                  <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                  <div className="action-buttons">
                    <button
                      className="btn btn-sm btn-info"
                      onClick={() => setSelectedUser(user)}
                    >
                      View
                    </button>
                    {user.is_active ? (
                      <button
                        className="btn btn-sm btn-warning"
                        onClick={() => handleDeactivate(user.id)}
                      >
                        Deactivate
                      </button>
                    ) : (
                      <button
                        className="btn btn-sm btn-success"
                        onClick={() => handleActivate(user.id)}
                      >
                        Activate
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
