import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const HODProfile = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    qualifications: '',
    experience: '',
    department: ''
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await fetch('/api/hod/profile', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setProfile(data);
      setFormData({
        name: data.name || '',
        email: data.email || '',
        phone: data.phone || '',
        address: data.address || '',
        qualifications: data.qualifications || '',
        experience: data.experience || '',
        department: data.department || ''
      });
      setLoading(false);
    } catch (err) {
      setError('Failed to load profile');
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const response = await fetch('/api/hod/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSuccess('Profile updated successfully!');
        setEditing(false);
        loadProfile();
      } else {
        setError('Failed to update profile');
      }
    } catch (err) {
      setError('An error occurred');
    }
  };

  const handleAvatarChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('avatar', file);

    try {
      const response = await fetch('/api/hod/profile/avatar', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (response.ok) {
        loadProfile();
      } else {
        setError('Failed to upload avatar');
      }
    } catch (err) {
      setError('An error occurred');
    }
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="hod-profile-container">
      <div className="page-header">
        <h1>My Profile</h1>
        <button onClick={() => navigate('/hod')} className="back-btn">
          ← Back to Dashboard
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="profile-layout">
        <div className="profile-sidebar">
          <div className="profile-avatar-section">
            <img 
              src={profile?.avatar ? `/uploads/avatars/${profile.avatar}` : '/images/default-avatar.png'}
              alt={profile?.name}
              className="profile-avatar-large"
            />
            <label className="avatar-upload-btn">
              Change Photo
              <input 
                type="file" 
                accept="image/*"
                onChange={handleAvatarChange}
                hidden
              />
            </label>
          </div>
          
          <div className="profile-quick-info">
            <h2>{profile?.name}</h2>
            <p className="role">Head of Department</p>
            <p className="department">{profile?.department}</p>
          </div>

          <div className="profile-stats">
            <div className="stat">
              <span className="stat-value">{profile?.teachers_count || 0}</span>
              <span className="stat-label">Teachers</span>
            </div>
            <div className="stat">
              <span className="stat-value">{profile?.students_count || 0}</span>
              <span className="stat-label">Students</span>
            </div>
            <div className="stat">
              <span className="stat-value">{profile?.courses_count || 0}</span>
              <span className="stat-label">Courses</span>
            </div>
          </div>
        </div>

        <div className="profile-main">
          <div className="profile-header">
            <h2>Profile Information</h2>
            <button 
              onClick={() => setEditing(!editing)}
              className="btn-secondary"
            >
              {editing ? 'Cancel' : 'Edit Profile'}
            </button>
          </div>

          {editing ? (
            <form onSubmit={handleSubmit} className="profile-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Full Name</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                  />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Phone</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                  />
                </div>
                <div className="form-group">
                  <label>Department</label>
                  <input
                    type="text"
                    name="department"
                    value={formData.department}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Address</label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Qualifications</label>
                <textarea
                  name="qualifications"
                  value={formData.qualifications}
                  onChange={handleChange}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label>Experience</label>
                <textarea
                  name="experience"
                  value={formData.experience}
                  onChange={handleChange}
                  rows="3"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  Save Changes
                </button>
              </div>
            </form>
          ) : (
            <div className="profile-details">
              <div className="detail-section">
                <h3>Contact Information</h3>
                <div className="detail-row">
                  <span className="detail-label">Email</span>
                  <span className="detail-value">{profile?.email || 'Not provided'}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Phone</span>
                  <span className="detail-value">{profile?.phone || 'Not provided'}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Address</span>
                  <span className="detail-value">{profile?.address || 'Not provided'}</span>
                </div>
              </div>

              <div className="detail-section">
                <h3>Professional Information</h3>
                <div className="detail-row">
                  <span className="detail-label">Department</span>
                  <span className="detail-value">{profile?.department || 'Not provided'}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Qualifications</span>
                  <span className="detail-value">{profile?.qualifications || 'Not provided'}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Experience</span>
                  <span className="detail-value">{profile?.experience || 'Not provided'}</span>
                </div>
              </div>

              <div className="detail-section">
                <h3>Account Information</h3>
                <div className="detail-row">
                  <span className="detail-label">Member Since</span>
                  <span className="detail-value">
                    {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'Unknown'}
                  </span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Last Updated</span>
                  <span className="detail-value">
                    {profile?.updated_at ? new Date(profile.updated_at).toLocaleDateString() : 'Unknown'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HODProfile;
