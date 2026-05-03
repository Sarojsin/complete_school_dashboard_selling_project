import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { addBook } from '../api/library';
import '../../../shared/styles/global.css';
import './styles/library.css';

export default function AddBook() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    isbn: '',
    publisher: '',
    category: '',
    total_copies: 1,
    shelf_location: '',
    price: 0
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await addBook({
        ...formData,
        total_copies: parseInt(formData.total_copies),
        price: parseFloat(formData.price),
        available_copies: parseInt(formData.total_copies)
      });
      alert('Book added successfully!');
      navigate('/library/books');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    'Fiction',
    'Non-Fiction',
    'Science',
    'Mathematics',
    'History',
    'Geography',
    'Literature',
    'Technology',
    'Reference',
    'Other'
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Add New Book</h1>
        <p>Add a new book to the library collection</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form className="book-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Book Information</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label>Title *</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="Enter book title"
              />
            </div>
            <div className="form-group">
              <label>Author *</label>
              <input
                type="text"
                name="author"
                value={formData.author}
                onChange={handleChange}
                required
                placeholder="Enter author name"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>ISBN *</label>
              <input
                type="text"
                name="isbn"
                value={formData.isbn}
                onChange={handleChange}
                required
                placeholder="Enter ISBN"
              />
            </div>
            <div className="form-group">
              <label>Publisher</label>
              <input
                type="text"
                name="publisher"
                value={formData.publisher}
                onChange={handleChange}
                placeholder="Enter publisher name"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Category</label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
              >
                <option value="">Select Category</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Number of Copies *</label>
              <input
                type="number"
                name="total_copies"
                value={formData.total_copies}
                onChange={handleChange}
                min="1"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Shelf Location</label>
              <input
                type="text"
                name="shelf_location"
                value={formData.shelf_location}
                onChange={handleChange}
                placeholder="e.g., A-12, Shelf 3"
              />
            </div>
            <div className="form-group">
              <label>Price</label>
              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleChange}
                min="0"
                step="0.01"
              />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-success" disabled={loading}>
            {loading ? 'Adding...' : 'Add Book'}
          </button>
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => navigate('/library/books')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
