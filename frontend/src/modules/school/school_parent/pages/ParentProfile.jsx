import { useEffect, useState } from 'react';
import { getParentProfile, updateParentProfile } from '../api/parents';
import '../../../shared/styles/global.css';
import '../styles/parent.css';

export default function ParentProfile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const res = await getParentProfile();
      setProfile(res.data);
      setFormData(res.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateParentProfile(formData);
      setProfile(formData);
      setIsEditing(false);
      alert('Profile updated successfully!');
    } catch (err) {
      setError(err.message);
    }
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
        <h1>My Profile</h1>
        <p>View and edit your profile information</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="profile-container">
        {/* Profile Header */}
        <div className="profile-header">
          <div className="profile-avatar">
            {profile?.first_name?.charAt(0) || 'P'}
          </div>
          <div className="profile-info">
            <h2>{profile?.first_name} {profile?.last_name}</h2>
            <p>{profile?.email}</p>
            <span className="role-badge">{profile?.role || 'Parent'}</span>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => setIsEditing(!isEditing)}
          >
            {isEditing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {/* Profile Form */}
        {isEditing ? (
          <form className="profile-form" onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>First Name</label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name || ''}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email || ''}
                onChange={handleChange}
                disabled
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Phone</label>
                <input
                  type="text"
                  name="phone"
                  value={formData.phone || ''}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Occupation</label>
                <input
                  type="text"
                  name="occupation"
                  value={formData.occupation || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Address</label>
              <textarea
                name="address"
                value={formData.address || ''}
                onChange={handleChange}
                rows="3"
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-success">
                Save Changes
              </button>
            </div>
          </form>
        ) : (
          <div className="profile-details">
            <div className="detail-row">
              <span className="detail-label">First Name</span>
              <span className="detail-value">{profile?.first_name || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Last Name</span>
              <span className="detail-value">{profile?.last_name || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Email</span>
              <span className="detail-value">{profile?.email || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Phone</span>
              <span className="detail-value">{profile?.phone || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Occupation</span>
              <span className="detail-value">{profile?.occupation || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Address</span>
              <span className="detail-value">{profile?.address || 'N/A'}</span>
            </div>
          </div>
        )}

        {/* Linked Children Section */}
        <div className="linked-children-section">
          <h3>Linked Children</h3>
          {profile?.children && profile.children.length > 0 ? (
            <div className="children-list">
              {profile.children.map((child, index) => (
                <div key={index} className="child-item">
                  <div className="child-avatar-small">
                    {child.student_name?.charAt(0)}
                  </div>
                  <div className="child-details">
                    <p className="child-name">{child.student_name}</p>
                    <p className="child-class">{child.class} - {child.section}</p>
                    <p className="child-relation">Relation: {child.relation}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data">No children linked to your account.</p>
          )}
        </div>
      </div>
    </div>
  );
}
