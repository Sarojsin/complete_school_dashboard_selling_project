import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTeacher } from '../../api/authority';
import './AddEdit.css';

const AddTeacher = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    department: '',
    subject: '',
    qualification: '',
    experience: '',
    address: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createTeacher(formData);
      navigate('/authority/teachers');
    } catch (err) {
      console.error('Failed to create teacher:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-edit-page">
      <div className="page-header">
        <h1>Add New Teacher</h1>
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
            <div className="form-group">
              <label>Address</label>
              <input type="text" name="address" value={formData.address} onChange={handleChange} />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Professional Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Department *</label>
              <select name="department" value={formData.department} onChange={handleChange} required>
                <option value="">Select Department</option>
                <option value="Science">Science</option>
                <option value="Mathematics">Mathematics</option>
                <option value="English">English</option>
                <option value="History">History</option>
                <option value="Geography">Geography</option>
                <option value="Physics">Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Biology">Biology</option>
              </select>
            </div>
            <div className="form-group">
              <label>Subject *</label>
              <input type="text" name="subject" value={formData.subject} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Qualification</label>
              <input type="text" name="qualification" value={formData.qualification} onChange={handleChange} placeholder="B.Ed, M.Sc..." />
            </div>
            <div className="form-group">
              <label>Experience (years)</label>
              <input type="number" name="experience" value={formData.experience} onChange={handleChange} min="0" />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={() => navigate('/authority/teachers')}>Cancel</button>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Creating...' : 'Create Teacher'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddTeacher;
