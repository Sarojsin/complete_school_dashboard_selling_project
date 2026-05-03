import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getStudent } from '../../api/authority';
import './AuthorityDetail.css';

const AuthorityStudentDetail = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('info');

  useEffect(() => {
    loadStudent();
  }, [studentId]);

  const loadStudent = async () => {
    try {
      const response = await getStudent(studentId);
      setStudent(response.data);
    } catch (err) {
      console.error('Failed to load student:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="detail-loading">Loading student details...</div>;
  }

  if (!student) {
    return <div className="detail-loading">Student not found</div>;
  }

  return (
    <div className="authority-detail-page">
      <div className="detail-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <div className="header-content">
          <div className="avatar-large">
            {student.name?.charAt(0).toUpperCase() || 'S'}
          </div>
          <div className="header-info">
            <h1>{student.name}</h1>
            <p>Student ID: {student.id}</p>
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
          className={`tab ${activeTab === 'academic' ? 'active' : ''}`}
          onClick={() => setActiveTab('academic')}
        >
          Academic
        </button>
        <button 
          className={`tab ${activeTab === 'fees' ? 'active' : ''}`}
          onClick={() => setActiveTab('fees')}
        >
          Fees
        </button>
        <button 
          className={`tab ${activeTab === 'attendance' ? 'active' : ''}`}
          onClick={() => setActiveTab('attendance')}
        >
          Attendance
        </button>
      </div>

      {activeTab === 'info' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Personal Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Full Name</label>
                <span>{student.name}</span>
              </div>
              <div className="info-item">
                <label>Email</label>
                <span>{student.email || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Phone</label>
                <span>{student.phone || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Date of Birth</label>
                <span>{student.date_of_birth || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Address</label>
                <span>{student.address || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Gender</label>
                <span>{student.gender || 'N/A'}</span>
              </div>
            </div>
          </div>

          <div className="info-section">
            <h3>Parent/Guardian Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Parent Name</label>
                <span>{student.parent_name || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Parent Phone</label>
                <span>{student.parent_phone || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Parent Email</label>
                <span>{student.parent_email || 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'academic' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Academic Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Grade/Class</label>
                <span>{student.grade || student.class || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Section</label>
                <span>{student.section || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Roll Number</label>
                <span>{student.roll_number || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Academic Year</label>
                <span>{student.academic_year || 'N/A'}</span>
              </div>
            </div>
          </div>

          <div className="info-section">
            <h3>Enrolled Courses</h3>
            {student.courses && student.courses.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Course</th>
                    <th>Teacher</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {student.courses.map((course) => (
                    <tr key={course.id}>
                      <td>{course.name}</td>
                      <td>{course.teacher_name}</td>
                      <td><span className="status-badge active">Active</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-text">No courses enrolled</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'fees' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Fee History</h3>
            {student.fees && student.fees.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Amount</th>
                    <th>Due Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {student.fees.map((fee) => (
                    <tr key={fee.id}>
                      <td>{fee.type}</td>
                      <td>${fee.amount}</td>
                      <td>{fee.due_date}</td>
                      <td>
                        <span className={`status-badge ${fee.status}`}>
                          {fee.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-text">No fee records</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'attendance' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Attendance Summary</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-value">{student.attendance?.total || 0}</span>
                <span className="stat-label">Total Days</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{student.attendance?.present || 0}</span>
                <span className="stat-label">Present</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{student.attendance?.absent || 0}</span>
                <span className="stat-label">Absent</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{student.attendance?.percentage || 0}%</span>
                <span className="stat-label">Percentage</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuthorityStudentDetail;
