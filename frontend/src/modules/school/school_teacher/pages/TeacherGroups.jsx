import { useState, useEffect } from 'react';
import { getTeacherGroups } from '../api/teachers';
import './TeacherPortal.css';

const TeacherGroups = () => {
  const [loading, setLoading] = useState(true);
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    loadGroups();
  }, []);

  const loadGroups = async () => {
    try {
      const response = await getTeacherGroups();
      setGroups(response.data || response);
    } catch (err) {
      console.error('Failed to load groups:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="teacher-loading">Loading groups...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <h1>My Groups</h1>
        <p>Groups you manage or participate in</p>
      </div>

      <div className="teacher-card">
        {groups.length > 0 ? (
          <div className="groups-grid">
            {groups.map((group) => (
              <div key={group.id} className="group-card">
                <div className="group-icon">
                  {group.type === 'class' ? '👨‍🎓' : group.type === 'club' ? '⚽' : '👥'}
                </div>
                <div className="group-info">
                  <h4>{group.name}</h4>
                  <p>{group.member_count || 0} members</p>
                </div>
                <button className="action-btn">View</button>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">👥</span>
            <p>No groups found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherGroups;
