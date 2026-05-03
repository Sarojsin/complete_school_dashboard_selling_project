import { useEffect, useState } from 'react';
import { getOverdueLoans, returnBook } from '../api/library';
import '../../../shared/styles/global.css';
import './styles/library.css';

export default function Overdue() {
  const [overdueLoans, setOverdueLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchOverdueLoans();
  }, []);

  const fetchOverdueLoans = async () => {
    try {
      setLoading(true);
      const res = await getOverdueLoans();
      setOverdueLoans(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReturn = async (loanId) => {
    try {
      await returnBook(loanId);
      alert('Book returned successfully!');
      fetchOverdueLoans();
    } catch (err) {
      alert('Failed to return book: ' + err.message);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const getDaysOverdue = (dueDate) => {
    const due = new Date(dueDate);
    const now = new Date();
    const diffTime = now - due;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Overdue Books</h1>
        <p>Manage overdue book returns</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Summary Cards */}
      <div className="overdue-summary">
        <div className="summary-card total">
          <h3>Total Overdue</h3>
          <p className="summary-value">{overdueLoans.length}</p>
        </div>
        <div className="summary-card warning">
          <h3>Total Fines</h3>
          <p className="summary-value">
            ${overdueLoans.reduce((sum, loan) => sum + (loan.fine || 0), 0).toFixed(2)}
          </p>
        </div>
      </div>

      {/* Overdue List */}
      <div className="overdue-section">
        <h2>Overdue Books List</h2>
        {overdueLoans.length > 0 ? (
          <table className="data-table overdue-table">
            <thead>
              <tr>
                <th>Book</th>
                <th>Student</th>
                <th>Issue Date</th>
                <th>Due Date</th>
                <th>Days Overdue</th>
                <th>Fine</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {overdueLoans.map((loan) => (
                <tr key={loan.id}>
                  <td>
                    <strong>{loan.book_title}</strong>
                  </td>
                  <td>{loan.student_name}</td>
                  <td>{formatDate(loan.issue_date)}</td>
                  <td>{formatDate(loan.due_date)}</td>
                  <td>
                    <span className="days-overdue">
                      {getDaysOverdue(loan.due_date)} days
                    </span>
                  </td>
                  <td>
                    <span className="fine-amount">
                      ${loan.fine?.toFixed(2) || '0.00'}
                    </span>
                  </td>
                  <td>
                    <button 
                      className="btn btn-success btn-sm"
                      onClick={() => handleReturn(loan.id)}
                    >
                      Mark Returned
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="no-data success">
            <p>🎉 No overdue books! All books have been returned.</p>
          </div>
        )}
      </div>
    </div>
  );
}
