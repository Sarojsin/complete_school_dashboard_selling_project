import { useState, useEffect } from 'react';
import { getFinanceData, getFinancialReports } from '../api/superadmin';
import './AdminPages.css';

const Finance = () => {
  const [loading, setLoading] = useState(true);
  const [financeData, setFinanceData] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadFinanceData();
  }, []);

  const loadFinanceData = async () => {
    try {
      const response = await getFinanceData();
      setFinanceData(response.data);
    } catch (err) {
      console.error('Failed to load finance data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading finance data...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Finance Management</h1>
        <p>Overview of financial transactions and reports</p>
      </div>

      <div className="finance-stats">
        <div className="finance-stat">
          <span className="value">${financeData?.total_revenue || '0'}</span>
          <span className="label">Total Revenue</span>
        </div>
        <div className="finance-stat">
          <span className="value">${financeData?.total_expenses || '0'}</span>
          <span className="label">Total Expenses</span>
        </div>
        <div className="finance-stat">
          <span className="value">${financeData?.net_income || '0'}</span>
          <span className="label">Net Income</span>
        </div>
        <div className="finance-stat">
          <span className="value">{financeData?.pending_payments || '0'}</span>
          <span className="label">Pending Payments</span>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'transactions' ? 'active' : ''}`}
          onClick={() => setActiveTab('transactions')}
        >
          Transactions
        </button>
        <button 
          className={`tab ${activeTab === 'reports' ? 'active' : ''}`}
          onClick={() => setActiveTab('reports')}
        >
          Reports
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="content-card">
          <h3>Financial Overview</h3>
          <div className="overview-grid">
            <div className="overview-item">
              <h4>Revenue by Category</h4>
              <div className="chart-placeholder">
                {financeData?.revenue_by_category?.map((item) => (
                  <div key={item.category} className="category-bar">
                    <span className="category-name">{item.category}</span>
                    <div className="bar-container">
                      <div 
                        className="bar" 
                        style={{width: `${item.percentage}%`}}
                      ></div>
                    </div>
                    <span className="category-value">${item.amount}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'transactions' && (
        <div className="content-card">
          <h3>Recent Transactions</h3>
          {financeData?.transactions?.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {financeData.transactions.map((trans) => (
                  <tr key={trans.id}>
                    <td>{trans.date}</td>
                    <td>{trans.description}</td>
                    <td>
                      <span className={`type-badge ${trans.type}`}>
                        {trans.type}
                      </span>
                    </td>
                    <td className={trans.type === 'income' ? 'income' : 'expense'}>
                      ${trans.amount}
                    </td>
                    <td>
                      <span className={`status-badge ${trans.status}`}>
                        {trans.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="empty-text">No transactions found</p>
          )}
        </div>
      )}

      {activeTab === 'reports' && (
        <div className="content-card">
          <h3>Financial Reports</h3>
          <div className="report-types">
            <button className="report-type">
              <span className="icon">📊</span>
              <h4>Income Statement</h4>
              <p>Revenue and expenses summary</p>
            </button>
            <button className="report-type">
              <span className="icon">💰</span>
              <h4>Cash Flow</h4>
              <p>Cash inflow and outflow</p>
            </button>
            <button className="report-type">
              <span className="icon">📈</span>
              <h4>Balance Sheet</h4>
              <p>Assets and liabilities</p>
            </button>
            <button className="report-type">
              <span className="icon">👥</span>
              <h4>Receivables</h4>
              <p>Outstanding payments</p>
            </button>
            <button className="report-type">
              <span className="icon">📋</span>
              <h4>Fee Collection</h4>
              <p>Fee payment summary</p>
            </button>
            <button className="report-type">
              <span className="icon">🏢</span>
              <h4>Expense Report</h4>
              <p>Detailed expense breakdown</p>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Finance;
