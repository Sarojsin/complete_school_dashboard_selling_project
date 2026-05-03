import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getCourse, updateCourse } from '../../api/authority';
import './AddEdit.css';

const AuthorityEditCourse = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    grade: '',
    credits: '',
    teacher_id: '',
    academic_year: new Date().getFullYear().toString()
  });

  useEffect(() => {
    loadCourse();
  }, [courseId]);

  const loadCourse = async () => {
    try {
      const response = await getCourse(courseId);
      setFormData(response.data);
    } catch (err) {
      console.error('Failed to load course:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateCourse(courseId, formData);
      navigate('/authority/courses');
    } catch (err) {
      console.error('Failed to update course:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="edit-loading">Loading course...</div>;
  }

  return (
    <div className="authority-edit-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1>Edit Course</h1>
      </div>

      <div className="edit-form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Course Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Course Code</label>
              <input
                type="text"
                value={formData.code}
                onChange={(e) => setFormData({...formData, code: e.target.value})}
                required
              />
            </div>
          </div>

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
              <label>Credits</label>
              <input
                type="number"
                value={formData.credits}
                onChange={(e) => setFormData({...formData, credits: e.target.value})}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows={4}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Assigned Teacher ID</label>
              <input
                type="text"
                value={formData.teacher_id}
                onChange={(e) => setFormData({...formData, teacher_id: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Academic Year</label>
              <input
                type="text"
                value={formData.academic_year}
                onChange={(e) => setFormData({...formData, academic_year: e.target.value})}
              />
            </div>
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

export default AuthorityEditCourse;
