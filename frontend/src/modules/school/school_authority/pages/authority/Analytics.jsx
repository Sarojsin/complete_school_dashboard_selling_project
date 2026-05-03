import { useState, useEffect } from 'react';
import { getAnalytics } from '../../api/authority';
import './AuthorityReports.css';

const AuthorityAnalytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await getAnalytics();
      setAnalytics(response.data);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-loading">Loading analytics...</div>;
  }

  return (
    <div className="authority-reports-page">
      <div className="page-header">
        <h1>Analytics Dashboard</h1>
        <p>School performance metrics and insights</p>
      </div>

      <div className="analytics-cards">
        <div className="analytics-card">
          <div className="card-icon students">👨‍🎓</div>
          <div className="card-content">
            <span className="value">{analytics?.total_students || 0}</span>
            <span className="label">Total Students</span>
          </div>
        </div>
        <div className="analytics-card">
          <div className="card-icon teachers">👨‍🏫</div>
          <div className="card-content">
            <span className="value">{analytics?.total_teachers || 0}</span>
            <span className="label">Total Teachers</span>
          </div>
        </div>
        <div className="analytics-card">
          <div className="card-icon courses">📚</div>
          <div className="card-content">
            <span className="value">{analytics?.total_courses || 0}</span>
            <span className="label">Total Courses</span>
          </div>
        </div>
        <div className="analytics-card">
          <div className="card-icon attendance">📊</div>
          <div className="card-content">
            <span className="value">{analytics?.avg_attendance || 0}%</span>
            <span className="label">Avg Attendance</span>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-card">
          <h3>Enrollment Trend</h3>
          <div className="chart-placeholder">
            <div className="bar-chart">
              <div className="bar" style={{height: '60%'}}><span>Jan</span></div>
              <div className="bar" style={{height: '75%'}}><span>Feb</span></div>
              <div className="bar" style={{height: '80%'}}><span>Mar</span></div>
              <div className="bar" style={{height: '70%'}}><span>Apr</span></div>
              <div className="bar" style={{height: '85%'}}><span>May</span></div>
              <div className="bar" style={{height: '90%'}}><span>Jun</span></div>
            </div>
          </div>
        </div>
        <div className="chart-card">
          <h3>Grade Distribution</h3>
          <div className="chart-placeholder">
            <div className="pie-chart">
              <div className="pie-segment a" style={{transform: 'rotate(0deg)'}}></div>
              <div className="pie-segment b" style={{transform: 'rotate(120deg)'}}></div>
              <div className="pie-segment c" style={{transform: 'rotate(200deg)'}}></div>
            </div>
            <div className="legend">
              <span><i style={{background: '#27ae60'}}></i> A Grade 30%</span>
              <span><i style={{background: '#3498db'}}></i> B Grade 35%</span>
              <span><i style={{background: '#f39c12'}}></i> C Grade 25%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="insights-section">
        <h3>Key Insights</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <span className="insight-icon">📈</span>
            <p>Student enrollment increased by 15% this month</p>
          </div>
          <div className="insight-card">
            <span className="insight-icon">⚠️</span>
            <p>5 students have attendance below 75%</p>
          </div>
          <div className="insight-card">
            <span className="insight-icon">💰</span>
            <p>Fee collection rate is at 82%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthorityAnalytics;
