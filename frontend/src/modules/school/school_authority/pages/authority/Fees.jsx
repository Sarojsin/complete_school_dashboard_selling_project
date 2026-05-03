import { useState, useEffect } from 'react';
import { getFees, createFee } from '../../api/authority';
import './AuthorityFees.css';

const AuthorityFees = () => {
  const [fees, setFees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    amount: '',
    due_date: '',
    description: '',
    fee_type: 'tuition'
  });

  useEffect(() => {
    loadFees();
  }, []);

  const loadFees = async () => {
    try {
      const response = await getFees();
      setFees(response.data);
    } catch (err) {
      console.error('Failed to load fees:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createFee(formData);
      setShowForm(false);
      setFormData({
        student_id: '',
        amount: '',
        due_date: '',
        description: '',
        fee_type: 'tuition'
      });
      loadFees();
    } catch (err) {
      console.error('Failed to create fee:', err);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      paid: { class: 'paid', text: 'Paid' },
      pending: { class: 'pending', text: 'Pending' },
      overdue: { class: 'overdue', text: 'Overdue' }
    };
    const badge = badges[status] || badges.pending;
    return <span className={`status-badge ${badge.class}`}>{badge.text}</span>;
  };

  if (loading) {
    return <div className="fees-loading">Loading fees...</div>;
  }

  return (
    <div className="authority-fees-page">
      <div className="page-header">
        <div>
          <h1>Fee Management</h1>
          <p>Manage student fees and payments</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Fee'}
        </button>
      </div>

      {showForm && (
        <div className="fee-form-card">
          <h3>Create New Fee</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Student ID</label>
                <input
                  type="text"
                  value={formData.student_id}
                  onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Fee Type</label>
                <select
                  value={formData.fee_type}
                  onChange={(e) => setFormData({...formData, fee_type: e.target.value})}
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
                <label>Due Date</label>
                <input
                  type="date"
                  value={formData.due_date}
                  onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                  required
                />
              </div>
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows={3}
              />
            </div>
            <button type="submit" className="btn-submit">Create Fee</button>
          </form>
        </div>
      )}

      <div className="fees-summary">
        <div className="summary-card">
          <span className="summary-icon">💰</span>
          <div>
            <span className="summary-value">${fees.reduce((sum, f) => sum + (parseFloat(f.amount) || 0), 0).toLocaleString()}</span>
            <span className="summary-label">Total Amount</span>
          </div>
        </div>
        <div className="summary-card">
          <span className="summary-icon">✓</span>
          <div>
            <span className="summary-value">{fees.filter(f => f.status === 'paid').length}</span>
            <span className="summary-label">Paid</span>
          </div>
        </div>
        <div className="summary-card">
          <span className="summary-icon">⏳</span>
          <div>
            <span className="summary-value">{fees.filter(f => f.status === 'pending').length}</span>
            <span className="summary-label">Pending</span>
          </div>
        </div>
        <div className="summary-card">
          <span className="summary-icon">⚠️</span>
          <div>
            <span className="summary-value">{fees.filter(f => f.status === 'overdue').length}</span>
            <span className="summary-label">Overdue</span>
          </div>
        </div>
      </div>

      <div className="fees-table-card">
        <h3>Fee Records</h3>
        {fees.length > 0 ? (
          <table className="fees-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Type</th>
                <th>Amount</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {fees.map((fee) => (
                <tr key={fee.id}>
                  <td>{fee.student_name || 'N/A'}</td>
                  <td>{fee.fee_type}</td>
                  <td>${parseFloat(fee.amount || 0).toLocaleString()}</td>
                  <td>{fee.due_date}</td>
                  <td>{getStatusBadge(fee.status)}</td>
                  <td>
                    <button className="btn-action">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📋</span>
            <p>No fee records found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthorityFees;
