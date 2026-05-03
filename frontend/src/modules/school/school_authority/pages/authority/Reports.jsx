import { useState, useEffect } from 'react';
import { getReports, generateReport } from '../../api/authority';
import './AuthorityReports.css';

const AuthorityReports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const response = await getReports();
      setReports(response.data || []);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async (type) => {
    setGenerating(true);
    try {
      const response = await generateReport(type);
      setReports([...reports, response.data]);
    } catch (err) {
      console.error('Failed to generate report:', err);
    } finally {
      setGenerating(false);
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const reportTypes = [
    { id: 'attendance', name: 'Attendance Report', icon: '📊', description: 'Student attendance statistics' },
    { id: 'fees', name: 'Fee Collection Report', icon: '💰', description: 'Fee collection and pending payments' },
    { id: 'grades', name: 'Grade Analysis', icon: '📝', description: 'Student grades and performance' },
    { id: 'enrollment', name: 'Enrollment Report', icon: '👥', description: 'Student enrollment statistics' },
    { id: 'teachers', name: 'Teacher Report', icon: '👨‍🏫', description: 'Teacher allocation and subjects' },
    { id: 'exams', name: 'Exam Report', icon: '📋', description: 'Exam schedule and results' }
  ];

  if (loading) {
    return <div className="reports-loading">Loading reports...</div>;
  }

  return (
    <div className="authority-reports-page">
      <div className="page-header">
        <h1>Reports & Analytics</h1>
        <p>Generate and view various school reports</p>
      </div>

      <div className="generate-section">
        <h2>Generate New Report</h2>
        <div className="report-types">
          {reportTypes.map((type) => (
            <div key={type.id} className="report-type-card">
              <span className="icon">{type.icon}</span>
              <h3>{type.name}</h3>
              <p>{type.description}</p>
              <button 
                onClick={() => handleGenerate(type.id)}
                disabled={generating}
              >
                Generate
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="existing-reports">
        <h2>Existing Reports</h2>
        {reports.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📄</span>
            <p>No reports generated yet</p>
          </div>
        ) : (
          <div className="reports-table">
            <table>
              <thead>
                <tr>
                  <th>Report Name</th>
                  <th>Type</th>
                  <th>Generated Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((report, index) => (
                  <tr key={index}>
                    <td>{report.name}</td>
                    <td>{report.type}</td>
                    <td>{formatDate(report.created_at)}</td>
                    <td>
                      <button className="download-btn">⬇️ Download</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthorityReports;
