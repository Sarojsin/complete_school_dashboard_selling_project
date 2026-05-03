import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTeacherCourses, createAssignment } from '../api/teachers';
import './TeacherPortal.css';

const CreateAssignment = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_id: '',
    due_date: '',
    total_marks: 100,
    instructions: ''
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
      await createAssignment(formData);
      alert('Assignment created successfully!');
      navigate('/teacher/assignments');
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
        <h1>Create Assignment</h1>
        <p>Create a new assignment for your students</p>
      </div>

      <div className="teacher-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Assignment Title</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="Enter assignment title"
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
              <label>Due Date</label>
              <input
                type="datetime-local"
                value={formData.due_date}
                onChange={(e) => handleChange('due_date', e.target.value)}
                required
              />
            </div>
          </div>

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
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              rows={4}
              placeholder="Describe the assignment"
            />
          </div>

          <div className="form-group">
            <label>Instructions</label>
            <textarea
              value={formData.instructions}
              onChange={(e) => handleChange('instructions', e.target.value)}
              rows={4}
              placeholder="Additional instructions for students"
            />
          </div>

          <div className="action-btns">
            <button type="button" className="btn-secondary" onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button type="submit" className="btn-success" disabled={loading}>
              {loading ? 'Creating...' : 'Create Assignment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateAssignment;
