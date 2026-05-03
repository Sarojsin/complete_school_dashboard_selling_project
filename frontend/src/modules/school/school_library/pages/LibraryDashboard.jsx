import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getLibraryDashboard, getActiveLoans, getOverdueLoans } from '../api/library';
import Card from '../../../shared/components/Card';
import Badge from '../../../shared/components/Badge';
import './styles/library.css';

export default function LibraryDashboard() {
  const [summary, setSummary] = useState(null);
  const [activeLoans, setActiveLoans] = useState([]);
  const [returnedLoans, setReturnedLoans] = useState([]);
  const [overdueLoans, setOverdueLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock data matching backup/templates student library
  const mockActiveLoans = [
    { id: 1, book_title: 'Introduction to Algorithms', book_author: 'Cormen et al.', taken_date: '2024-03-10', due_date: '2024-03-25', status: 'active' },
    { id: 2, book_title: 'Database System Concepts', book_author: 'Silberschatz', taken_date: '2024-03-15', due_date: '2024-03-30', status: 'active' },
    { id: 3, book_title: 'Operating System Concepts', book_author: 'Silberschatz et al.', taken_date: '2024-03-18', due_date: '2024-04-02', status: 'active' },
  ];

  const mockReturnedLoans = [
    { id: 101, book_title: 'Computer Networks', book_author: 'Tanenbaum', taken_date: '2024-02-01', return_date: '2024-02-15', fine_amount: 0 },
    { id: 102, book_title: 'Software Engineering', book_author: 'Sommerville', taken_date: '2024-01-15', return_date: '2024-01-30', fine_amount: 50 },
  ];

  const stats = {
    total_borrowed: 15,
    currently_borrowed: 3,
    overdue_count: 0,
    total_fines: 50,
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryRes, loansRes, overdueRes] = await Promise.all([
        getLibraryDashboard(),
        getActiveLoans(),
        getOverdueLoans()
      ]);
      
      setSummary(summaryRes.data);
      setActiveLoans(loansRes.data || mockActiveLoans);
      setReturnedLoans(mockReturnedLoans);
      setOverdueLoans(overdueRes.data || []);
    } catch (err) {
      setError(err.message || 'Failed to load library data');
      console.error('Error fetching library dashboard:', err);
      // Use mock data on error
      setActiveLoans(mockActiveLoans);
      setReturnedLoans(mockReturnedLoans);
    } finally {
      setLoading(false);
    }
  };

  const getDaysLeft = (dueDate) => {
    const today = new Date('2024-03-28'); // Mock today
    const due = new Date(dueDate);
    const diff = Math.ceil((due - today) / (1000 * 60 * 60 * 24));
    return diff;
  };

  const getDaysLeftVariant = (daysLeft) => {
    if (daysLeft < 0) return 'danger';
    if (daysLeft === 0) return 'warning';
    if (daysLeft <= 3) return 'warning';
    return 'success';
  };

  const getDueDateVariant = (daysLeft) => {
    if (daysLeft < 0) return 'text-danger fw-bold';
    if (daysLeft <= 3) return 'text-warning fw-bold';
    return '';
  };

  if (loading) {
    return (
      <div className="library-page p-4">
        <div className="text-center">Loading library data...</div>
      </div>
    );
  }

  return (
    <div className="library-page">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1><i className="bi bi-book-half me-2 text-primary"></i>My Library Account</h1>
          <p className="text-muted mb-0">John Doe (STU-2024-001)</p>
        </div>
        <Link to="/student/dashboard" className="btn btn-outline-primary">
          <i className="bi bi-arrow-left me-2"></i>Back to Dashboard
        </Link>
      </div>

      {/* Stats Cards with Gradients */}
      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card border-0 h-100" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
            <div className="card-body text-white">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="card-title mb-0">Total Books Borrowed</h6>
                  <h3 className="mt-2 mb-0">{stats.total_borrowed}</h3>
                </div>
                <i className="bi bi-bookshelf fs-1 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 h-100" style={{ background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)' }}>
            <div className="card-body text-white">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="card-title mb-0">Currently Borrowed</h6>
                  <h3 className="mt-2 mb-0">{stats.currently_borrowed}</h3>
                </div>
                <i className="bi bi-book fs-1 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 h-100" style={{ background: 'linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%)' }}>
            <div className="card-body text-white">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="card-title mb-0">Overdue Books</h6>
                  <h3 className="mt-2 mb-0">{stats.overdue_count}</h3>
                </div>
                <i className="bi bi-exclamation-circle fs-1 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 h-100" style={{ background: 'linear-gradient(135deg, #834d9b 0%, #d04ed6 100%)' }}>
            <div className="card-body text-white">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="card-title mb-0">Total Fines</h6>
                  <h3 className="mt-2 mb-0">₹{stats.total_fines}</h3>
                  {stats.total_fines > 0 && <small>Please pay at library</small>}
                </div>
                <i className="bi bi-cash-coin fs-1 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Currently Borrowed Books */}
      {activeLoans.length > 0 && (
        <Card title="Currently Borrowed Books" icon="book" className="mb-4">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <Badge variant="primary">{activeLoans.length} books</Badge>
          </div>
          <div className="table-responsive">
            <table className="table table-hover">
              <thead className="table-light">
                <tr>
                  <th>Book Title</th>
                  <th>Author</th>
                  <th>Borrowed Date</th>
                  <th>Due Date</th>
                  <th>Days Left</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {activeLoans.map((loan) => {
                  const daysLeft = getDaysLeft(loan.due_date);
                  return (
                    <tr key={loan.id}>
                      <td>
                        <div className="d-flex align-items-center">
                          <i className="bi bi-book me-2 text-primary"></i>
                          <span className="fw-medium">{loan.book_title}</span>
                        </div>
                      </td>
                      <td>{loan.book_author}</td>
                      <td>{loan.taken_date}</td>
                      <td className={getDueDateVariant(daysLeft)}>
                        {loan.due_date}
                      </td>
                      <td>
                        <Badge variant={getDaysLeftVariant(daysLeft)}>
                          {daysLeft < 0 ? `${Math.abs(daysLeft)} days overdue` : daysLeft === 0 ? 'Due today' : `${daysLeft} days left`}
                        </Badge>
                      </td>
                      <td>
                        {daysLeft < 0 ? (
                          <Badge variant="danger">Overdue</Badge>
                        ) : (
                          <Badge variant="primary">Active</Badge>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Returned Books History */}
      {returnedLoans.length > 0 && (
        <Card title="Returned Books History" icon="clock-history" className="mb-4">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <Badge variant="success">{returnedLoans.length} books</Badge>
          </div>
          <div className="table-responsive">
            <table className="table table-hover">
              <thead className="table-light">
                <tr>
                  <th>Book Title</th>
                  <th>Author</th>
                  <th>Borrowed Date</th>
                  <th>Returned Date</th>
                  <th>Fine Paid</th>
                </tr>
              </thead>
              <tbody>
                {returnedLoans.map((loan) => (
                  <tr key={loan.id}>
                    <td>
                      <div className="d-flex align-items-center">
                        <i className="bi bi-check-circle me-2 text-success"></i>
                        <span className="fw-medium">{loan.book_title}</span>
                      </div>
                    </td>
                    <td>{loan.book_author}</td>
                    <td>{loan.taken_date}</td>
                    <td>{loan.return_date}</td>
                    <td>
                      {loan.fine_amount > 0 ? (
                        <span className="text-danger fw-bold">₹{loan.fine_amount}</span>
                      ) : (
                        <span className="text-muted">-</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Empty State */}
      {activeLoans.length === 0 && returnedLoans.length === 0 && (
        <div className="text-center py-5">
          <i className="bi bi-book display-4 text-muted"></i>
          <h4 className="mt-3 text-muted">No Library Records</h4>
          <p className="text-muted">You haven't borrowed any books yet.</p>
          <Link to="/library/books" className="btn btn-primary mt-2">
            <i className="bi bi-search me-2"></i>Browse Book Catalog
          </Link>
        </div>
      )}

      {/* Library Information */}
      <Card title="Library Information" icon="info-circle">
        <div className="row">
          <div className="col-md-4">
            <h6><i className="bi bi-clock me-2"></i>Loan Period</h6>
            <p className="text-muted small">Books can be borrowed for 15 days. Please return on time to avoid fines.</p>
          </div>
          <div className="col-md-4">
            <h6><i className="bi bi-cash-coin me-2"></i>Fine Structure</h6>
            <p className="text-muted small">₹10 per day for overdue books. Pay at the library counter.</p>
          </div>
          <div className="col-md-4">
            <h6><i className="bi bi-telephone me-2"></i>Contact</h6>
            <p className="text-muted small">Visit the library or contact the librarian for any queries.</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
