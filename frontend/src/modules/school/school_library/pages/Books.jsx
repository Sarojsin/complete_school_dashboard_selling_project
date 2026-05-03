import { useEffect, useState } from 'react';
import { getAllBooks, searchBooks, deleteBook } from '../api/library';
import '../../../shared/styles/global.css';
import './styles/library.css';

export default function Books() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const res = await getAllBooks();
      setBooks(res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (searchQuery) {
        const res = await searchBooks(searchQuery);
        setBooks(res.data || []);
      } else {
        await fetchBooks();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (bookId) => {
    if (!window.confirm('Are you sure you want to delete this book?')) return;
    
    try {
      await deleteBook(bookId);
      setBooks(books.filter(b => b.id !== bookId));
      alert('Book deleted successfully!');
    } catch (err) {
      alert('Failed to delete book: ' + err.message);
    }
  };

  const categories = ['all', ...new Set(books.map(b => b.category).filter(Boolean))];

  const filteredBooks = selectedCategory === 'all' 
    ? books 
    : books.filter(b => b.category === selectedCategory);

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Library Books</h1>
        <p>Manage library book collection</p>
      </div>

      {/* Search and Filter */}
      <div className="books-toolbar">
        <form className="search-form" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search books by title, author, or ISBN..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="btn btn-primary">Search</button>
        </form>

        <select 
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="category-filter"
        >
          {categories.map(cat => (
            <option key={cat} value={cat}>
              {cat === 'all' ? 'All Categories' : cat}
            </option>
          ))}
        </select>

        <a href="/library/add-book" className="btn btn-success">
          + Add New Book
        </a>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Books Grid */}
      <div className="books-grid">
        {filteredBooks.length > 0 ? (
          filteredBooks.map((book) => (
            <div key={book.id} className="book-card">
              <div className="book-cover">
                <span className="book-icon">📚</span>
              </div>
              <div className="book-info">
                <h3>{book.title}</h3>
                <p className="book-author">by {book.author}</p>
                <p className="book-isbn">ISBN: {book.isbn}</p>
                <div className="book-meta">
                  <span className="book-category">{book.category}</span>
                  <span className={`availability ${book.available_copies > 0 ? 'available' : 'unavailable'}`}>
                    {book.available_copies} / {book.total_copies} available
                  </span>
                </div>
              </div>
              <div className="book-actions">
                <button 
                  className="btn btn-sm btn-danger"
                  onClick={() => handleDelete(book.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="no-data">
            <p>No books found.</p>
          </div>
        )}
      </div>

      {/* Books Table (Alternative View) */}
      <div className="books-table-container">
        <h2>All Books List</h2>
        <table className="data-table books-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th>Category</th>
              <th>Total</th>
              <th>Available</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredBooks.map((book) => (
              <tr key={book.id}>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.isbn}</td>
                <td>{book.category}</td>
                <td>{book.total_copies}</td>
                <td>
                  <span className={book.available_copies > 0 ? 'text-success' : 'text-danger'}>
                    {book.available_copies}
                  </span>
                </td>
                <td>
                  <button 
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(book.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
