import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getGroup, manageGroupMembers, getGroups } from '../../api/authority';
import './AuthorityGroups.css';

const AuthorityManageGroup = () => {
  const { groupId } = useParams();
  const [group, setGroup] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('members');

  useEffect(() => {
    loadGroup();
  }, [groupId]);

  const loadGroup = async () => {
    try {
      if (groupId) {
        const response = await getGroup(groupId);
        setGroup(response.data);
      }
    } catch (err) {
      console.error('Failed to load group:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMember = async (memberId) => {
    try {
      const currentMembers = group.members.filter(m => m.id !== memberId);
      await manageGroupMembers(groupId, { members: currentMembers.map(m => m.id) });
      loadGroup();
    } catch (err) {
      console.error('Failed to remove member:', err);
    }
  };

  const handleAddMembers = async () => {
    // This would open a modal to add members
    alert('Add members feature - implement with modal');
  };

  if (loading) {
    return <div className="manage-group-loading">Loading group...</div>;
  }

  if (!group) {
    return <div className="manage-group-loading">Group not found</div>;
  }

  return (
    <div className="manage-group-page">
      <div className="group-info-card">
        <h2>{group.name}</h2>
        <p>{group.description || 'No description'}</p>
        <div className="group-meta">
          <span className="group-type-badge">{group.group_type}</span>
          {group.is_private && <span className="group-type-badge private-badge">Private</span>}
          <span className="member-count">{group.members?.length || 0} members</span>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          Members
        </button>
        <button 
          className={`tab ${activeTab === 'posts' ? 'active' : ''}`}
          onClick={() => setActiveTab('posts')}
        >
          Posts
        </button>
        <button 
          className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </button>
      </div>

      {activeTab === 'members' && (
        <div className="members-section">
          <div className="section-header">
            <h3>Group Members</h3>
            <button className="btn-primary" onClick={handleAddMembers}>
              + Add Members
            </button>
          </div>
          
          {group.members && group.members.length > 0 ? (
            <div className="members-list">
              {group.members.map((member) => (
                <div key={member.id} className="member-item">
                  <div className="member-info">
                    <div className="member-avatar">
                      {member.name?.charAt(0).toUpperCase() || 'M'}
                    </div>
                    <div className="member-details">
                      <span className="name">{member.name}</span>
                      <span className="role">{member.role || 'Member'}</span>
                    </div>
                  </div>
                  <div className="member-actions">
                    <button onClick={() => handleRemoveMember(member.id)}>
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <span className="empty-icon">👥</span>
              <p>No members in this group</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'posts' && (
        <div className="members-section">
          <h3>Group Posts</h3>
          <div className="empty-state">
            <span className="empty-icon">📝</span>
            <p>No posts in this group yet</p>
          </div>
        </div>
      )}

      {activeTab === 'settings' && (
        <div className="members-section">
          <h3>Group Settings</h3>
          <form className="settings-form">
            <div className="form-group">
              <label>Group Name</label>
              <input type="text" defaultValue={group.name} />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea defaultValue={group.description} rows={4} />
            </div>
            <div className="form-group">
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked={group.is_private} />
                <span>Private Group</span>
              </label>
            </div>
            <button type="submit" className="btn-submit">Save Changes</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default AuthorityManageGroup;
