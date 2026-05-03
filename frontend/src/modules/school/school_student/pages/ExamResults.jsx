import { useState, useEffect } from 'react';
import api from '../../../shared/api/client';
import Card from '../../../shared/components/Card';
import Badge from '../../../shared/components/Badge';
import './ExamResults.css';

const ExamResults = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [selectedExam, setSelectedExam] = useState('all');

  // Mock data for demonstration
  const mockResults = [
    { id: 1, subject: 'Mathematics', exam_name: 'Mid-Term 2024', marks_obtained: 92, total_marks: 100, percentage: 92, grade: 'A+', exam_date: '2024-03-15' },
    { id: 2, subject: 'Physics', exam_name: 'Mid-Term 2024', marks_obtained: 85, total_marks: 100, percentage: 85, grade: 'A', exam_date: '2024-03-16' },
    { id: 3, subject: 'Chemistry', exam_name: 'Mid-Term 2024', marks_obtained: 78, total_marks: 100, percentage: 78, grade: 'B+', exam_date: '2024-03-17' },
    { id: 4, subject: 'English', exam_name: 'Mid-Term 2024', marks_obtained: 88, total_marks: 100, percentage: 88, grade: 'A', exam_date: '2024-03-18' },
    { id: 5, subject: 'Computer Science', exam_name: 'Mid-Term 2024', marks_obtained: 95, total_marks: 100, percentage: 95, grade: 'A+', exam_date: '2024-03-19' },
    { id: 6, subject: 'Mathematics', exam_name: 'Unit Test 1', marks_obtained: 88, total_marks: 100, percentage: 88, grade: 'A', exam_date: '2024-02-20' },
    { id: 7, subject: 'Physics', exam_name: 'Unit Test 1', marks_obtained: 82, total_marks: 100, percentage: 82, grade: 'A-', exam_date: '2024-02-21' },
    { id: 8, subject: 'Chemistry', exam_name: 'Unit Test 1', marks_obtained: 75, total_marks: 100, percentage: 75, grade: 'B+', exam_date: '2024-02-22' },
  ];

  // Calculate statistics
  const calculateStats = () => {
    const filtered = filter === 'all' ? mockResults : mockResults.filter(r => r.exam_name === filter);
    const totalMarks = filtered.reduce((sum, r) => sum + r.marks_obtained, 0);
    const avgPercentage = filtered.length ? (totalMarks / filtered.length).toFixed(2) : 0;
    const totalSubjects = filtered.length;
    
    // Calculate GPA (4.0 scale)
    const gradePoints = { 'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0 };
    const gpa = (filtered.reduce((sum, r) => sum + (gradePoints[r.grade] || 0), 0) / filtered.length).toFixed(2);
    
    return { avgPercentage, totalSubjects, gpa, filtered };
  };

  const stats = calculateStats();
  const uniqueExams = [...new Set(mockResults.map(r => r.exam_name))];

  const getGradeColor = (grade) => {
    const colors = {
      'A+': '#27ae60', 'A': '#2ecc71', 'A-': '#82e0aa',
      'B+': '#3498db', 'B': '#5dade2', 'B-': '#85c1e9',
      'C+': '#f39c12', 'C': '#f7dc6f', 'C-': '#f8c471',
      'D': '#e74c3c', 'F': '#c0392b'
    };
    return colors[grade] || '#95a5a6';
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getGradeDistribution = () => {
    const distribution = {};
    stats.filtered.forEach(r => {
      distribution[r.grade] = (distribution[r.grade] || 0) + 1;
    });
    return distribution;
  };

  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      const response = await api.get('/student/exam-results');
      setResults(response.data || mockResults);
    } catch (err) {
      console.error('Failed to load results:', err);
      setResults(mockResults);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="results-loading">Loading results...</div>;
  }

  return (
    <div className="exam-results-page">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>Exam Results</h1>
          <p className="text-muted mb-0">View your examination results, grades and performance</p>
        </div>
        <div className="d-flex gap-2">
          <select 
            className="form-select form-select-sm" 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            style={{ width: 'auto' }}
          >
            <option value="all">All Exams</option>
            {uniqueExams.map(exam => (
              <option key={exam} value={exam}>{exam}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Stats Row */}
      <div className="row g-3 mb-4">
        <div className="col-xl-3 col-md-6">
          <Card className="h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <div className="text-xs fw-bold text-primary text-uppercase mb-1">Overall GPA</div>
                  <div className="h3 mb-0 fw-bold">{stats.gpa}</div>
                  <small className="text-muted">out of 4.0</small>
                </div>
                <i className="bi bi-mortarboard fs-1 text-primary" style={{ opacity: 0.3 }}></i>
              </div>
            </div>
          </Card>
        </div>
        <div className="col-xl-3 col-md-6">
          <Card className="h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <div className="text-xs fw-bold text-success text-uppercase mb-1">Average Score</div>
                  <div className="h3 mb-0 fw-bold">{stats.avgPercentage}%</div>
                  <small className="text-muted">{stats.filtered.length} exams</small>
                </div>
                <i className="bi bi-graph-up-arrow fs-1 text-success" style={{ opacity: 0.3 }}></i>
              </div>
            </div>
          </Card>
        </div>
        <div className="col-xl-3 col-md-6">
          <Card className="h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <div className="text-xs fw-bold text-info text-uppercase mb-1">Subjects</div>
                  <div className="h3 mb-0 fw-bold">{stats.totalSubjects}</div>
                  <small className="text-muted">total subjects</small>
                </div>
                <i className="bi bi-book fs-1 text-info" style={{ opacity: 0.3 }}></i>
              </div>
            </div>
          </Card>
        </div>
        <div className="col-xl-3 col-md-6">
          <Card className="h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <div className="text-xs fw-bold text-warning text-uppercase mb-1">Highest Grade</div>
                  <div className="h3 mb-0 fw-bold">A+</div>
                  <small className="text-muted">Computer Science</small>
                </div>
                <i className="bi bi-trophy fs-1 text-warning" style={{ opacity: 0.3 }}></i>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Grade Distribution & Results Table */}
      <div className="row g-4">
        {/* Grade Distribution */}
        <div className="col-xl-4">
          <Card title="Grade Distribution" icon="pie-chart">
            <div className="grade-distribution">
              {Object.entries(getGradeDistribution()).map(([grade, count]) => (
                <div key={grade} className="grade-item d-flex align-items-center mb-3">
                  <div className="grade-badge-large" style={{ background: getGradeColor(grade) }}>
                    {grade}
                  </div>
                  <div className="flex-grow-1 ms-3">
                    <div className="d-flex justify-content-between mb-1">
                      <span className="small">{grade} Grade</span>
                      <span className="small fw-bold">{count} subject{count > 1 ? 's' : ''}</span>
                    </div>
                    <div className="progress" style={{ height: '6px' }}>
                      <div 
                        className="progress-bar" 
                        style={{ 
                          width: `${(count / stats.filtered.length) * 100}%`,
                          background: getGradeColor(grade)
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Results Table */}
        <div className="col-xl-8">
          <Card title="Exam Results" icon="journal-check">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Subject</th>
                    <th>Exam</th>
                    <th>Marks</th>
                    <th>Percentage</th>
                    <th>Grade</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.filtered.map((result) => (
                    <tr key={result.id}>
                      <td>
                        <div className="d-flex align-items-center">
                          <i className="bi bi-book text-muted me-2"></i>
                          <span className="fw-medium">{result.subject}</span>
                        </div>
                      </td>
                      <td><Badge variant="secondary">{result.exam_name}</Badge></td>
                      <td>
                        <span className="fw-bold">{result.marks_obtained}</span>
                        <span className="text-muted"> / {result.total_marks}</span>
                      </td>
                      <td>
                        <div className="d-flex align-items-center">
                          <div className="progress flex-grow-1 me-2" style={{ height: '6px', width: '60px' }}>
                            <div 
                              className="progress-bar" 
                              style={{ 
                                width: `${result.percentage}%`,
                                background: result.percentage >= 90 ? '#27ae60' : result.percentage >= 80 ? '#2ecc71' : result.percentage >= 70 ? '#3498db' : result.percentage >= 60 ? '#f39c12' : '#e74c3c'
                              }}
                            ></div>
                          </div>
                          <span className="small">{result.percentage}%</span>
                        </div>
                      </td>
                      <td>
                        <span 
                          className="grade-badge"
                          style={{ background: getGradeColor(result.grade), color: '#fff' }}
                        >
                          {result.grade}
                        </span>
                      </td>
                      <td className="text-muted">{formatDate(result.exam_date)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            {/* Pagination */}
            <nav aria-label="Results pagination" className="mt-4">
              <ul className="pagination justify-content-center">
                <li className="page-item disabled">
                  <a className="page-link" href="#">Previous</a>
                </li>
                <li className="page-item active"><a className="page-link" href="#">1</a></li>
                <li className="page-item disabled">
                  <a className="page-link" href="#">Next</a>
                </li>
              </ul>
            </nav>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ExamResults;
