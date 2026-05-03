import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAvailableBooks, getStudentsList, issueBook } from '../api/library';
import '../../../shared/styles/global.css';
import './styles/library.css';

export default function IssueBook() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [books, setBooks] = useState([]);
  const [students, setStudents] = useState([]);
  const [formData, setFormData] = useState({
    book_id: '',
    student_id: '',
    due_date: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [booksRes, studentsRes] = await Promise.all([
        getAvailableBooks(),
        getStudentsList()
      ]);
      setBooks(booksRes.data || []);
      setStudents(studentsRes.data || []);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await issueBook({
        book_id: parseInt(formData.book_id),
        student_id: parseInt(formData.student_id),
        due_date: formData.due_date
      });
      alert('Book issued successfully!');
      navigate('/library');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Calculate default due date (14 days from now)
  const getDefaultDueDate = () => {
    const date = new Date();
    date.setDate(date.getDate() + 14);
    return date.toISOString().split('T')[0];
  };

  const selectedBook = books.find(b => b.id === parseInt(formData.book_id));

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Issue Book</h1>
        <p>Issue a book to a student</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form className="issue-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Issue Details</h3>

          <div className="form-group">
            <label>Select Book *</label>
            <select
              name="book_id"
              value={formData.book_id}
              onChange={handleChange}
              required
            >
              <option value="">Select a book</option>
              {books.map(book => (
                <option key={book.id} value={book.id}>
                  {book.title} by {book.author} (ISBN: {book.isbn})
                </option>
              ))}
            </select>
          </div>

          {selectedBook && (
            <div className="selected-book-info">
              <h4>Book Details:</h4>
              <p><strong>Title:</strong> {selectedBook.title}</p>
              <p><strong>Author:</strong> {selectedBook.author}</p>
              <p><strong>ISBN:</strong> {selectedBook.isbn}</p>
              <p><strong>Available:</strong> {selectedBook.available_copies} copies</p>
            </div>
          )}

          <div className="form-group">
            <label>Select Student *</label>
            <select
              name="student_id"
              value={formData.student_id}
              onChange={handleChange}
              required
            >
              <option value="">Select a student</option>
              {students.map(student => (
                <option key={student.id} value={student.id}>
                  {student.first_name} {student.last_name} - {student.email}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Due Date *</label>
            <input
              type="date"
              name="due_date"
              value={formData.due_date || getDefaultDueDate()}
              onChange={handleChange}
              required
              min={new Date().toISOString().split('T')[0]}
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-success" disabled={loading}>
            {loading ? 'Issuing...' : 'Issue Book'}
          </button>
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => navigate('/library')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
