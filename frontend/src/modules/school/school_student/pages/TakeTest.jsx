import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../../shared/api/client';
import './TakeTest.css';

const TakeTest = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const [test, setTest] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadTest();
  }, [testId]);

  useEffect(() => {
    if (test && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [test, timeLeft]);

  const loadTest = async () => {
    try {
      const response = await api.get(`/student/tests/${testId}`);
      setTest(response.data);
      setTimeLeft(response.data.duration * 60);
    } catch (err) {
      console.error('Failed to load test:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      await api.post(`/student/tests/${testId}/submit`, { answers });
      navigate('/student/tests/results', { state: { testId } });
    } catch (err) {
      console.error('Failed to submit test:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return <div className="test-loading">Loading test...</div>;
  }

  if (!test) {
    return <div className="test-error">Test not found</div>;
  }

  const questions = test.questions || [];
  const question = questions[currentQuestion];

  return (
    <div className="take-test-page">
      <div className="test-header">
        <div className="test-title">
          <h1>{test.title}</h1>
          <p>{test.subject}</p>
        </div>
        <div className="test-timer">
          <span className={`timer ${timeLeft < 300 ? 'warning' : ''}`}>
            ⏱️ {formatTime(timeLeft)}
          </span>
        </div>
        <div className="test-progress">
          Question {currentQuestion + 1} of {questions.length}
        </div>
      </div>

      <div className="test-content">
        <div className="question-container">
          <div className="question-number">
            Question {currentQuestion + 1}
          </div>
          <div className="question-text">
            {question?.text}
          </div>
          <div className="options">
            {question?.options?.map((option, index) => (
              <div 
                key={index}
                className={`option ${answers[question.id] === option ? 'selected' : ''}`}
                onClick={() => handleAnswer(question.id, option)}
              >
                <span className="option-letter">
                  {String.fromCharCode(65 + index)}
                </span>
                <span className="option-text">{option}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="question-navigation">
          <div className="question-dots">
            {questions.map((q, index) => (
              <button
                key={index}
                className={`dot ${index === currentQuestion ? 'current' : ''} ${answers[q.id] ? 'answered' : ''}`}
                onClick={() => setCurrentQuestion(index)}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="test-footer">
        <button 
          className="nav-btn prev"
          onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
          disabled={currentQuestion === 0}
        >
          ← Previous
        </button>
        {currentQuestion === questions.length - 1 ? (
          <button 
            className="submit-btn"
            onClick={handleSubmit}
            disabled={submitting}
          >
            {submitting ? 'Submitting...' : 'Submit Test'}
          </button>
        ) : (
          <button 
            className="nav-btn next"
            onClick={() => setCurrentQuestion(Math.min(questions.length - 1, currentQuestion + 1))}
          >
            Next →
          </button>
        )}
      </div>
    </div>
  );
};

export default TakeTest;
