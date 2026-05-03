import { useState, useEffect } from 'react';
import { getFeeStructures, createFeeStructure } from '../../api/authority';
import './AuthorityFees.css';

const AuthorityFeeStructure = () => {
  const [structures, setStructures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    amount: '',
    category: 'tuition',
    grade: '',
    academic_year: new Date().getFullYear().toString()
  });

  useEffect(() => {
    loadStructures();
  }, []);

  const loadStructures = async () => {
    try {
      const response = await getFeeStructures();
      setStructures(response.data);
    } catch (err) {
      console.error('Failed to load fee structures:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createFeeStructure(formData);
      setShowForm(false);
      setFormData({
        name: '',
        amount: '',
        category: 'tuition',
        grade: '',
        academic_year: new Date().getFullYear().toString()
      });
      loadStructures();
    } catch (err) {
      console.error('Failed to create fee structure:', err);
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      tuition: '📚',
      exam: '📝',
      transport: '🚌',
      hostel: '🏠',
      library: '📖',
      other: '💰'
    };
    return icons[category] || '💰';
  };

  if (loading) {
    return <div className="fees-loading">Loading fee structures...</div>;
  }

  return (
    <div className="authority-fees-page">
      <div className="page-header">
        <div>
          <h1>Fee Structure</h1>
          <p>Manage fee structures by category and grade</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Structure'}
        </button>
      </div>

      {showForm && (
        <div className="fee-form-card">
          <h3>Create New Fee Structure</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Structure Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  placeholder="e.g., Grade 10 Tuition Fee"
                  required
                />
              </div>
              <div className="form-group">
                <label>Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                >
                  <option value="tuition">Tuition</option>
                  <option value="exam">Exam Fee</option>
                  <option value="transport">Transport</option>
                  <option value="hostel">Hostel</option>
                  <option value="library">Library</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Amount</label>
                <input
                  type="number"
                  value={formData.amount}
                  onChange={(e) => setFormData({...formData, amount: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Grade/Class</label>
                <input
                  type="text"
                  value={formData.grade}
                  onChange={(e) => setFormData({...formData, grade: e.target.value})}
                  placeholder="e.g., Grade 10"
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Academic Year</label>
                <input
                  type="text"
                  value={formData.academic_year}
                  onChange={(e) => setFormData({...formData, academic_year: e.target.value})}
                />
              </div>
            </div>
            <button type="submit" className="btn-submit">Create Structure</button>
          </form>
        </div>
      )}

      <div className="structures-grid">
        {structures.length > 0 ? (
          structures.map((structure) => (
            <div key={structure.id} className="structure-card">
              <div className="structure-icon">
                {getCategoryIcon(structure.category)}
              </div>
              <div className="structure-info">
                <h4>{structure.name}</h4>
                <p className="category">{structure.category}</p>
                <p className="amount">${parseFloat(structure.amount || 0).toLocaleString()}</p>
                <p className="details">
                  {structure.grade && <span>Grade: {structure.grade}</span>}
                  {structure.academic_year && <span>Year: {structure.academic_year}</span>}
                </p>
              </div>
              <div className="structure-actions">
                <button className="btn-action">Edit</button>
                <button className="btn-action delete">Delete</button>
              </div>
            </div>
          ))
        ) : (
          <div className="empty-state" style={{gridColumn: '1 / -1'}}>
            <span className="empty-icon">📋</span>
            <p>No fee structures found</p>
          </div>
        )}
      </div>

      <div className="category-summary">
        <h3>Category Summary</h3>
        <div className="category-cards">
          <div className="category-card">
            <span className="cat-icon">📚</span>
            <span className="cat-name">Tuition</span>
            <span className="cat-count">{structures.filter(s => s.category === 'tuition').length} structures</span>
          </div>
          <div className="category-card">
            <span className="cat-icon">🚌</span>
            <span className="cat-name">Transport</span>
            <span className="cat-count">{structures.filter(s => s.category === 'transport').length} structures</span>
          </div>
          <div className="category-card">
            <span className="cat-icon">🏠</span>
            <span className="cat-name">Hostel</span>
            <span className="cat-count">{structures.filter(s => s.category === 'hostel').length} structures</span>
          </div>
          <div className="category-card">
            <span className="cat-icon">📝</span>
            <span className="cat-name">Exam</span>
            <span className="cat-count">{structures.filter(s => s.category === 'exam').length} structures</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthorityFeeStructure;
