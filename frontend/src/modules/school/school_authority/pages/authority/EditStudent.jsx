import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getStudent, updateStudent } from '../../api/authority';
import './AddEdit.css';

const AuthorityEditStudent = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    address: '',
    grade: '',
    section: '',
    roll_number: '',
    parent_name: '',
    parent_phone: '',
    parent_email: ''
  });

  useEffect(() => {
    loadStudent();
  }, [studentId]);

  const loadStudent = async () => {
    try {
      const response = await getStudent(studentId);
      setFormData(response.data);
    } catch (err) {
      console.error('Failed to load student:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateStudent(studentId, formData);
      navigate('/authority/students');
    } catch (err) {
      console.error('Failed to update student:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="edit-loading">Loading student...</div>;
  }

  return (
    <div className="authority-edit-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1>Edit Student</h1>
      </div>

      <div className="edit-form-card">
        <h3>Personal Information</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Phone</label>
              <input
                type="text"
                value={formData.phone}
                onChange={(e) => setFormData({...formData, phone: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Date of Birth</label>
              <input
                type="date"
                value={formData.date_of_birth}
                onChange={(e) => setFormData({...formData, date_of_birth: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Gender</label>
              <select
                value={formData.gender}
                onChange={(e) => setFormData({...formData, gender: e.target.value})}
              >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="form-group">
              <label>Address</label>
              <input
                type="text"
                value={formData.address}
                onChange={(e) => setFormData({...formData, address: e.target.value})}
              />
            </div>
          </div>

          <h3>Academic Information</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Grade/Class</label>
              <input
                type="text"
                value={formData.grade}
                onChange={(e) => setFormData({...formData, grade: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Section</label>
              <input
                type="text"
                value={formData.section}
                onChange={(e) => setFormData({...formData, section: e.target.value})}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Roll Number</label>
            <input
              type="text"
              value={formData.roll_number}
              onChange={(e) => setFormData({...formData, roll_number: e.target.value})}
            />
          </div>

          <h3>Parent/Guardian Information</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Parent Name</label>
              <input
                type="text"
                value={formData.parent_name}
                onChange={(e) => setFormData({...formData, parent_name: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Parent Phone</label>
              <input
                type="text"
                value={formData.parent_phone}
                onChange={(e) => setFormData({...formData, parent_phone: e.target.value})}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Parent Email</label>
            <input
              type="email"
              value={formData.parent_email}
              onChange={(e) => setFormData({...formData, parent_email: e.target.value})}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-cancel" onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button type="submit" className="btn-submit" disabled={saving}>
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AuthorityEditStudent;
