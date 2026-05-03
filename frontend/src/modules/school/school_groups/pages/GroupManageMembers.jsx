import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getGroupById, getGroupMembers, addGroupMember, removeGroupMember } from '../api/groups';
import '../styles/groups.css';

const GroupManageMembers = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [group, setGroup] = useState(null);
  const [members, setMembers] = useState([]);
  const [newMemberId, setNewMemberId] = useState('');

  useEffect(() => { loadData(); }, [groupId]);

  const loadData = async () => {
    try {
      const [groupRes, membersRes] = await Promise.all([
        getGroupById(groupId),
        getGroupMembers(groupId)
      ]);
      setGroup(groupRes.data || groupRes);
      setMembers(membersRes.data || membersRes);
    } catch (err) { console.error('Failed:', err); }
    finally { setLoading(false); }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    try {
      await addGroupMember(groupId, newMemberId);
      setNewMemberId('');
      loadData();
    } catch (err) { console.error('Failed:', err); }
  };

  const handleRemoveMember = async (userId) => {
    if (window.confirm('Remove this member?')) {
      try {
        await removeGroupMember(groupId, userId);
        loadData();
      } catch (err) { console.error('Failed:', err); }
    }
  };

  if (loading) return <div className="groups-loading">Loading...</div>;

  return (
    <div className="groups-page">
      <button className="back-btn" onClick={() => navigate(-1)}>← Back</button>
      <h1>Manage Members - {group?.name}</h1>
      
      <div className="groups-card">
        <h3>Add Member</h3>
        <form onSubmit={handleAddMember} className="add-member-form">
          <input 
            type="text" 
            placeholder="Enter User ID" 
            value={newMemberId}
            onChange={(e) => setNewMemberId(e.target.value)}
            required
          />
          <button type="submit" className="groups-btn primary">Add</button>
        </form>
      </div>

      <div className="groups-card">
        <h3>Members ({members.length})</h3>
        <div className="members-list">
          {members.map((member) => (
            <div key={member.id} className="member-item">
              <span>{member.name}</span>
              <span className="role">{member.role}</span>
              <button onClick={() => handleRemoveMember(member.id)}>Remove</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GroupManageMembers;
