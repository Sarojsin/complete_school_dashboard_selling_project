import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getActiveLoans, returnBook, calculateFine } from '../api/library';
import '../../../shared/styles/global.css';
import './styles/library.css';

export default function ReturnBook() {
  const navigate = useNavigate();
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedLoan, setSelectedLoan] = useState(null);
  const [fine, setFine] = useState(null);
  const [returning, setReturning] = useState(false);

  useEffect(() => {
    fetchLoans();
  }, []);

  const fetchLoans = async () => {
    try {
      setLoading(true);
      const res = await getActiveLoans();
      setLoans(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectLoan = async (loan) => {
    setSelectedLoan(loan);
    try {
      const fineRes = await calculateFine(loan.id);
      setFine(fineRes.data);
    } catch (err) {
      setFine(0);
    }
  };

  const handleReturn = async () => {
    if (!selectedLoan) return;
    
    try {
      setReturning(true);
      await returnBook(selectedLoan.id);
      alert('Book returned successfully!');
      setSelectedLoan(null);
      setFine(null);
      fetchLoans();
    } catch (err) {
      alert('Failed to return book: ' + err.message);
    } finally {
      setReturning(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
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
        <h1>Return Book</h1>
        <p>Process book returns</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="return-layout">
        {/* Loans List */}
        <div className="loans-section">
          <h2>Active Loans</h2>
          {loans.length > 0 ? (
            <div className="loans-list">
              {loans.map((loan) => (
                <div 
                  key={loan.id} 
                  className={`loan-card ${selectedLoan?.id === loan.id ? 'selected' : ''}`}
                  onClick={() => handleSelectLoan(loan)}
                >
                  <div className="loan-book">
                    <strong>{loan.book_title}</strong>
                  </div>
                  <div className="loan-student">
                    {loan.student_name}
                  </div>
                  <div className="loan-dates">
                    <span>Issued: {formatDate(loan.issue_date)}</span>
                    <span>Due: {formatDate(loan.due_date)}</span>
                  </div>
                  <div className={`loan-status ${new Date(loan.due_date) < new Date() ? 'overdue' : ''}`}>
                    {new Date(loan.due_date) < new Date() ? 'Overdue' : 'Active'}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">
              <p>No active loans.</p>
            </div>
          )}
        </div>

        {/* Return Form */}
        <div className="return-section">
          <h2>Process Return</h2>
          {selectedLoan ? (
            <div className="return-form">
              <div className="selected-loan-details">
                <h3>Selected Loan</h3>
                <p><strong>Book:</strong> {selectedLoan.book_title}</p>
                <p><strong>Student:</strong> {selectedLoan.student_name}</p>
                <p><strong>Issue Date:</strong> {formatDate(selectedLoan.issue_date)}</p>
                <p><strong>Due Date:</strong> {formatDate(selectedLoan.due_date)}</p>
                
                {fine > 0 && (
                  <div className="fine-warning">
                    <strong>Late Fee: ${fine}</strong>
                  </div>
                )}
              </div>

              <button 
                className="btn btn-success btn-lg"
                onClick={handleReturn}
                disabled={returning}
              >
                {returning ? 'Processing...' : 'Confirm Return'}
              </button>
            </div>
          ) : (
            <div className="no-selection">
              <p>Select a loan from the list to process return</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
