import { useState, useEffect } from 'react';
import { useStudentProfile } from '../hooks/useStudent';
import Card from '../../../shared/components/Card';
import Badge from '../../../shared/components/Badge';
import './StudentProfile.css';

const StudentProfile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [activeTab, setActiveTab] = useState('personal');

  // Mock profile data
  const mockProfile = {
    id: 'STU-2024-001',
    name: 'Alex Johnson',
    email: 'alex.johnson@student.edu',
    phone: '+1 234-567-8900',
    avatar: null,
    date_of_birth: '2005-06-15',
    gender: 'Male',
    address: '123 Main Street, City, State 12345',
    class_name: 'Class 12 - Science',
    roll_number: '15',
    section: 'A',
    session: '2023-2024',
    attendance: 94,
    father_name: 'Robert Johnson',
    mother_name: 'Mary Johnson',
    parent_phone: '+1 234-567-8901',
    blood_group: 'O+',
    emergency_contact: '+1 234-567-8902',
    admission_date: '2020-04-01',
    transport_route: 'Route A - North Campus',
    hostel: 'Day Scholar',
    achievements: ['Science Olympiad - 1st Place', 'Basketball Team Captain', 'Perfect Attendance Award'],
    subjects: ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English'],
  };

  const { data: profileData, isLoading, refetch } = useStudentProfile();

  // Map backend data to frontend format
  const mapBackendToFrontend = (data) => {
    if (!data) return mockProfile;
    return {
      id: data.student_id || data.id,
      name: data.full_name || 'Student',
      email: data.email || '',
      phone: data.phone || '',
      date_of_birth: data.date_of_birth || '',
      gender: data.gender || 'Not specified',
      address: data.address || '',
      class_name: data.grade_level || 'N/A',
      roll_number: data.roll_number || 'N/A',
      section: data.section || 'N/A',
      session: new Date().getFullYear().toString(),
      attendance: data.attendance || 0,
      father_name: data.parent_name || 'N/A',
      mother_name: data.parent_name || 'N/A',
      parent_phone: data.parent_phone || '',
      blood_group: data.blood_group || 'N/A',
      emergency_contact: data.emergency_contact || '',
      admission_date: data.enrollment_date || '',
      transport_route: 'Not assigned',
      hostel: 'Day Scholar',
      achievements: [],
      subjects: [],
    };
  };

  useEffect(() => {
    if (profileData) {
      const mappedData = mapBackendToFrontend(profileData);
      setProfile(mappedData);
      setFormData(mappedData);
    } else if (!isLoading) {
      setProfile(mockProfile);
      setFormData(mockProfile);
    }
    if (!isLoading) {
      setLoading(false);
    }
  }, [profileData, isLoading]);

  const loadProfile = async () => {
    await refetch();
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Map frontend form data back to backend format
      const backendData = {
        full_name: formData.name,
        phone: formData.phone,
        date_of_birth: formData.date_of_birth,
        address: formData.address,
        parent_name: formData.father_name,
        parent_phone: formData.parent_phone,
      };
      
      // Use the updateMyProfile API function
      const { updateMyProfile } = await import('../api/students');
      await updateMyProfile(backendData);
      
      setProfile(formData);
      setEditing(false);
    } catch (err) {
      console.error('Failed to update profile:', err);
    }
  };

  const getAvatarUrl = (avatar, name) => {
    if (avatar) return avatar.startsWith('http') ? avatar : `/uploads/avatars/${avatar}`;
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&color=fff&size=150`;
  };

  if (isLoading || loading) {
    return <div className="profile-loading">Loading profile...</div>;
  }

  return (
    <div className="student-profile-page">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>My Profile</h1>
          <p className="text-muted mb-0">View and manage your personal information</p>
        </div>
        <button 
          className={`btn ${editing ? 'btn-secondary' : 'btn-primary'}`}
          onClick={() => setEditing(!editing)}
        >
          <i className={`bi ${editing ? 'bi-x-circle' : 'bi-pencil-square'} me-2`}></i>
          {editing ? 'Cancel' : 'Edit Profile'}
        </button>
      </div>

      {/* Profile Header Card */}
      <Card className="mb-4">
        <div className="row align-items-center">
          <div className="col-md-3 text-center">
            <div className="position-relative d-inline-block">
              <img 
                src={getAvatarUrl(profile?.avatar, profile?.name)} 
                alt={profile?.name}
                className="rounded-circle mb-3"
                style={{ width: '120px', height: '120px', objectFit: 'cover', border: '4px solid var(--primary-color)' }}
              />
              <span 
                className="position-absolute bottom-0 start-50 translate-middle-x badge bg-success"
                style={{ fontSize: '0.7rem' }}
              >
                Active
              </span>
            </div>
            {editing && (
              <button className="btn btn-sm btn-outline-primary d-block mx-auto mt-2">
                <i className="bi bi-camera me-1"></i>Change Photo
              </button>
            )}
          </div>
          <div className="col-md-6">
            <h3 className="mb-1">{profile?.name}</h3>
            <p className="text-muted mb-2">
              <i className="bi bi-mortarboard me-2"></i>
              {profile?.class_name} - Section {profile?.section}
            </p>
            <div className="d-flex flex-wrap gap-2 mb-3">
              <Badge variant="primary"><i className="bi bi-hash me-1"></i>{profile?.id}</Badge>
              <Badge variant="info"><i className="bi bi-person-badge me-1"></i>Roll: {profile?.roll_number}</Badge>
              <Badge variant="success"><i className="bi bi-calendar-check me-1"></i>{profile?.attendance}% Attendance</Badge>
            </div>
            <div className="d-flex flex-wrap gap-3">
              <span className="text-muted small">
                <i className="bi bi-envelope me-1"></i>{profile?.email}
              </span>
              <span className="text-muted small">
                <i className="bi bi-telephone me-1"></i>{profile?.phone}
              </span>
            </div>
          </div>
          <div className="col-md-3 text-md-end">
            <div className="quick-stats">
              <div className="mb-2">
                <small className="text-muted">Blood Group</small>
                <div className="fw-bold">{profile?.blood_group}</div>
              </div>
              <div className="mb-2">
                <small className="text-muted">Transport</small>
                <div className="fw-bold">{profile?.transport_route}</div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Tabs */}
      <div className="row">
        <div className="col-lg-3">
          <Card className="mb-4">
            <div className="list-group">
              <button 
                className={`list-group-item list-group-item-action ${activeTab === 'personal' ? 'active' : ''}`}
                onClick={() => setActiveTab('personal')}
              >
                <i className="bi bi-person me-2"></i>Personal Info
              </button>
              <button 
                className={`list-group-item list-group-item-action ${activeTab === 'academic' ? 'active' : ''}`}
                onClick={() => setActiveTab('academic')}
              >
                <i className="bi bi-book me-2"></i>Academic Info
              </button>
              <button 
                className={`list-group-item list-group-item-action ${activeTab === 'family' ? 'active' : ''}`}
                onClick={() => setActiveTab('family')}
              >
                <i className="bi bi-people me-2"></i>Family Info
              </button>
              <button 
                className={`list-group-item list-group-item-action ${activeTab === 'achievements' ? 'active' : ''}`}
                onClick={() => setActiveTab('achievements')}
              >
                <i className="bi bi-trophy me-2"></i>Achievements
              </button>
            </div>
          </Card>
        </div>

        <div className="col-lg-9">
          {activeTab === 'personal' && (
            <Card title="Personal Information" icon="person-badge">
              {editing ? (
                <form onSubmit={handleSubmit}>
                  <div className="row g-3">
                    <div className="col-md-6">
                      <label className="form-label">Full Name</label>
                      <input type="text" className="form-control" name="name" value={formData.name || ''} onChange={handleChange} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Email</label>
                      <input type="email" className="form-control" name="email" value={formData.email || ''} onChange={handleChange} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Phone</label>
                      <input type="text" className="form-control" name="phone" value={formData.phone || ''} onChange={handleChange} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Date of Birth</label>
                      <input type="date" className="form-control" name="date_of_birth" value={formData.date_of_birth || ''} onChange={handleChange} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Gender</label>
                      <select className="form-select" name="gender" value={formData.gender || ''} onChange={handleChange}>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Emergency Contact</label>
                      <input type="text" className="form-control" name="emergency_contact" value={formData.emergency_contact || ''} onChange={handleChange} />
                    </div>
                    <div className="col-12">
                      <label className="form-label">Address</label>
                      <textarea className="form-control" name="address" rows="3" value={formData.address || ''} onChange={handleChange}></textarea>
                    </div>
                    <div className="col-12">
                      <button type="submit" className="btn btn-primary">Save Changes</button>
                    </div>
                  </div>
                </form>
              ) : (
                <div className="row g-3">
                  <div className="col-md-6">
                    <div className="info-box">
                      <small className="text-muted">Full Name</small>
                      <div className="fw-bold">{profile?.name}</div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="info-box">
                      <small className="text-muted">Email</small>
                      <div className="fw-bold">{profile?.email}</div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="info-box">
                      <small className="text-muted">Phone</small>
                      <div className="fw-bold">{profile?.phone}</div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="info-box">
                      <small className="text-muted">Date of Birth</small>
                      <div className="fw-bold">{profile?.date_of_birth}</div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="info-box">
                      <small className="text-muted">Gender</small>
                      <div className="fw-bold">{profile?.gender}</div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="info-box">
                      <small className="text-muted">Blood Group</small>
                      <div className="fw-bold">{profile?.blood_group}</div>
                    </div>
                  </div>
                  <div className="col-12">
                    <div className="info-box">
                      <small className="text-muted">Address</small>
                      <div className="fw-bold">{profile?.address}</div>
                    </div>
                  </div>
                </div>
              )}
            </Card>
          )}

          {activeTab === 'academic' && (
            <Card title="Academic Information" icon="graduation-cap">
              <div className="row g-3">
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Student ID</small>
                    <div className="fw-bold">{profile?.id}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Class / Grade</small>
                    <div className="fw-bold">{profile?.class_name}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Roll Number</small>
                    <div className="fw-bold">{profile?.roll_number}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Section</small>
                    <div className="fw-bold">{profile?.section}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Session</small>
                    <div className="fw-bold">{profile?.session}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Attendance</small>
                    <div className="fw-bold">{profile?.attendance}%</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Admission Date</small>
                    <div className="fw-bold">{profile?.admission_date}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Hostel Status</small>
                    <div className="fw-bold">{profile?.hostel}</div>
                  </div>
                </div>
                <div className="col-12">
                  <div className="info-box">
                    <small className="text-muted">Enrolled Subjects</small>
                    <div className="d-flex flex-wrap gap-2 mt-2">
                      {profile?.subjects?.map((subject, idx) => (
                        <Badge key={idx} variant="primary">{subject}</Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {activeTab === 'family' && (
            <Card title="Family Information" icon="people">
              <div className="row g-3">
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Father's Name</small>
                    <div className="fw-bold">{profile?.father_name}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Mother's Name</small>
                    <div className="fw-bold">{profile?.mother_name}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Parent Phone</small>
                    <div className="fw-bold">{profile?.parent_phone}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="info-box">
                    <small className="text-muted">Emergency Contact</small>
                    <div className="fw-bold">{profile?.emergency_contact}</div>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {activeTab === 'achievements' && (
            <Card title="Achievements & Awards" icon="trophy">
              <div className="achievements-list">
                {profile?.achievements?.map((achievement, idx) => (
                  <div key={idx} className="achievement-item d-flex align-items-center p-3 mb-2 bg-light rounded">
                    <div className="icon-box bg-warning bg-opacity-10 rounded p-2 me-3">
                      <i className="bi bi-trophy text-warning"></i>
                    </div>
                    <div className="flex-grow-1">
                      <div className="fw-bold">{achievement}</div>
                      <small className="text-muted">Academic Year 2023-2024</small>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default StudentProfile;
