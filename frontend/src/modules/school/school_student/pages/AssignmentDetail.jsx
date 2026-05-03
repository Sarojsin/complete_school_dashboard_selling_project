import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../../shared/api/client';
import './AssignmentDetail.css';

const AssignmentDetail = () => {
  const { assignmentId } = useParams();
  const [assignment, setAssignment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submission, setSubmission] = useState({ content: '', file: null });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadAssignment();
  }, [assignmentId]);

  const loadAssignment = async () => {
    try {
      const response = await api.get(`/student/assignments/${assignmentId}`);
      setAssignment(response.data);
    } catch (err) {
      console.error('Failed to load assignment:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    setSubmission({ ...submission, file: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('content', submission.content);
      if (submission.file) {
        formData.append('file', submission.file);
      }
      await api.post(`/student/assignments/${assignmentId}/submit`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      loadAssignment();
    } catch (err) {
      console.error('Failed to submit assignment:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: '#f39c12',
      submitted: '#3498db',
      graded: '#27ae60',
      late: '#e74c3c'
    };
    return colors[status] || '#95a5a6';
  };

  if (loading) {
    return <div className="assignment-loading">Loading assignment...</div>;
  }

  if (!assignment) {
    return <div className="assignment-error">Assignment not found</div>;
  }

  return (
    <div className="assignment-detail-page">
      <div className="page-header">
        <h1>{assignment.title}</h1>
        <span 
          className="status-badge"
          style={{ background: getStatusColor(assignment.status) }}
        >
          {assignment.status}
        </span>
      </div>

      <div className="assignment-content">
        <div className="info-card">
          <h2>Assignment Details</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Subject</span>
              <span className="value">{assignment.subject}</span>
            </div>
            <div className="info-item">
              <span className="label">Class</span>
              <span className="value">{assignment.class_name}</span>
            </div>
            <div className="info-item">
              <span className="label">Teacher</span>
              <span className="value">{assignment.teacher_name}</span>
            </div>
            <div className="info-item">
              <span className="label">Due Date</span>
              <span className="value">{formatDate(assignment.due_date)}</span>
            </div>
            <div className="info-item">
              <span className="label">Total Marks</span>
              <span className="value">{assignment.total_marks}</span>
            </div>
            {assignment.obtained_marks !== undefined && (
              <div className="info-item">
                <span className="label">Obtained Marks</span>
                <span className="value">{assignment.obtained_marks}</span>
              </div>
            )}
          </div>
          <div className="description">
            <h3>Description</h3>
            <p>{assignment.description}</p>
          </div>
          {assignment.attachments && assignment.attachments.length > 0 && (
            <div className="attachments">
              <h3>Attachments</h3>
              {assignment.attachments.map((file, index) => (
                <a key={index} href={file.url} className="attachment" download>
                  📎 {file.name}
                </a>
              ))}
            </div>
          )}
        </div>

        <div className="submission-card">
          <h2>Your Submission</h2>
          {assignment.status === 'submitted' || assignment.status === 'graded' ? (
            <div className="submitted-info">
              <p>✅ Submitted on {formatDate(assignment.submitted_at)}</p>
              {assignment.submission_content && (
                <p className="submission-content">{assignment.submission_content}</p>
              )}
              {assignment.submission_file && (
                <a href={assignment.submission_file} className="submission-file" download>
                  📎 View Submitted File
                </a>
              )}
              {assignment.feedback && (
                <div className="feedback">
                  <h3>Teacher Feedback</h3>
                  <p>{assignment.feedback}</p>
                </div>
              )}
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="submission-form">
              <textarea
                placeholder="Enter your answer or comments..."
                value={submission.content}
                onChange={(e) => setSubmission({ ...submission, content: e.target.value })}
                rows="6"
                required
              />
              <div className="file-upload">
                <label>Attach File (optional):</label>
                <input 
                  type="file" 
                  onChange={handleFileChange}
                  accept=".pdf,.doc,.docx,.txt,.zip"
                />
              </div>
              <button 
                type="submit" 
                className="submit-btn"
                disabled={submitting}
              >
                {submitting ? 'Submitting...' : 'Submit Assignment'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default AssignmentDetail;
