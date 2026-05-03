import { useState, useEffect } from 'react';
import { getTimetable, getPeriods } from '../api/timetable';
import './styles/timetable.css';

const TimetableDashboard = () => {
  const [timetable, setTimetable] = useState({});
  const [periods, setPeriods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedClass, setSelectedClass] = useState('all');
  const [viewMode, setViewMode] = useState('week');

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  useEffect(() => {
    loadData();
  }, [selectedClass]);

  const loadData = async () => {
    try {
      setLoading(true);
      const params = selectedClass !== 'all' ? { class: selectedClass } : {};
      const [timetableRes, periodsRes] = await Promise.all([
        getTimetable(params),
        getPeriods()
      ]);
      setTimetable(timetableRes.data || {});
      setPeriods(periodsRes.data || []);
    } catch (err) {
      console.error('Failed to load timetable:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSubjectColor = (subject) => {
    const colors = {
      'Math': '#e74c3c',
      'English': '#3498db',
      'Science': '#27ae60',
      'History': '#9b59b6',
      'Geography': '#f39c12',
      'Physics': '#1abc9c',
      'Chemistry': '#e67e22',
      'Biology': '#2ecc71'
    };
    return colors[subject] || '#95a5a6';
  };

  if (loading) {
    return <div className="timetable-loading">Loading timetable...</div>;
  }

  return (
    <div className="timetable-dashboard">
      <div className="timetable-header">
        <div className="header-content">
          <h1>Class Timetable</h1>
          <p>Weekly schedule and class timings</p>
        </div>
        <div className="header-actions">
          <select 
            value={selectedClass}
            onChange={(e) => setSelectedClass(e.target.value)}
            className="class-select"
          >
            <option value="all">All Classes</option>
            <option value="class1">Class 1</option>
            <option value="class2">Class 2</option>
            <option value="class3">Class 3</option>
          </select>
          <button className="btn-primary">+ Add Class</button>
        </div>
      </div>

      <div className="timetable-tabs">
        <button 
          className={`tab ${viewMode === 'week' ? 'active' : ''}`}
          onClick={() => setViewMode('week')}
        >
          Week View
        </button>
        <button 
          className={`tab ${viewMode === 'day' ? 'active' : ''}`}
          onClick={() => setViewMode('day')}
        >
          Day View
        </button>
      </div>

      <div className="timetable-content">
        <div className="timetable-container">
          <table className="timetable-table">
            <thead>
              <tr>
                <th className="period-col">Period</th>
                {days.map(day => (
                  <th key={day}>{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {periods.length === 0 ? (
                <tr>
                  <td colSpan={days.length + 1} className="empty-cell">
                    No timetable data available
                  </td>
                </tr>
              ) : (
                periods.map((period, periodIndex) => (
                  <tr key={period.id}>
                    <td className="period-cell">
                      <span className="period-number">{periodIndex + 1}</span>
                      <span className="period-time">
                        {period.start_time} - {period.end_time}
                      </span>
                    </td>
                    {days.map(day => {
                      const classData = timetable[day]?.[periodIndex];
                      return (
                        <td key={`${day}-${periodIndex}`}>
                          {classData ? (
                            <div 
                              className="class-block"
                              style={{ background: getSubjectColor(classData.subject) }}
                            >
                              <span className="subject">{classData.subject}</span>
                              <span className="teacher">{classData.teacher}</span>
                            </div>
                          ) : (
                            <div className="empty-slot">-</div>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="timetable-legend">
          <h4>Subject Legend</h4>
          <div className="legend-items">
            {Object.entries({
              'Math': '#e74c3c',
              'English': '#3498db',
              'Science': '#27ae60',
              'History': '#9b59b6',
              'Geography': '#f39c12',
              'Physics': '#1abc9c'
            }).map(([subject, color]) => (
              <div key={subject} className="legend-item">
                <span className="legend-color" style={{ background: color }}></span>
                <span>{subject}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimetableDashboard;
