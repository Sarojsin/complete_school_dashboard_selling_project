import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../../shared/api/client';
import './TestList.css';

const TestList = () => {
  const [tests, setTests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTests();
  }, []);

  const loadTests = async () => {
    try {
      const response = await api.get('/student/tests');
      setTests(response.data || []);
    } catch (err) {
      console.error('Failed to load tests:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      available: '#27ae60',
      in_progress: '#f39c12',
      completed: '#3498db',
      expired: '#e74c3c'
    };
    return colors[status] || '#95a5a6';
  };

  if (loading) {
    return <div className="test-list-loading">Loading tests...</div>;
  }

  return (
    <div className="test-list-page">
      <div className="page-header">
        <h1>Online Tests</h1>
        <p>Take available tests and view results</p>
      </div>

      <div className="tests-content">
        {tests.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📝</span>
            <h3>No Tests Available</h3>
            <p>There are no tests available at the moment</p>
          </div>
        ) : (
          <div className="tests-grid">
            {tests.map((test, index) => (
              <div key={index} className="test-card">
                <div className="test-header">
                  <h3>{test.title}</h3>
                  <span 
                    className="status-badge"
                    style={{ background: getStatusColor(test.status) }}
                  >
                    {test.status.replace('_', ' ')}
                  </span>
                </div>
                <div className="test-info">
                  <p className="subject">{test.subject}</p>
                  <p className="description">{test.description}</p>
                  <div className="test-meta">
                    <span>📅 {formatDate(test.date)}</span>
                    <span>⏱️ {test.duration} min</span>
                    <span>📝 {test.questions} questions</span>
                  </div>
                  <div className="test-marks">
                    <span>Total Marks: {test.total_marks}</span>
                  </div>
                </div>
                <div className="test-actions">
                  {test.status === 'available' && (
                    <Link to={`/student/tests/${test.id}`} className="start-btn">
                      Start Test
                    </Link>
                  )}
                  {test.status === 'completed' && (
                    <button className="result-btn">View Result</button>
                  )}
                  {test.status === 'in_progress' && (
                    <Link to={`/student/tests/${test.id}`} className="continue-btn">
                      Continue Test
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TestList;
