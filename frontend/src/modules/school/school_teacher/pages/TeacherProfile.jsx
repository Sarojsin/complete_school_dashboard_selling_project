import { useState, useEffect } from 'react';
import { getTeacherProfile, updateTeacherProfile } from '../api/teachers';
import './TeacherPortal.css';

const TeacherProfile = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    address: '',
    qualification: '',
    experience: '',
    department: '',
    designation: ''
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await getTeacherProfile();
      setProfile(response.data);
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field, value) => {
    setProfile({...profile, [field]: value});
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateTeacherProfile(profile);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error('Failed to update:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="teacher-loading">Loading profile...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <h1>My Profile</h1>
        <p>View and update your profile information</p>
      </div>

      <div className="teacher-card">
        <h3>Personal Information</h3>
        
        <div className="form-row">
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => handleChange('name', e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={profile.email}
              onChange={(e) => handleChange('email', e.target.value)}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Phone</label>
            <input
              type="text"
              value={profile.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Date of Birth</label>
            <input
              type="date"
              value={profile.date_of_birth}
              onChange={(e) => handleChange('date_of_birth', e.target.value)}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Gender</label>
            <select
              value={profile.gender}
              onChange={(e) => handleChange('gender', e.target.value)}
            >
              <option value="">Select Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="form-group">
            <label>Address</label>
            <input
              type="text"
              value={profile.address}
              onChange={(e) => handleChange('address', e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="teacher-card" style={{marginTop: '20px'}}>
        <h3>Professional Information</h3>
        
        <div className="form-row">
          <div className="form-group">
            <label>Qualification</label>
            <input
              type="text"
              value={profile.qualification}
              onChange={(e) => handleChange('qualification', e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Experience (Years)</label>
            <input
              type="number"
              value={profile.experience}
              onChange={(e) => handleChange('experience', e.target.value)}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Department</label>
            <input
              type="text"
              value={profile.department}
              onChange={(e) => handleChange('department', e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Designation</label>
            <input
              type="text"
              value={profile.designation}
              onChange={(e) => handleChange('designation', e.target.value)}
            />
          </div>
        </div>
      </div>

      <button 
        className="btn-success" 
        style={{marginTop: '20px'}}
        onClick={handleSave}
        disabled={saving}
      >
        {saving ? 'Saving...' : 'Save Changes'}
      </button>
    </div>
  );
};

export default TeacherProfile;
