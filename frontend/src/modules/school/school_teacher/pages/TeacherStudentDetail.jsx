import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getStudentDetails, getStudentGrades } from '../api/teachers';
import './TeacherPortal.css';

const TeacherStudentDetail = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [student, setStudent] = useState(null);
  const [grades, setGrades] = useState([]);

  useEffect(() => {
    loadData();
  }, [studentId]);

  const loadData = async () => {
    try {
      const [studentRes, gradesRes] = await Promise.all([
        getStudentDetails(studentId),
        getStudentGrades(studentId)
      ]);
      setStudent(studentRes.data || studentRes);
      setGrades(gradesRes.data || gradesRes);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="teacher-loading">Loading student details...</div>;
  }

  return (
    <div className="teacher-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1>{student?.name}</h1>
        <p>Student ID: {student?.id}</p>
      </div>

      <div className="teacher-card">
        <h3>Student Information</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Name</label>
            <span>{student?.name}</span>
          </div>
          <div className="form-group">
            <label>Email</label>
            <span>{student?.email || 'N/A'}</span>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Phone</label>
            <span>{student?.phone || 'N/A'}</span>
          </div>
          <div className="form-group">
            <label>Grade/Class</label>
            <span>{student?.grade || 'N/A'}</span>
          </div>
        </div>
      </div>

      <div className="teacher-card" style={{marginTop: '20px'}}>
        <h3>Grades</h3>
        {grades.length > 0 ? (
          <table className="teacher-table">
            <thead>
              <tr>
                <th>Course</th>
                <th>Grade</th>
                <th>Remarks</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {grades.map((grade) => (
                <tr key={grade.id}>
                  <td>{grade.course_name}</td>
                  <td>{grade.grade}</td>
                  <td>{grade.remarks || '-'}</td>
                  <td>{grade.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📝</span>
            <p>No grades found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherStudentDetail;
