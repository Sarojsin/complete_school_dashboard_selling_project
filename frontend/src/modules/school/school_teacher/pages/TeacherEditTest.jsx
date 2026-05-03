import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const TeacherEditTest = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [test, setTest] = useState({
    title: '',
    description: '',
    course_id: '',
    test_date: '',
    duration_minutes: '',
    total_marks: '',
    passing_marks: '',
    instructions: '',
    is_published: false
  });
  const [courses, setCourses] = useState([]);
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    loadTest();
    loadCourses();
  }, [testId]);

  const loadTest = async () => {
    try {
      const response = await fetch(`/api/teacher/tests/${testId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setTest({
        ...data,
        test_date: data.test_date ? data.test_date.split('T')[0] : ''
      });
      setQuestions(data.questions || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load test');
      setLoading(false);
    }
  };

  const loadCourses = async () => {
    try {
      const response = await fetch('/api/teacher/courses', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setCourses(data);
    } catch (err) {
      console.error('Failed to load courses');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setTest(prev => ({ 
      ...prev, 
      [name]: type === 'checkbox' ? checked : value 
    }));
  };

  const handleQuestionChange = (index, field, value) => {
    const updatedQuestions = [...questions];
    updatedQuestions[index] = { ...updatedQuestions[index], [field]: value };
    setQuestions(updatedQuestions);
  };

  const addQuestion = () => {
    setQuestions([
      ...questions,
      {
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'a',
        marks: 1
      }
    ]);
  };

  const removeQuestion = (index) => {
    const updatedQuestions = questions.filter((_, i) => i !== index);
    setQuestions(updatedQuestions);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`/api/teacher/tests/${testId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ ...test, questions })
      });

      if (response.ok) {
        setSuccess('Test updated successfully!');
        setTimeout(() => navigate('/teacher/view-tests'), 1500);
      } else {
        setError('Failed to update test');
      }
    } catch (err) {
      setError('An error occurred while updating the test');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading test...</div>;
  }

  return (
    <div className="teacher-edit-test-container">
      <div className="page-header">
        <h1>Edit Test</h1>
        <button onClick={() => navigate('/teacher/view-tests')} className="back-btn">
          ← Back to Tests
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleSubmit} className="test-form">
        <div className="form-section">
          <h3>Test Details</h3>
          
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={test.title}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="course_id">Course *</label>
            <select
              id="course_id"
              name="course_id"
              value={test.course_id}
              onChange={handleChange}
              required
            >
              <option value="">Select Course</option>
              {courses.map(course => (
                <option key={course.id} value={course.id}>
                  {course.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="test_date">Test Date *</label>
              <input
                type="date"
                id="test_date"
                name="test_date"
                value={test.test_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="duration_minutes">Duration (minutes) *</label>
              <input
                type="number"
                id="duration_minutes"
                name="duration_minutes"
                value={test.duration_minutes}
                onChange={handleChange}
                min="1"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="total_marks">Total Marks *</label>
              <input
                type="number"
                id="total_marks"
                name="total_marks"
                value={test.total_marks}
                onChange={handleChange}
                min="0"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="passing_marks">Passing Marks *</label>
              <input
                type="number"
                id="passing_marks"
                name="passing_marks"
                value={test.passing_marks}
                onChange={handleChange}
                min="0"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={test.description}
              onChange={handleChange}
              rows="3"
            />
          </div>

          <div className="form-group">
            <label htmlFor="instructions">Instructions</label>
            <textarea
              id="instructions"
              name="instructions"
              value={test.instructions}
              onChange={handleChange}
              rows="4"
              placeholder="Instructions for students"
            />
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="is_published"
                checked={test.is_published}
                onChange={handleChange}
              />
              Publish Test (Make available to students)
            </label>
          </div>
        </div>

        <div className="form-section">
          <div className="section-header">
            <h3>Questions ({questions.length})</h3>
            <button type="button" onClick={addQuestion} className="btn-add">
              + Add Question
            </button>
          </div>

          {questions.map((question, index) => (
            <div key={index} className="question-card">
              <div className="question-header">
                <span>Question {index + 1}</span>
                <button 
                  type="button" 
                  onClick={() => removeQuestion(index)}
                  className="btn-remove"
                >
                  Remove
                </button>
              </div>
              
              <div className="form-group">
                <label>Question Text *</label>
                <textarea
                  value={question.question_text}
                  onChange={(e) => handleQuestionChange(index, 'question_text', e.target.value)}
                  rows="2"
                  required
                />
              </div>

              <div className="options-grid">
                <div className="option-input">
                  <label>A:</label>
                  <input
                    type="text"
                    value={question.option_a}
                    onChange={(e) => handleQuestionChange(index, 'option_a', e.target.value)}
                    required
                  />
                </div>
                <div className="option-input">
                  <label>B:</label>
                  <input
                    type="text"
                    value={question.option_b}
                    onChange={(e) => handleQuestionChange(index, 'option_b', e.target.value)}
                    required
                  />
                </div>
                <div className="option-input">
                  <label>C:</label>
                  <input
                    type="text"
                    value={question.option_c}
                    onChange={(e) => handleQuestionChange(index, 'option_c', e.target.value)}
                    required
                  />
                </div>
                <div className="option-input">
                  <label>D:</label>
                  <input
                    type="text"
                    value={question.option_d}
                    onChange={(e) => handleQuestionChange(index, 'option_d', e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="question-footer">
                <div className="form-group">
                  <label>Correct Answer</label>
                  <select
                    value={question.correct_answer}
                    onChange={(e) => handleQuestionChange(index, 'correct_answer', e.target.value)}
                  >
                    <option value="a">A</option>
                    <option value="b">B</option>
                    <option value="c">C</option>
                    <option value="d">D</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Marks</label>
                  <input
                    type="number"
                    value={question.marks}
                    onChange={(e) => handleQuestionChange(index, 'marks', e.target.value)}
                    min="1"
                  />
                </div>
              </div>
            </div>
          ))}

          {questions.length === 0 && (
            <div className="no-questions">
              <p>No questions added yet. Click "Add Question" to add questions.</p>
            </div>
          )}
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
          <button 
            type="button" 
            className="btn-secondary"
            onClick={() => navigate('/teacher/view-tests')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default TeacherEditTest;
