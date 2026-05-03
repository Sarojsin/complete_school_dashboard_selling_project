import { useState, useEffect } from 'react';
import { getTeacherTimetable } from '../api/teachers';
import './TeacherPortal.css';

const TeacherTimetable = () => {
  const [loading, setLoading] = useState(true);
  const [timetable, setTimetable] = useState([]);

  useEffect(() => {
    loadTimetable();
  }, []);

  const loadTimetable = async () => {
    try {
      const response = await getTeacherTimetable();
      setTimetable(response.data || response);
    } catch (err) {
      console.error('Failed to load timetable:', err);
    } finally {
      setLoading(false);
    }
  };

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const timeSlots = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'];

  if (loading) {
    return <div className="teacher-loading">Loading timetable...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <h1>My Timetable</h1>
        <p>Weekly teaching schedule</p>
      </div>

      <div className="teacher-card">
        <div className="timetable-container">
          <table className="teacher-table timetable">
            <thead>
              <tr>
                <th>Time</th>
                {days.map((day) => (
                  <th key={day}>{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {timeSlots.map((time) => (
                <tr key={time}>
                  <td className="time-slot">{time}</td>
                  {days.map((day) => {
                    const class_ = timetable.find(
                      t => t.day === day && t.start_time === time
                    );
                    return (
                      <td key={day} className={class_ ? 'has-class' : ''}>
                        {class_ ? (
                          <div className="class-info">
                            <span className="subject">{class_.course_name}</span>
                            <span className="room">{class_.room || 'TBD'}</span>
                          </div>
                        ) : (
                          '-'
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TeacherTimetable;
