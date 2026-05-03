import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const TeacherEditAssignment = () => {
  const { assignmentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [assignment, setAssignment] = useState({
    title: '',
    description: '',
    course_id: '',
    due_date: '',
    total_marks: '',
    instructions: ''
  });
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    loadAssignment();
    loadCourses();
  }, [assignmentId]);

  const loadAssignment = async () => {
    try {
      const response = await fetch(`/api/teacher/assignments/${assignmentId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setAssignment({
        ...data,
        due_date: data.due_date ? data.due_date.split('T')[0] : ''
      });
      setLoading(false);
    } catch (err) {
      setError('Failed to load assignment');
      setLoading(false);
    }
  };

  const loadCourses = async () => {
    try {
      const response = await fetch('/api/teacher/courses', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setCourses(data);
    } catch (err) {
      console.error('Failed to load courses');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAssignment(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`/api/teacher/assignments/${assignmentId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(assignment)
      });

      if (response.ok) {
        setSuccess('Assignment updated successfully!');
        setTimeout(() => navigate('/teacher/assignments'), 1500);
      } else {
        setError('Failed to update assignment');
      }
    } catch (err) {
      setError('An error occurred while updating the assignment');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading assignment...</div>;
  }

  return (
    <div className="teacher-edit-assignment-container">
      <div className="page-header">
        <h1>Edit Assignment</h1>
        <button onClick={() => navigate('/teacher/assignments')} className="back-btn">
          ← Back to Assignments
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleSubmit} className="assignment-form">
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={assignment.title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="course_id">Course *</label>
          <select
            id="course_id"
            name="course_id"
            value={assignment.course_id}
            onChange={handleChange}
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
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={assignment.description}
            onChange={handleChange}
            rows="4"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="due_date">Due Date *</label>
            <input
              type="date"
              id="due_date"
              name="due_date"
              value={assignment.due_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="total_marks">Total Marks *</label>
            <input
              type="number"
              id="total_marks"
              name="total_marks"
              value={assignment.total_marks}
              onChange={handleChange}
              min="0"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="instructions">Instructions</label>
          <textarea
            id="instructions"
            name="instructions"
            value={assignment.instructions}
            onChange={handleChange}
            rows="6"
            placeholder="Detailed instructions for the assignment"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
          <button 
            type="button" 
            className="btn-secondary"
            onClick={() => navigate('/teacher/assignments')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default TeacherEditAssignment;
