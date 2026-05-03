import { useState, useEffect } from 'react';
import { getTeacherCourses, getAttendanceSessions, createAttendanceSession } from '../api/teachers';
import './TeacherPortal.css';

const TeacherAttendance = () => {
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    course_id: '',
    date: '',
    start_time: '',
    end_time: '',
    notes: ''
  });

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await getTeacherCourses();
      setCourses(response.data || response);
    } catch (err) {
      console.error('Failed to load courses:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSessions = async (courseId) => {
    setSelectedCourse(courseId);
    try {
      const response = await getAttendanceSessions(courseId);
      setSessions(response.data || response);
    } catch (err) {
      console.error('Failed to load sessions:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createAttendanceSession(formData);
      setShowForm(false);
      setFormData({ course_id: '', date: '', start_time: '', end_time: '', notes: '' });
      if (selectedCourse) loadSessions(selectedCourse);
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  if (loading) {
    return <div className="teacher-loading">Loading attendance...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <div>
          <h1>Attendance Management</h1>
          <p>Track and manage student attendance</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Session'}
        </button>
      </div>

      <div className="teacher-tabs">
        {courses.map((course) => (
          <button
            key={course.id}
            className={`teacher-tab ${selectedCourse === course.id ? 'active' : ''}`}
            onClick={() => loadSessions(course.id)}
          >
            {course.name}
          </button>
        ))}
      </div>

      {showForm && (
        <div className="teacher-card">
          <h3>Create Attendance Session</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Course</label>
                <select
                  value={formData.course_id}
                  onChange={(e) => setFormData({...formData, course_id: e.target.value})}
                  required
                >
                  <option value="">Select Course</option>
                  {courses.map((c) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Date</label>
                <input
                  type="date"
                  value={formData.date}
                  onChange={(e) => setFormData({...formData, date: e.target.value})}
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Start Time</label>
                <input
                  type="time"
                  value={formData.start_time}
                  onChange={(e) => setFormData({...formData, start_time: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>End Time</label>
                <input
                  type="time"
                  value={formData.end_time}
                  onChange={(e) => setFormData({...formData, end_time: e.target.value})}
                  required
                />
              </div>
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows={2}
              />
            </div>
            <button type="submit" className="btn-success">Create Session</button>
          </form>
        </div>
      )}

      <div className="teacher-card">
        <h3>Attendance Sessions</h3>
        {sessions.length > 0 ? (
          <table className="teacher-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Total Students</th>
                <th>Present</th>
                <th>Absent</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map((session) => (
                <tr key={session.id}>
                  <td>{session.date}</td>
                  <td>{session.start_time} - {session.end_time}</td>
                  <td>{session.total_students || 0}</td>
                  <td>{session.present || 0}</td>
                  <td>{session.absent || 0}</td>
                  <td>
                    <button className="action-btn">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📅</span>
            <p>No attendance sessions found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherAttendance;
