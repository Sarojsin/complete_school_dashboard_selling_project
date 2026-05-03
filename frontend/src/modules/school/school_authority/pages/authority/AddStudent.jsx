import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createStudent } from '../../api/authority';
import './AddEdit.css';

const AddStudent = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    class_name: '',
    section: '',
    roll_number: '',
    father_name: '',
    mother_name: '',
    parent_phone: '',
    address: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createStudent(formData);
      navigate('/authority/students');
    } catch (err) {
      console.error('Failed to create student:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-edit-page">
      <div className="page-header">
        <h1>Add New Student</h1>
      </div>

      <form onSubmit={handleSubmit} className="add-form">
        <div className="form-section">
          <h2>Personal Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Full Name *</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Email *</label>
              <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input type="text" name="phone" value={formData.phone} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Date of Birth</label>
              <input type="date" name="date_of_birth" value={formData.date_of_birth} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Gender</label>
              <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Academic Information</h2>
          <div className="form-grid">
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
              <label>Section</label>
              <input type="text" name="section" value={formData.section} onChange={handleChange} placeholder="A, B, C..." />
            </div>
            <div className="form-group">
              <label>Roll Number *</label>
              <input type="text" name="roll_number" value={formData.roll_number} onChange={handleChange} required />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Parent/Guardian Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Father's Name</label>
              <input type="text" name="father_name" value={formData.father_name} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Mother's Name</label>
              <input type="text" name="mother_name" value={formData.mother_name} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Parent Phone</label>
              <input type="text" name="parent_phone" value={formData.parent_phone} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Address</label>
              <input type="text" name="address" value={formData.address} onChange={handleChange} />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={() => navigate('/authority/students')}>Cancel</button>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Creating...' : 'Create Student'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddStudent;
