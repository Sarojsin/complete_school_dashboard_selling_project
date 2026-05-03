import { useState, useEffect } from 'react';
import { getNotes, deleteNote } from '../api/notes';
import './styles/notes.css';

const NotesDashboard = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('all');

  useEffect(() => {
    loadNotes();
  }, [selectedSubject]);

  const loadNotes = async () => {
    try {
      setLoading(true);
      const params = selectedSubject !== 'all' ? { subject: selectedSubject } : {};
      const response = await getNotes(params);
      setNotes(response.data || []);
    } catch (err) {
      console.error('Failed to load notes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (noteId) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        await deleteNote(noteId);
        loadNotes();
      } catch (err) {
        console.error('Failed to delete note:', err);
      }
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getFileIcon = (fileType) => {
    if (fileType?.includes('pdf')) return '📄';
    if (fileType?.includes('powerpoint') || fileType?.includes('ppt')) return '📊';
    if (fileType?.includes('word') || fileType?.includes('document')) return '📝';
    if (fileType?.includes('image')) return '🖼️';
    return '📁';
  };

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    note.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const subjects = [...new Set(notes.map(n => n.subject))];

  if (loading) {
    return <div className="notes-loading">Loading notes...</div>;
  }

  return (
    <div className="notes-dashboard">
      <div className="notes-header">
        <div className="header-content">
          <h1>Study Notes</h1>
          <p>Access and download study materials</p>
        </div>
        <button className="btn-primary">+ Upload Note</button>
      </div>

      <div className="notes-toolbar">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search notes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="filters">
          <select 
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
          >
            <option value="all">All Subjects</option>
            {subjects.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
        </div>
        <div className="view-toggle">
          <button 
            className={viewMode === 'grid' ? 'active' : ''}
            onClick={() => setViewMode('grid')}
          >
            ▦
          </button>
          <button 
            className={viewMode === 'list' ? 'active' : ''}
            onClick={() => setViewMode('list')}
          >
            ☰
          </button>
        </div>
      </div>

      <div className="notes-content">
        {filteredNotes.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📚</span>
            <h3>No Notes Found</h3>
            <p>No notes available for the selected criteria</p>
          </div>
        ) : viewMode === 'grid' ? (
          <div className="notes-grid">
            {filteredNotes.map(note => (
              <div key={note.id} className="note-card">
                <div className="note-icon">
                  {getFileIcon(note.file_type)}
                </div>
                <div className="note-info">
                  <h4>{note.title}</h4>
                  <p className="subject">{note.subject}</p>
                  <p className="description">{note.description}</p>
                </div>
                <div className="note-meta">
                  <span className="date">{formatDate(note.uploaded_at)}</span>
                  <span className="size">{note.file_size}</span>
                </div>
                <div className="note-actions">
                  <button className="btn-download">⬇️ Download</button>
                  <button className="btn-icon" onClick={() => handleDelete(note.id)}>🗑️</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="notes-list">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Subject</th>
                  <th>Uploaded</th>
                  <th>Size</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredNotes.map(note => (
                  <tr key={note.id}>
                    <td>
                      <div className="title-cell">
                        <span className="icon">{getFileIcon(note.file_type)}</span>
                        <span>{note.title}</span>
                      </div>
                    </td>
                    <td>{note.subject}</td>
                    <td>{formatDate(note.uploaded_at)}</td>
                    <td>{note.file_size}</td>
                    <td>
                      <button className="btn-download">⬇️</button>
                      <button className="btn-icon">🗑️</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default NotesDashboard;
