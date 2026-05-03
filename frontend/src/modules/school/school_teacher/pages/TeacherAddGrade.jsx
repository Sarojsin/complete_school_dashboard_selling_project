import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTeacherCourses } from '../api/teachers';

const TeacherAddGrade = () => {
  const { courseId, studentId } = useParams();
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(courseId || '');
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(studentId || '');
  const [grade, setGrade] = useState('');
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadCourses();
  }, []);

  useEffect(() => {
    if (selectedCourse) {
      loadStudents(selectedCourse);
    }
  }, [selectedCourse]);

  const loadCourses = async () => {
    try {
      const data = await getTeacherCourses();
      setCourses(data);
    } catch (err) {
      setError('Failed to load courses');
    }
  };

  const loadStudents = async (courseId) => {
    try {
      const response = await fetch(`/api/teacher/courses/${courseId}/students`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setStudents(data);
    } catch (err) {
      setError('Failed to load students');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('/api/teacher/grades', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          student_id: selectedStudent,
          course_id: selectedCourse,
          grade: grade,
          comment: comment
        })
      });

      if (response.ok) {
        setSuccess('Grade added successfully!');
        setTimeout(() => navigate('/teacher/grades'), 1500);
      } else {
        setError('Failed to add grade');
      }
    } catch (err) {
      setError('An error occurred while adding grade');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="teacher-add-grade-container">
      <div className="page-header">
        <h1>Add Grade</h1>
        <button onClick={() => navigate('/teacher/grades')} className="back-btn">
          ← Back to Grades
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleSubmit} className="grade-form">
        <div className="form-group">
          <label htmlFor="course">Course *</label>
          <select
            id="course"
            value={selectedCourse}
            onChange={(e) => setSelectedCourse(e.target.value)}
            required
          >
            <option value="">Select Course</option>
            {courses.map(course => (
              <option key={course.id} value={course.id}>
                {course.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="student">Student *</label>
          <select
            id="student"
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            required
            disabled={!selectedCourse}
          >
            <option value="">Select Student</option>
            {students.map(student => (
              <option key={student.id} value={student.id}>
                {student.name} ({student.email})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="grade">Grade *</label>
          <input
            type="text"
            id="grade"
            value={grade}
            onChange={(e) => setGrade(e.target.value)}
            placeholder="Enter grade (e.g., A, B+, 85)"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="comment">Comment</label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Optional comment about the grade"
            rows="4"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Adding Grade...' : 'Add Grade'}
          </button>
          <button 
            type="button" 
            className="btn-secondary"
            onClick={() => navigate('/teacher/grades')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default TeacherAddGrade;
