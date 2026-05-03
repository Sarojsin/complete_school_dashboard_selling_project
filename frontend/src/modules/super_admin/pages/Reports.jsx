import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Reports = () => {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [generating, setGenerating] = useState(false);
  const [reportType, setReportType] = useState('students');

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const response = await fetch('/api/super-admin/reports', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      const data = await response.json();
      setReports(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load reports');
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setGenerating(true);
    try {
      const response = await fetch(`/api/super-admin/reports/generate?type=${reportType}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });

      if (response.ok) {
        loadReports();
      } else {
        setError('Failed to generate report');
      }
    } catch (err) {
      setError('An error occurred');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (reportId, format) => {
    try {
      const response = await fetch(`/api/super-admin/reports/${reportId}/download?format=${format}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `report-${reportId}.${format}`;
        a.click();
      }
    } catch (err) {
      setError('Failed to download report');
    }
  };

  const handleDelete = async (reportId) => {
    if (!window.confirm('Are you sure you want to delete this report?')) return;

    try {
      const response = await fetch(`/api/super-admin/reports/${reportId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });

      if (response.ok) {
        setReports(reports.filter(r => r.id !== reportId));
      }
    } catch (err) {
      setError('Failed to delete report');
    }
  };

  if (loading) {
    return <div className="loading">Loading reports...</div>;
  }

  return (
    <div className="admin-reports-container">
      <div className="page-header">
        <h1>Reports</h1>
        <button onClick={() => navigate('/admin')} className="back-btn">
          ← Back to Dashboard
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="generate-report-section">
        <h2>Generate New Report</h2>
        <div className="generate-form">
          <div className="form-group">
            <label>Report Type</label>
            <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
              <option value="students">Student Report</option>
              <option value="teachers">Teacher Report</option>
              <option value="courses">Course Report</option>
              <option value="attendance">Attendance Report</option>
              <option value="grades">Grades Report</option>
              <option value="fees">Fees Report</option>
              <option value="activity">Activity Report</option>
            </select>
          </div>
          <button 
            onClick={handleGenerateReport} 
            className="btn-primary"
            disabled={generating}
          >
            {generating ? 'Generating...' : 'Generate Report'}
          </button>
        </div>
      </div>

      <div className="reports-list-section">
        <h2>Existing Reports</h2>
        {reports.length === 0 ? (
          <p className="no-reports">No reports generated yet.</p>
        ) : (
          <table className="reports-table">
            <thead>
              <tr>
                <th>Report Name</th>
                <th>Type</th>
                <th>Generated Date</th>
                <th>Size</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reports.map(report => (
                <tr key={report.id}>
                  <td>{report.name}</td>
                  <td>{report.type}</td>
                  <td>{new Date(report.created_at).toLocaleString()}</td>
                  <td>{report.size || 'N/A'}</td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        onClick={() => handleDownload(report.id, 'pdf')}
                        className="btn-download"
                      >
                        PDF
                      </button>
                      <button 
                        onClick={() => handleDownload(report.id, 'excel')}
                        className="btn-download"
                      >
                        Excel
                      </button>
                      <button 
                        onClick={() => handleDelete(report.id)}
                        className="btn-delete"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Reports;
