import { useState, useEffect } from 'react';
import { getGradeSheets } from '../api/examSection';
import './ExamSection.css';

const ExamGradeSheet = () => {
  const [loading, setLoading] = useState(true);
  const [gradeSheets, setGradeSheets] = useState([]);
  const [selectedExam, setSelectedExam] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await getGradeSheets();
      setGradeSheets(response.data || response);
    } catch (err) {
      console.error('Failed to load:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="exam-loading">Loading...</div>;

  return (
    <div className="exam-page">
      <div className="page-header">
        <h1>Grade Sheets</h1>
        <p>View and manage student grade sheets</p>
      </div>

      <div className="exam-card">
        {gradeSheets.length > 0 ? (
          <table className="exam-table">
            <thead>
              <tr>
                <th>Student Name</th>
                <th>Student ID</th>
                <th>Exam</th>
                <th>Marks</th>
                <th>Grade</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {gradeSheets.map((sheet) => (
                <tr key={sheet.id}>
                  <td>{sheet.student_name}</td>
                  <td>{sheet.student_id}</td>
                  <td>{sheet.exam_name}</td>
                  <td>{sheet.marks}/{sheet.total_marks}</td>
                  <td>{sheet.grade}</td>
                  <td><button className="exam-btn">View</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📊</span>
            <p>No grade sheets found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExamGradeSheet;
