import { useState, useEffect } from 'react';
import { getTeacherCourses, getTeacherGrades, addGrade } from '../api/teachers';
import './TeacherPortal.css';

const TeacherGrades = () => {
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [grades, setGrades] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    course_id: '',
    grade: '',
    remarks: ''
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

  const loadGrades = async (courseId) => {
    setSelectedCourse(courseId);
    try {
      const response = await getTeacherGrades(courseId);
      setGrades(response.data || response);
    } catch (err) {
      console.error('Failed to load grades:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addGrade({...formData, course_id: selectedCourse});
      setShowForm(false);
      setFormData({ student_id: '', course_id: '', grade: '', remarks: '' });
      loadGrades(selectedCourse);
    } catch (err) {
      console.error('Failed to add grade:', err);
    }
  };

  if (loading) {
    return <div className="teacher-loading">Loading grades...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <div>
          <h1>Grades Management</h1>
          <p>Manage student grades for your courses</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Grade'}
        </button>
      </div>

      <div className="teacher-tabs">
        {courses.map((course) => (
          <button
            key={course.id}
            className={`teacher-tab ${selectedCourse === course.id ? 'active' : ''}`}
            onClick={() => loadGrades(course.id)}
          >
            {course.name}
          </button>
        ))}
      </div>

      {showForm && (
        <div className="teacher-card">
          <h3>Add New Grade</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Student ID</label>
                <input
                  type="text"
                  value={formData.student_id}
                  onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Grade</label>
                <input
                  type="text"
                  value={formData.grade}
                  onChange={(e) => setFormData({...formData, grade: e.target.value})}
                  placeholder="e.g., A, B+, 85"
                  required
                />
              </div>
            </div>
            <div className="form-group">
              <label>Remarks</label>
              <textarea
                value={formData.remarks}
                onChange={(e) => setFormData({...formData, remarks: e.target.value})}
                rows={3}
              />
            </div>
            <button type="submit" className="btn-success">Add Grade</button>
          </form>
        </div>
      )}

      <div className="teacher-card">
        <h3>{selectedCourse ? 'Grades' : 'Select a Course'}</h3>
        {selectedCourse ? (
          grades.length > 0 ? (
            <table className="teacher-table">
              <thead>
                <tr>
                  <th>Student Name</th>
                  <th>Student ID</th>
                  <th>Grade</th>
                  <th>Remarks</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {grades.map((grade) => (
                  <tr key={grade.id}>
                    <td>{grade.student_name}</td>
                    <td>{grade.student_id}</td>
                    <td>{grade.grade}</td>
                    <td>{grade.remarks || '-'}</td>
                    <td>{grade.created_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <span className="empty-icon">📝</span>
              <p>No grades added yet</p>
            </div>
          )
        ) : (
          <div className="empty-state">
            <span className="empty-icon">👈</span>
            <p>Select a course to view grades</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherGrades;
