import React, { useEffect, useState } from 'react';
import { getMyTeacherProfile } from '../api/teachers';
import { logout } from '../../../auth/api/auth';

export default function TeacherDashboard() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getMyTeacherProfile()
      .then(res => setProfile(res.data))
      .catch(err => setError('Failed to load profile'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Teacher Dashboard</h1>
        <button onClick={logout} style={{ width: 'auto', padding: '0.5rem 1rem' }}>Logout</button>
      </div>
      
      {profile && (
        <div className="profile-card" style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
          <h3>Welcome, {profile.full_name}</h3>
          <p><strong>Employee ID:</strong> {profile.employee_id}</p>
          <p><strong>Department:</strong> {profile.department}</p>
          <p><strong>Specialization:</strong> {profile.specialization}</p>
        </div>
      )}
    </div>
  );
}
