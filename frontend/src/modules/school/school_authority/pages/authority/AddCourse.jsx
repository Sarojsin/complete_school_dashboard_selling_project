import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createCourse } from '../../api/authority';
import './AddEdit.css';

const AddCourse = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    department: '',
    class_name: '',
    teacher_id: '',
    credits: '',
    description: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createCourse(formData);
      navigate('/authority/courses');
    } catch (err) {
      console.error('Failed to create course:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-edit-page">
      <div className="page-header">
        <h1>Add New Course</h1>
      </div>

      <form onSubmit={handleSubmit} className="add-form">
        <div className="form-section">
          <h2>Course Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Course Name *</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Course Code *</label>
              <input type="text" name="code" value={formData.code} onChange={handleChange} required placeholder="e.g., ENG101" />
            </div>
            <div className="form-group">
              <label>Department *</label>
              <select name="department" value={formData.department} onChange={handleChange} required>
                <option value="">Select Department</option>
                <option value="Science">Science</option>
                <option value="Mathematics">Mathematics</option>
                <option value="English">English</option>
                <option value="History">History</option>
              </select>
            </div>
            <div className="form-group">
              <label>Class *</label>
              <select name="class_name" value={formData.class_name} onChange={handleChange} required>
                <option value="">Select Class</option>
                <option value="1">Class 1</option>
                <option value="2">Class 2</option>
                <option value="3">Class 3</option>
                <option value="4">Class 4</option>
                <option value="5">Class 5</option>
                <option value="6">Class 6</option>
                <option value="7">Class 7</option>
                <option value="8">Class 8</option>
                <option value="9">Class 9</option>
                <option value="10">Class 10</option>
                <option value="11">Class 11</option>
                <option value="12">Class 12</option>
              </select>
            </div>
            <div className="form-group">
              <label>Credits</label>
              <input type="number" name="credits" value={formData.credits} onChange={handleChange} min="1" max="10" />
            </div>
            <div className="form-group">
              <label>Assigned Teacher</label>
              <select name="teacher_id" value={formData.teacher_id} onChange={handleChange}>
                <option value="">Select Teacher</option>
                <option value="1">Teacher 1</option>
                <option value="2">Teacher 2</option>
              </select>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Description</h2>
          <div className="form-group">
            <textarea 
              name="description" 
              value={formData.description} 
              onChange={handleChange} 
              rows="4"
              placeholder="Course description..."
            ></textarea>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={() => navigate('/authority/courses')}>Cancel</button>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Creating...' : 'Create Course'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddCourse;
