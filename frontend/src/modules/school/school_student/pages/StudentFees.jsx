import { useState, useEffect } from 'react';
import api from '../../../shared/api/client';
import Card from '../../../shared/components/Card';
import Badge from '../../../shared/components/Badge';
import './StudentFees.css';

const StudentFees = () => {
  const [fees, setFees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  // Mock data for demonstration
  const mockFees = [
    { id: 1, name: 'Tuition Fee - Spring 2024', amount: 5000, paid_amount: 5000, status: 'paid', due_date: '2024-01-15', payment_date: '2024-01-10', payment_method: 'Online Transfer', transaction_id: 'TXN-2024-001' },
    { id: 2, name: 'Laboratory Fee', amount: 500, paid_amount: 500, status: 'paid', due_date: '2024-02-01', payment_date: '2024-01-28', payment_method: 'Credit Card', transaction_id: 'TXN-2024-002' },
    { id: 3, name: 'Library Fee', amount: 200, paid_amount: 200, status: 'paid', due_date: '2024-02-15', payment_date: '2024-02-10', payment_method: 'Debit Card', transaction_id: 'TXN-2024-003' },
    { id: 4, name: 'Tuition Fee - Summer 2024', amount: 5000, paid_amount: 2500, status: 'partial', due_date: '2024-04-01', payment_date: '2024-03-20', payment_method: 'Online Payment', transaction_id: 'TXN-2024-004', balance: 2500 },
    { id: 5, name: 'Examination Fee', amount: 300, paid_amount: 0, status: 'pending', due_date: '2024-05-15', payment_date: null, payment_method: null, transaction_id: null },
    { id: 6, name: 'Transport Fee - April', amount: 400, paid_amount: 0, status: 'pending', due_date: '2024-04-01', payment_date: null, payment_method: null, transaction_id: null },
    { id: 7, name: 'Hostel Fee - Spring 2024', amount: 3000, paid_amount: 3000, status: 'paid', due_date: '2024-01-20', payment_date: '2024-01-15', payment_method: 'Bank Transfer', transaction_id: 'TXN-2024-005' },
  ];

  // Calculate totals
  const totalAmount = mockFees.reduce((sum, fee) => sum + fee.amount, 0);
  const totalPaid = mockFees.filter(f => f.status === 'paid').reduce((sum, fee) => sum + fee.paid_amount, 0) + mockFees.filter(f => f.status === 'partial').reduce((sum, fee) => sum + fee.paid_amount, 0);
  const totalPending = totalAmount - totalPaid;
  const totalOverdue = mockFees.filter(f => f.status === 'overdue').reduce((sum, fee) => sum + fee.amount, 0);

  const stats = [
    { icon: 'cash-stack', value: `${totalAmount.toLocaleString()}`, label: 'Total Fees', sublabel: 'Academic Year 2024', color: 'primary' },
    { icon: 'check-circle', value: `${totalPaid.toLocaleString()}`, label: 'Amount Paid', sublabel: `${((totalPaid/totalAmount)*100).toFixed(0)}% completed`, color: 'success' },
    { icon: 'clock', value: `${totalPending.toLocaleString()}`, label: 'Amount Pending', sublabel: 'Due this semester', color: 'warning' },
    { icon: 'exclamation-triangle', value: `${totalOverdue.toLocaleString()}`, label: 'Overdue', sublabel: 'Immediate action needed', color: 'danger' },
  ];

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusVariant = (status) => {
    const variants = {
      paid: 'success',
      pending: 'warning',
      overdue: 'danger',
      partial: 'info'
    };
    return variants[status] || 'secondary';
  };

  const filteredFees = filter === 'all' ? mockFees : mockFees.filter(fee => fee.status === filter);

  useEffect(() => {
    loadFees();
  }, []);

  const loadFees = async () => {
    try {
      const response = await api.get('/student/fees');
      setFees(response.data || mockFees);
    } catch (err) {
      console.error('Failed to load fees:', err);
      setFees(mockFees);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="fees-loading">Loading fees...</div>;
  }

  return (
    <div className="student-fees-page">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>My Fees</h1>
          <p className="text-muted mb-0">View and pay your school fees</p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-primary">
            <i className="bi bi-download me-2"></i>Download Receipt
          </button>
          <button className="btn btn-primary">
            <i className="bi bi-credit-card me-2"></i>Pay Now
          </button>
        </div>
      </div>

      {/* Stats Row */}
      <div className="row g-3 mb-4">
        {stats.map((stat, idx) => (
          <div className="col-xl-3 col-md-6" key={idx}>
            <Card className="h-100">
              <div className="card-body">
                <div className="d-flex align-items-center">
                  <div className="flex-grow-1">
                    <div className="text-xs fw-bold text-uppercase mb-1" style={{ color: `var(--${stat.color})` }}>{stat.label}</div>
                    <div className="h4 mb-0 fw-bold">{stat.value}</div>
                    <small className="text-muted">{stat.sublabel}</small>
                  </div>
                  <div className="ms-3">
                    <i className={`bi bi-${stat.icon} fs-1 text-${stat.color}`} style={{ opacity: 0.3 }}></i>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        ))}
      </div>

      {/* Filter & Fee List */}
      <div className="row">
        <div className="col-lg-8">
          <Card title="Fee Details" icon="receipt">
            <div className="d-flex gap-2 mb-3">
              <button 
                className={`btn btn-sm ${filter === 'all' ? 'btn-primary' : 'btn-outline-primary'}`}
                onClick={() => setFilter('all')}
              >
                All Fees
              </button>
              <button 
                className={`btn btn-sm ${filter === 'pending' ? 'btn-warning' : 'btn-outline-primary'}`}
                onClick={() => setFilter('pending')}
              >
                Pending
              </button>
              <button 
                className={`btn btn-sm ${filter === 'partial' ? 'btn-info' : 'btn-outline-primary'}`}
                onClick={() => setFilter('partial')}
              >
                Partial
              </button>
              <button 
                className={`btn btn-sm ${filter === 'paid' ? 'btn-success' : 'btn-outline-primary'}`}
                onClick={() => setFilter('paid')}
              >
                Paid
              </button>
            </div>

            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Fee Type</th>
                    <th>Amount</th>
                    <th>Paid</th>
                    <th>Balance</th>
                    <th>Due Date</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFees.map((fee) => (
                    <tr key={fee.id}>
                      <td>
                        <div className="d-flex align-items-center">
                          <i className="bi bi-file-text text-muted me-2"></i>
                          <span className="fw-medium">{fee.name}</span>
                        </div>
                      </td>
                      <td><strong>{formatCurrency(fee.amount)}</strong></td>
                      <td className="text-success">{formatCurrency(fee.paid_amount)}</td>
                      <td>
                        {fee.balance ? (
                          <span className="text-warning">{formatCurrency(fee.balance)}</span>
                        ) : (
                          <span className="text-muted">-</span>
                        )}
                      </td>
                      <td>{formatDate(fee.due_date)}</td>
                      <td>
                        <Badge variant={getStatusVariant(fee.status)}>
                          {fee.status.charAt(0).toUpperCase() + fee.status.slice(1)}
                        </Badge>
                      </td>
                      <td>
                        {(fee.status === 'pending' || fee.status === 'partial' || fee.status === 'overdue') && (
                          <button className="btn btn-sm btn-primary">
                            <i className="bi bi-credit-card"></i>
                          </button>
                        )}
                        {fee.status === 'paid' && (
                          <button className="btn btn-sm btn-outline-secondary" title="Download Receipt">
                            <i className="bi bi-download"></i>
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        {/* Payment Summary */}
        <div className="col-lg-4">
          <Card title="Payment Summary" icon="pie-chart" className="mb-4">
            <div className="mb-3">
              <div className="d-flex justify-content-between mb-2">
                <span>Paid</span>
                <span className="fw-bold">{formatCurrency(totalPaid)}</span>
              </div>
              <div className="progress" style={{ height: '12px' }}>
                <div className="progress-bar bg-success" style={{ width: `${(totalPaid/totalAmount)*100}%` }}></div>
                <div className="progress-bar bg-warning" style={{ width: `${(totalPending/totalAmount)*100}%` }}></div>
              </div>
              <div className="d-flex justify-content-between mt-2">
                <small className="text-success">{((totalPaid/totalAmount)*100).toFixed(0)}% Paid</small>
                <small className="text-warning">{((totalPending/totalAmount)*100).toFixed(0)}% Pending</small>
              </div>
            </div>

            <hr />

            <div className="payment-instructions">
              <h6>Payment Methods</h6>
              <ul className="list-unstyled small">
                <li className="mb-2"><i className="bi bi-check-circle text-success me-2"></i>Online Payment (Credit/Debit Card)</li>
                <li className="mb-2"><i className="bi bi-check-circle text-success me-2"></i>Bank Transfer</li>
                <li className="mb-2"><i className="bi bi-check-circle text-success me-2"></i>UPI Payment</li>
                <li className="mb-2"><i className="bi bi-check-circle text-success me-2"></i>Cash at Office</li>
              </ul>
            </div>
          </Card>

          <Card title="Recent Transactions" icon="history">
            <div className="recent-transactions">
              {mockFees.filter(f => f.status === 'paid').slice(0, 3).map((fee, idx) => (
                <div key={idx} className="transaction-item d-flex align-items-center mb-3">
                  <div className="icon-box bg-success bg-opacity-10 rounded p-2 me-3">
                    <i className="bi bi-check-circle text-success"></i>
                  </div>
                  <div className="flex-grow-1">
                    <div className="small fw-medium">{fee.name}</div>
                    <small className="text-muted">{formatDate(fee.payment_date)}</small>
                  </div>
                  <div className="text-end">
                    <div className="small fw-bold">{formatCurrency(fee.paid_amount)}</div>
                    <small className="text-muted">{fee.transaction_id}</small>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default StudentFees;
