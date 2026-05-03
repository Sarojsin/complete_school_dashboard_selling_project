import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getCourse } from '../../api/authority';
import './AuthorityDetail.css';

const AuthorityCourseDetail = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('info');

  useEffect(() => {
    loadCourse();
  }, [courseId]);

  const loadCourse = async () => {
    try {
      const response = await getCourse(courseId);
      setCourse(response.data);
    } catch (err) {
      console.error('Failed to load course:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="detail-loading">Loading course details...</div>;
  }

  if (!course) {
    return <div className="detail-loading">Course not found</div>;
  }

  return (
    <div className="authority-detail-page">
      <div className="detail-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <div className="header-content">
          <div className="avatar-large" style={{background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'}}>
            📚
          </div>
          <div className="header-info">
            <h1>{course.name}</h1>
            <p>Course Code: {course.code}</p>
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
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'students' ? 'active' : ''}`}
          onClick={() => setActiveTab('students')}
        >
          Students
        </button>
        <button 
          className={`tab ${activeTab === 'content' ? 'active' : ''}`}
          onClick={() => setActiveTab('content')}
        >
          Content
        </button>
        <button 
          className={`tab ${activeTab === 'schedule' ? 'active' : ''}`}
          onClick={() => setActiveTab('schedule')}
        >
          Schedule
        </button>
      </div>

      {activeTab === 'info' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Course Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Course Name</label>
                <span>{course.name}</span>
              </div>
              <div className="info-item">
                <label>Course Code</label>
                <span>{course.code}</span>
              </div>
              <div className="info-item">
                <label>Grade/Class</label>
                <span>{course.grade || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Teacher</label>
                <span>{course.teacher_name || 'Not Assigned'}</span>
              </div>
              <div className="info-item">
                <label>Credits</label>
                <span>{course.credits || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Academic Year</label>
                <span>{course.academic_year || 'N/A'}</span>
              </div>
            </div>
          </div>

          <div className="info-section">
            <h3>Description</h3>
            <p>{course.description || 'No description available'}</p>
          </div>

          <div className="info-section">
            <h3>Course Stats</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-value">{course.enrolled_students || 0}</span>
                <span className="stat-label">Enrolled</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{course.assignments || 0}</span>
                <span className="stat-label">Assignments</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{course.tests || 0}</span>
                <span className="stat-label">Tests</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{course.resources || 0}</span>
                <span className="stat-label">Resources</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'students' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Enrolled Students</h3>
            {course.students && course.students.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Roll Number</th>
                    <th>Email</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {course.students.map((student) => (
                    <tr key={student.id}>
                      <td>{student.name}</td>
                      <td>{student.roll_number}</td>
                      <td>{student.email}</td>
                      <td><span className="status-badge active">Active</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-text">No students enrolled</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'content' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Course Content</h3>
            {course.syllabus && course.syllabus.length > 0 ? (
              <div className="syllabus-list">
                {course.syllabus.map((item, index) => (
                  <div key={index} className="syllabus-item">
                    <span className="week-number">Week {item.week}</span>
                    <span className="topic-name">{item.topic}</span>
                    <span className={`status-badge ${item.completed ? 'active' : 'pending'}`}>
                      {item.completed ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-text">No syllabus content</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'schedule' && (
        <div className="detail-content">
          <div className="info-section">
            <h3>Class Schedule</h3>
            {course.schedule && course.schedule.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Day</th>
                    <th>Time</th>
                    <th>Room</th>
                    <th>Duration</th>
                  </tr>
                </thead>
                <tbody>
                  {course.schedule.map((slot, index) => (
                    <tr key={index}>
                      <td>{slot.day}</td>
                      <td>{slot.start_time} - {slot.end_time}</td>
                      <td>{slot.room || 'TBD'}</td>
                      <td>{slot.duration || '1 hour'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-text">No schedule set</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AuthorityCourseDetail;
