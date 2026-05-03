import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTeacherCourses, createTest } from '../api/teachers';
import './TeacherPortal.css';

const TeacherCreateTest = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_id: '',
    test_date: '',
    start_time: '',
    end_time: '',
    total_marks: 100,
    passing_marks: 40,
    instructions: '',
    is_active: true
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
    }
  };

  const handleChange = (field, value) => {
    setFormData({...formData, [field]: value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createTest(formData);
      alert('Test created successfully!');
      navigate('/teacher/tests');
    } catch (err) {
      console.error('Failed to create:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="teacher-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1>Create Test/Quiz</h1>
        <p>Create a new test or quiz for your students</p>
      </div>

      <div className="teacher-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Test Title</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="Enter test title"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Course</label>
              <select
                value={formData.course_id}
                onChange={(e) => handleChange('course_id', e.target.value)}
                required
              >
                <option value="">Select Course</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>{course.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Test Date</label>
              <input
                type="date"
                value={formData.test_date}
                onChange={(e) => handleChange('test_date', e.target.value)}
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
                onChange={(e) => handleChange('start_time', e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>End Time</label>
              <input
                type="time"
                value={formData.end_time}
                onChange={(e) => handleChange('end_time', e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Total Marks</label>
              <input
                type="number"
                value={formData.total_marks}
                onChange={(e) => handleChange('total_marks', e.target.value)}
                min="1"
              />
            </div>
            <div className="form-group">
              <label>Passing Marks</label>
              <input
                type="number"
                value={formData.passing_marks}
                onChange={(e) => handleChange('passing_marks', e.target.value)}
                min="1"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              rows={3}
            />
          </div>

          <div className="form-group">
            <label>Instructions</label>
            <textarea
              value={formData.instructions}
              onChange={(e) => handleChange('instructions', e.target.value)}
              rows={3}
              placeholder="Instructions for students"
            />
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => handleChange('is_active', e.target.checked)}
              />
              <span>Active (Students can take test)</span>
            </label>
          </div>

          <div className="action-btns">
            <button type="button" className="btn-secondary" onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button type="submit" className="btn-success" disabled={loading}>
              {loading ? 'Creating...' : 'Create Test'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TeacherCreateTest;
