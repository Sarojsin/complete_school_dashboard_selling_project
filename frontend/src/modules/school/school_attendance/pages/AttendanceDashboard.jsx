import { useState, useEffect } from 'react';
import { getSessions, getAttendanceRecords, getStats } from '../api/attendance';
import './styles/attendance.css';

const AttendanceDashboard = () => {
  const [sessions, setSessions] = useState([]);
  const [records, setRecords] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('sessions');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    loadData();
  }, [selectedDate]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [sessionsRes, recordsRes] = await Promise.all([
        getSessions(),
        getAttendanceRecords({ date: selectedDate })
      ]);
      setSessions(sessionsRes.data || []);
      setRecords(recordsRes.data || []);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      present: '#27ae60',
      absent: '#e74c3c',
      late: '#f39c12',
      excused: '#3498db'
    };
    return colors[status] || '#95a5a6';
  };

  const statsData = [
    { label: 'Present', count: records.filter(r => r.status === 'present').length, color: '#27ae60' },
    { label: 'Absent', count: records.filter(r => r.status === 'absent').length, color: '#e74c3c' },
    { label: 'Late', count: records.filter(r => r.status === 'late').length, color: '#f39c12' },
    { label: 'Excused', count: records.filter(r => r.status === 'excused').length, color: '#3498db' }
  ];

  if (loading) {
    return <div className="attendance-loading">Loading attendance...</div>;
  }

  return (
    <div className="attendance-dashboard">
      <div className="attendance-header">
        <div className="header-content">
          <h1>Attendance Management</h1>
          <p>Track and manage student attendance</p>
        </div>
        <div className="header-actions">
          <button className="btn-primary">+ New Session</button>
        </div>
      </div>

      <div className="date-selector">
        <button 
          className="date-nav"
          onClick={() => {
            const d = new Date(selectedDate);
            d.setDate(d.getDate() - 1);
            setSelectedDate(d.toISOString().split('T')[0]);
          }}
        >
          ← Previous
        </button>
        <input 
          type="date" 
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="date-input"
        />
        <button 
          className="date-nav"
          onClick={() => {
            const d = new Date(selectedDate);
            d.setDate(d.getDate() + 1);
            setSelectedDate(d.toISOString().split('T')[0]);
          }}
        >
          Next →
        </button>
      </div>

      <div className="attendance-tabs">
        <button 
          className={`tab ${activeTab === 'sessions' ? 'active' : ''}`}
          onClick={() => setActiveTab('sessions')}
        >
          Sessions
        </button>
        <button 
          className={`tab ${activeTab === 'records' ? 'active' : ''}`}
          onClick={() => setActiveTab('records')}
        >
          Records
        </button>
        <button 
          className={`tab ${activeTab === 'reports' ? 'active' : ''}`}
          onClick={() => setActiveTab('reports')}
        >
          Reports
        </button>
      </div>

      <div className="attendance-content">
        {activeTab === 'sessions' && (
          <div className="sessions-content">
            <div className="stats-row">
              {statsData.map((stat, index) => (
                <div key={index} className="stat-card" style={{ borderLeftColor: stat.color }}>
                  <span className="stat-count">{stat.count}</span>
                  <span className="stat-label">{stat.label}</span>
                </div>
              ))}
            </div>

            <div className="sessions-list">
              <h3>Today's Sessions</h3>
              {sessions.length === 0 ? (
                <div className="empty-state">
                  <p>No attendance sessions for this date</p>
                </div>
              ) : (
                <div className="session-cards">
                  {sessions.map(session => (
                    <div key={session.id} className="session-card">
                      <div className="session-header">
                        <h4>{session.class_name}</h4>
                        <span className="session-time">{session.time}</span>
                      </div>
                      <div className="session-info">
                        <span>📚 {session.subject}</span>
                        <span>👨‍🏫 {session.teacher}</span>
                      </div>
                      <div className="session-stats">
                        <span className="present">{session.present_count} Present</span>
                        <span className="absent">{session.absent_count} Absent</span>
                      </div>
                      <button className="btn-secondary">Take Attendance</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'records' && (
          <div className="records-content">
            <div className="content-header">
              <h2>Attendance Records</h2>
              <div className="filters">
                <select className="filter-select">
                  <option>All Classes</option>
                </select>
                <input 
                  type="text" 
                  placeholder="Search student..." 
                  className="search-input"
                />
              </div>
            </div>
            <div className="records-table">
              <table>
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Class</th>
                    <th>Subject</th>
                    <th>Time</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map(record => (
                    <tr key={record.id}>
                      <td>{record.student_name}</td>
                      <td>{record.class_name}</td>
                      <td>{record.subject}</td>
                      <td>{record.time}</td>
                      <td>
                        <span 
                          className="status-badge"
                          style={{ background: getStatusColor(record.status) }}
                        >
                          {record.status}
                        </span>
                      </td>
                      <td>
                        <button className="btn-icon">✏️</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="reports-content">
            <div className="content-header">
              <h2>Attendance Reports</h2>
              <button className="btn-primary">Generate Report</button>
            </div>
            <div className="reports-grid">
              <div className="report-card">
                <div className="report-icon">📊</div>
                <h4>Monthly Summary</h4>
                <p>Overall attendance for the month</p>
                <button className="btn-secondary">View</button>
              </div>
              <div className="report-card">
                <div className="report-icon">📈</div>
                <h4>Class Report</h4>
                <p>Attendance by class</p>
                <button className="btn-secondary">View</button>
              </div>
              <div className="report-card">
                <div className="report-icon">⚠️</div>
                <h4>Low Attendance</h4>
                <p>Students below threshold</p>
                <button className="btn-secondary">View</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AttendanceDashboard;
