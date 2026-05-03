import { useState, useEffect } from 'react';
import { getAcademicData, manageAcademic } from '../api/superadmin';
import './AdminPages.css';

const Academic = () => {
  const [loading, setLoading] = useState(true);
  const [academicData, setAcademicData] = useState(null);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('sessions');

  useEffect(() => {
    loadAcademicData();
  }, []);

  const loadAcademicData = async () => {
    try {
      const response = await getAcademicData();
      setAcademicData(response.data);
    } catch (err) {
      console.error('Failed to load academic data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await manageAcademic(academicData);
      alert('Academic settings saved successfully!');
    } catch (err) {
      console.error('Failed to save:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="admin-loading">Loading academic data...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Academic Management</h1>
        <p>Manage academic sessions, terms, and configurations</p>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'sessions' ? 'active' : ''}`}
          onClick={() => setActiveTab('sessions')}
        >
          Sessions
        </button>
        <button 
          className={`tab ${activeTab === 'terms' ? 'active' : ''}`}
          onClick={() => setActiveTab('terms')}
        >
          Terms
        </button>
        <button 
          className={`tab ${activeTab === 'grades' ? 'active' : ''}`}
          onClick={() => setActiveTab('grades')}
        >
          Grade Levels
        </button>
      </div>

      {activeTab === 'sessions' && (
        <div className="content-card">
          <h3>Academic Sessions</h3>
          <div className="sessions-list">
            {academicData?.sessions?.map((session) => (
              <div key={session.id} className="session-item">
                <div className="session-info">
                  <span className="session-name">{session.name}</span>
                  <span className="session-dates">{session.start_date} - {session.end_date}</span>
                </div>
                <span className={`status-badge ${session.is_active ? 'active' : 'inactive'}`}>
                  {session.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            ))}
          </div>
          <button className="btn-add">+ Add Session</button>
        </div>
      )}

      {activeTab === 'terms' && (
        <div className="content-card">
          <h3>Terms/Semesters</h3>
          <div className="terms-list">
            {academicData?.terms?.map((term) => (
              <div key={term.id} className="term-item">
                <span className="term-name">{term.name}</span>
                <span className="term-dates">{term.start_date} - {term.end_date}</span>
                <span className="term-session">{term.session_name}</span>
              </div>
            ))}
          </div>
          <button className="btn-add">+ Add Term</button>
        </div>
      )}

      {activeTab === 'grades' && (
        <div className="content-card">
          <h3>Grade Levels</h3>
          <div className="grades-list">
            {academicData?.grades?.map((grade) => (
              <div key={grade.id} className="grade-item">
                <span className="grade-name">{grade.name}</span>
                <span className="grade-level">Level {grade.level}</span>
              </div>
            ))}
          </div>
          <button className="btn-add">+ Add Grade</button>
        </div>
      )}
    </div>
  );
};

export default Academic;
