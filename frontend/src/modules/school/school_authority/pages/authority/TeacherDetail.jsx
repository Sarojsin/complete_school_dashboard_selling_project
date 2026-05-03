import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTeacher } from '../../api/authority';
import './AuthorityDetail.css';

const AuthorityTeacherDetail = () => {
  const { teacherId } = useParams();
  const navigate = useNavigate();
  const [teacher, setTeacher] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('info');

  useEffect(() => {
    loadTeacher();
  }, [teacherId]);

  const loadTeacher = async () => {
    try {
      const response = await getTeacher(teacherId);
      setTeacher(response.data);
    } catch (err) {
      console.error('Failed to load teacher:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="detail-loading">Loading teacher details...</div>;
  }

  if (!teacher) {
    return <div className="detail-loading">Teacher not found</div>;
  }

  return (
    <div className="authority-detail-page">
      <div className="detail-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <div className="header-content">
          <div className="avatar-large">
            {teacher.name?.charAt(0).toUpperCase() || 'T'}
          </div>
          <div className="header-info">
            <h1>{teacher.name}</h1>
            <p>Teacher ID: {teacher.id}</p>
            <span className="status-badge active">Active</span>
          </div>
          <div className="header-actions">
            <button className="btn-edit">Edit</button>
            <button className="btn-delete">Delete</button>
          </div>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'info' ? 'active' : ''}`}
          onClick={() => setActiveTab('info')}
        >
          Personal Info
        </button>
        <button 
          className={`tab ${activeTab === 'professional' ? 'active' : ''}`}
          onClick={() => setActiveTab('professional')}
        >
          Professional
        </button>
        <button 
          className={`tab ${activeTab === 'courses' ? 'active' : ''}`}
          onClick={() => setActiveTab('courses')}
        >
          Courses
        </button>
        <button 
          className={`tab ${activeTab === 'classes' ? 'active' : ''}`}
          onClick={() => setActiveTab('classes')}
        >
          Classes
        </button>
      </div>

      {activeTab === 'info' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Personal Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Full Name</label>
                <span>{teacher.name}</span>
              </div>
              <div className="info-item">
                <label>Email</label>
                <span>{teacher.email || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Phone</label>
                <span>{teacher.phone || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Date of Birth</label>
                <span>{teacher.date_of_birth || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Address</label>
                <span>{teacher.address || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Gender</label>
                <span>{teacher.gender || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Emergency Contact</label>
                <span>{teacher.emergency_contact || 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'professional' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Professional Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Employee ID</label>
                <span>{teacher.employee_id || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Department</label>
                <span>{teacher.department || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Designation</label>
                <span>{teacher.designation || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Qualification</label>
                <span>{teacher.qualification || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Experience (Years)</label>
                <span>{teacher.experience || 0}</span>
              </div>
              <div className="info-item">
                <label>Join Date</label>
                <span>{teacher.join_date || 'N/A'}</span>
              </div>
            </div>
          </div>

          <div className="info-section">
            <h3>Skills & Specializations</h3>
            <div className="skills-list">
              {teacher.skills && teacher.skills.length > 0 ? (
                teacher.skills.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                ))
              ) : (
                <p className="empty-text">No skills listed</p>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'courses' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Assigned Courses</h3>
            {teacher.courses && teacher.courses.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Course Name</th>
                    <th>Grade</th>
                    <th>Students</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {teacher.courses.map((course) => (
                    <tr key={course.id}>
                      <td>{course.name}</td>
                      <td>{course.grade}</td>
                      <td>{course.student_count || 0}</td>
                      <td><span className="status-badge active">Active</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-text">No courses assigned</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'classes' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Teaching Schedule</h3>
            {teacher.classes && teacher.classes.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Class</th>
                    <th>Subject</th>
                    <th>Day</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  {teacher.classes.map((cls, index) => (
                    <tr key={index}>
                      <td>{cls.class_name}</td>
                      <td>{cls.subject}</td>
                      <td>{cls.day}</td>
                      <td>{cls.time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-text">No class schedule</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AuthorityTeacherDetail;
