import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getAllGroups, searchGroups, joinGroup } from '../api/groups';
import '../../../shared/styles/global.css';
import '../styles/groups.css';

export default function GroupList() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [joining, setJoining] = useState(false);

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    try {
      setLoading(true);
      const res = await getAllGroups();
      setGroups(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (searchQuery) {
        const res = await searchGroups(searchQuery);
        setGroups(res.data || []);
      } else {
        await fetchGroups();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async (e) => {
    e.preventDefault();
    if (!joinCode.trim()) return;
    
    try {
      setJoining(true);
      await joinGroup(joinCode);
      alert('Successfully joined the group!');
      setJoinCode('');
      fetchGroups();
    } catch (err) {
      alert('Failed to join group: ' + err.message);
    } finally {
      setJoining(false);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      NOTICE: '#dc3545',
      NOTE: '#28a745',
      LINK: '#007bff',
      GENERAL: '#6c757d'
    };
    return colors[category] || colors.GENERAL;
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
        <h1>Student Groups</h1>
        <p>Join groups and collaborate with classmates</p>
      </div>

      {/* Join Group Form */}
      <div className="join-group-section">
        <form className="join-form" onSubmit={handleJoin}>
          <input
            type="text"
            placeholder="Enter group code to join..."
            value={joinCode}
            onChange={(e) => setJoinCode(e.target.value)}
            className="join-input"
          />
          <button type="submit" className="btn btn-primary" disabled={joining}>
            {joining ? 'Joining...' : 'Join Group'}
          </button>
        </form>
      </div>

      {/* Search */}
      <div className="search-section">
        <form className="search-form" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search groups..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="btn btn-secondary">Search</button>
        </form>
        <Link to="/groups/create" className="btn btn-success">
          + Create Group
        </Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Groups Grid */}
      <div className="groups-grid">
        {groups.length > 0 ? (
          groups.map((group) => (
            <div key={group.id} className="group-card">
              <div className="group-header">
                <h3>{group.name}</h3>
                <span 
                  className="group-category"
                  style={{ backgroundColor: getCategoryColor(group.category) }}
                >
                  {group.category}
                </span>
              </div>
              <p className="group-description">{group.description}</p>
              <div className="group-stats">
                <span>👥 {group.members_count || 0} members</span>
                <span>📝 {group.posts_count || 0} posts</span>
              </div>
              <div className="group-code">
                <small>Code: <code>{group.code}</code></small>
              </div>
              <Link to={`/groups/${group.id}`} className="btn btn-primary">
                View Group
              </Link>
            </div>
          ))
        ) : (
          <div className="no-data">
            <p>No groups found. Create or join a group to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
}
