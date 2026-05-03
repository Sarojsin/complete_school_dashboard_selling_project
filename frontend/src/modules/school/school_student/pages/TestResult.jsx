import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../../shared/api/client';
import './TestResult.css';

const TestResult = () => {
  const { testId } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResult();
  }, [testId]);

  const loadResult = async () => {
    try {
      const response = await api.get(`/student/tests/${testId}/result`);
      setResult(response.data);
    } catch (err) {
      console.error('Failed to load result:', err);
    } finally {
      setLoading(false);
    }
  };

  const getGradeColor = (percentage) => {
    if (percentage >= 90) return '#27ae60';
    if (percentage >= 80) return '#2ecc71';
    if (percentage >= 70) return '#3498db';
    if (percentage >= 60) return '#f39c12';
    if (percentage >= 50) return '#e67e22';
    return '#e74c3c';
  };

  const getGrade = (percentage) => {
    if (percentage >= 90) return 'A+';
    if (percentage >= 80) return 'A';
    if (percentage >= 70) return 'B';
    if (percentage >= 60) return 'C';
    if (percentage >= 50) return 'D';
    return 'F';
  };

  if (loading) {
    return <div className="result-loading">Loading result...</div>;
  }

  if (!result) {
    return <div className="result-error">Result not found</div>;
  }

  const percentage = (result.obtained_marks / result.total_marks) * 100;

  return (
    <div className="test-result-page">
      <div className="result-header">
        <div className="result-title">
          <h1>{result.test_title}</h1>
          <p>{result.subject}</p>
        </div>
      </div>

      <div className="result-content">
        <div className="score-card">
          <div 
            className="score-circle"
            style={{ 
              borderColor: getGradeColor(percentage),
              background: `linear-gradient(135deg, ${getGradeColor(percentage)}20 0%, ${getGradeColor(percentage)}10 100%)`
            }}
          >
            <span className="grade" style={{ color: getGradeColor(percentage) }}>
              {getGrade(percentage)}
            </span>
            <span className="percentage">{percentage.toFixed(1)}%</span>
          </div>
          <div className="score-details">
            <div className="detail-item">
              <span className="label">Obtained Marks</span>
              <span className="value">{result.obtained_marks}</span>
            </div>
            <div className="detail-item">
              <span className="label">Total Marks</span>
              <span className="value">{result.total_marks}</span>
            </div>
            <div className="detail-item">
              <span className="label">Correct Answers</span>
              <span className="value">{result.correct_answers}</span>
            </div>
            <div className="detail-item">
              <span className="label">Wrong Answers</span>
              <span className="value">{result.wrong_answers}</span>
            </div>
            <div className="detail-item">
              <span className="label">Time Taken</span>
              <span className="value">{result.time_taken} min</span>
            </div>
          </div>
        </div>

        <div className="questions-review">
          <h2>Question Review</h2>
          {result.questions?.map((q, index) => (
            <div 
              key={index} 
              className={`question-review ${q.is_correct ? 'correct' : 'incorrect'}`}
            >
              <div className="question-number">
                Q{index + 1}
                <span className="status-icon">
                  {q.is_correct ? '✅' : '❌'}
                </span>
              </div>
              <div className="question-text">{q.question}</div>
              <div className="answer-info">
                <p>Your Answer: <span>{q.user_answer || 'Not answered'}</span></p>
                {!q.is_correct && (
                  <p>Correct Answer: <span>{q.correct_answer}</span></p>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="result-actions">
          <Link to="/student/tests" className="back-btn">
            ← Back to Tests
          </Link>
          <button className="retry-btn">Retake Test</button>
        </div>
      </div>
    </div>
  );
};

export default TestResult;
