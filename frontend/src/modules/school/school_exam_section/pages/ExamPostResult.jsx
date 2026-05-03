import { useState, useEffect } from 'react';
import { getExams, getResults, postResults } from '../api/examSection';
import './ExamSection.css';

const ExamPostResult = () => {
  const [loading, setLoading] = useState(true);
  const [exams, setExams] = useState([]);
  const [results, setResults] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    exam_id: '',
    student_id: '',
    marks: '',
    grade: '',
    remarks: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [examsRes, resultsRes] = await Promise.all([getExams(), getResults()]);
      setExams(examsRes.data || examsRes);
      setResults(resultsRes.data || resultsRes);
    } catch (err) {
      console.error('Failed to load:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await postResults(formData);
      setShowForm(false);
      setFormData({ exam_id: '', student_id: '', marks: '', grade: '', remarks: '' });
      loadData();
    } catch (err) {
      console.error('Failed to post:', err);
    }
  };

  if (loading) return <div className="exam-loading">Loading...</div>;

  return (
    <div className="exam-page">
      <div className="page-header">
        <div>
          <h1>Post Results</h1>
          <p>Publish student exam results</p>
        </div>
        <button className="exam-btn primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Post Result'}
        </button>
      </div>

      {showForm && (
        <div className="exam-card">
          <h3>Post New Result</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Exam</label>
                <select value={formData.exam_id} onChange={(e) => setFormData({...formData, exam_id: e.target.value})} required>
                  <option value="">Select Exam</option>
                  {exams.map((exam) => (
                    <option key={exam.id} value={exam.id}>{exam.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Student ID</label>
                <input type="text" value={formData.student_id} onChange={(e) => setFormData({...formData, student_id: e.target.value})} required />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Marks</label>
                <input type="number" value={formData.marks} onChange={(e) => setFormData({...formData, marks: e.target.value})} required />
              </div>
              <div className="form-group">
                <label>Grade</label>
                <input type="text" value={formData.grade} onChange={(e) => setFormData({...formData, grade: e.target.value})} required />
              </div>
            </div>
            <div className="form-group">
              <label>Remarks</label>
              <textarea value={formData.remarks} onChange={(e) => setFormData({...formData, remarks: e.target.value})} rows={2} />
            </div>
            <button type="submit" className="exam-btn success">Post Result</button>
          </form>
        </div>
      )}

      <div className="exam-card">
        <h3>Results</h3>
        {results.length > 0 ? (
          <table className="exam-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Exam</th>
                <th>Marks</th>
                <th>Grade</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r) => (
                <tr key={r.id}>
                  <td>{r.student_name}</td>
                  <td>{r.exam_name}</td>
                  <td>{r.marks}</td>
                  <td>{r.grade}</td>
                  <td>{r.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <span className="empty-icon">📝</span>
            <p>No results posted</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExamPostResult;
