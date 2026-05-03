import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const TeacherCourseDetail = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [students, setStudents] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [tests, setTests] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadCourseDetails();
  }, [courseId]);

  const loadCourseDetails = async () => {
    setLoading(true);
    try {
      const [courseRes, studentsRes, assignmentsRes, testsRes] = await Promise.all([
        fetch(`/api/teacher/courses/${courseId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }),
        fetch(`/api/teacher/courses/${courseId}/students`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }),
        fetch(`/api/teacher/courses/${courseId}/assignments`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }),
        fetch(`/api/teacher/courses/${courseId}/tests`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
      ]);

      const courseData = await courseRes.json();
      const studentsData = await studentsRes.json();
      const assignmentsData = await assignmentsRes.json();
      const testsData = await testsRes.json();

      setCourse(courseData);
      setStudents(studentsData);
      setAssignments(assignmentsData);
      setTests(testsData);
      setLoading(false);
    } catch (err) {
      setError('Failed to load course details');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading course details...</div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  return (
    <div className="teacher-course-detail-container">
      <div className="page-header">
        <h1>{course.name}</h1>
        <button onClick={() => navigate('/teacher/courses')} className="back-btn">
          ← Back to Courses
        </button>
      </div>

      <div className="course-header-info">
        <div className="info-card">
          <span className="label">Course Code</span>
          <span className="value">{course.code}</span>
        </div>
        <div className="info-card">
          <span className="label">Credits</span>
          <span className="value">{course.credits}</span>
        </div>
        <div className="info-card">
          <span className="label">Students Enrolled</span>
          <span className="value">{students.length}</span>
        </div>
        <div className="info-card">
          <span className="label">Assignments</span>
          <span className="value">{assignments.length}</span>
        </div>
        <div className="info-card">
          <span className="label">Tests</span>
          <span className="value">{tests.length}</span>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'students' ? 'active' : ''}`}
          onClick={() => setActiveTab('students')}
        >
          Students ({students.length})
        </button>
        <button 
          className={`tab ${activeTab === 'assignments' ? 'active' : ''}`}
          onClick={() => setActiveTab('assignments')}
        >
          Assignments ({assignments.length})
        </button>
        <button 
          className={`tab ${activeTab === 'tests' ? 'active' : ''}`}
          onClick={() => setActiveTab('tests')}
        >
          Tests ({tests.length})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="section">
              <h3>Course Description</h3>
              <p>{course.description || 'No description available.'}</p>
            </div>
            
            <div className="section">
              <h3>Quick Actions</h3>
              <div className="action-buttons">
                <button onClick={() => navigate(`/teacher/take-attendance/${courseId}`)} className="btn-action">
                  Take Attendance
                </button>
                <button onClick={() => navigate(`/teacher/add-grade/${courseId}`)} className="btn-action">
                  Add Grade
                </button>
                <button onClick={() => navigate(`/teacher/create-assignment?course=${courseId}`)} className="btn-action">
                  Create Assignment
                </button>
                <button onClick={() => navigate(`/teacher/create-test?course=${courseId}`)} className="btn-action">
                  Create Test
                </button>
              </div>
            </div>

            <div className="section">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                {assignments.slice(0, 3).map(assignment => (
                  <div key={assignment.id} className="activity-item">
                    <span className="activity-type">Assignment</span>
                    <span className="activity-title">{assignment.title}</span>
                    <span className="activity-date">{new Date(assignment.created_at).toLocaleDateString()}</span>
                  </div>
                ))}
                {tests.slice(0, 3).map(test => (
                  <div key={test.id} className="activity-item">
                    <span className="activity-type">Test</span>
                    <span className="activity-title">{test.title}</span>
                    <span className="activity-date">{new Date(test.created_at).toLocaleDateString()}</span>
                  </div>
                ))}
                {assignments.length === 0 && tests.length === 0 && (
                  <p className="no-activity">No recent activity</p>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'students' && (
          <div className="students-tab">
            <div className="section-header">
              <h3>Enrolled Students</h3>
              <button onClick={() => navigate(`/teacher/add-grade/${courseId}`)} className="btn-primary">
                Add Grade
              </button>
            </div>
            {students.length === 0 ? (
              <p className="no-data">No students enrolled in this course.</p>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Enrollment Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map(student => (
                    <tr key={student.id}>
                      <td>{student.name}</td>
                      <td>{student.email}</td>
                      <td>{student.enrollment_date ? new Date(student.enrollment_date).toLocaleDateString() : '-'}</td>
                      <td>
                        <button 
                          onClick={() => navigate(`/teacher/student/${student.id}`)}
                          className="btn-link"
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'assignments' && (
          <div className="assignments-tab">
            <div className="section-header">
              <h3>Course Assignments</h3>
              <button onClick={() => navigate(`/teacher/create-assignment?course=${courseId}`)} className="btn-primary">
                + New Assignment
              </button>
            </div>
            {assignments.length === 0 ? (
              <p className="no-data">No assignments created yet.</p>
            ) : (
              <div className="items-grid">
                {assignments.map(assignment => (
                  <div key={assignment.id} className="item-card">
                    <h4>{assignment.title}</h4>
                    <p>{assignment.description}</p>
                    <div className="item-meta">
                      <span>Due: {new Date(assignment.due_date).toLocaleDateString()}</span>
                      <span>Marks: {assignment.total_marks}</span>
                    </div>
                    <div className="item-actions">
                      <button 
                        onClick={() => navigate(`/teacher/assignments/${assignment.id}`)}
                        className="btn-view"
                      >
                        View
                      </button>
                      <button 
                        onClick={() => navigate(`/teacher/edit-assignment/${assignment.id}`)}
                        className="btn-edit"
                      >
                        Edit
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'tests' && (
          <div className="tests-tab">
            <div className="section-header">
              <h3>Course Tests</h3>
              <button onClick={() => navigate(`/teacher/create-test?course=${courseId}`)} className="btn-primary">
                + New Test
              </button>
            </div>
            {tests.length === 0 ? (
              <p className="no-data">No tests created yet.</p>
            ) : (
              <div className="items-grid">
                {tests.map(test => (
                  <div key={test.id} className="item-card">
                    <h4>{test.title}</h4>
                    <p>{test.description}</p>
                    <div className="item-meta">
                      <span>Date: {new Date(test.test_date).toLocaleDateString()}</span>
                      <span>Marks: {test.total_marks}</span>
                      <span>Duration: {test.duration_minutes} min</span>
                    </div>
                    <div className="item-actions">
                      <button 
                        onClick={() => navigate(`/teacher/tests/${test.id}`)}
                        className="btn-view"
                      >
                        View
                      </button>
                      <button 
                        onClick={() => navigate(`/teacher/edit-test/${test.id}`)}
                        className="btn-edit"
                      >
                        Edit
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherCourseDetail;
