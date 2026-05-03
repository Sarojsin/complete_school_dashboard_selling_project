import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getNotices, updateNotice, deleteNotice } from '../../api/authority';
import './AuthorityNotices.css';

const AuthorityViewNotice = () => {
  const { noticeId } = useParams();
  const navigate = useNavigate();
  const [notices, setNotices] = useState([]);
  const [selectedNotice, setSelectedNotice] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadNotices();
  }, []);

  const loadNotices = async () => {
    try {
      const response = await getNotices();
      setNotices(response.data);
      if (noticeId) {
        const notice = response.data.find(n => n.id === parseInt(noticeId));
        setSelectedNotice(notice);
      }
    } catch (err) {
      console.error('Failed to load notices:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this notice?')) {
      try {
        await deleteNotice(id);
        loadNotices();
        setSelectedNotice(null);
      } catch (err) {
        console.error('Failed to delete notice:', err);
      }
    }
  };

  const getPriorityBadge = (priority) => {
    const badges = {
      high: { class: 'high', text: 'High Priority' },
      medium: { class: 'medium', text: 'Medium' },
      low: { class: 'low', text: 'Low' }
    };
    return badges[priority] || badges.medium;
  };

  if (loading) {
    return <div className="notices-loading">Loading notices...</div>;
  }

  return (
    <div className="authority-notices-page">
      <div className="page-header">
        <h1>Notices</h1>
        <p>View and manage school notices</p>
      </div>

      <div className="notices-layout">
        <div className="notices-list-card">
          <h3>All Notices</h3>
          {notices.length > 0 ? (
            <div className="notices-list">
              {notices.map((notice) => (
                <div 
                  key={notice.id} 
                  className={`notice-item ${selectedNotice?.id === notice.id ? 'active' : ''}`}
                  onClick={() => setSelectedNotice(notice)}
                >
                  <div className="notice-item-header">
                    <span className={`priority-badge ${getPriorityBadge(notice.priority).class}`}>
                      {getPriorityBadge(notice.priority).text}
                    </span>
                    <span className="notice-date">{notice.created_at}</span>
                  </div>
                  <h4>{notice.title}</h4>
                  <p>{notice.content?.substring(0, 100)}...</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <span className="empty-icon">📋</span>
              <p>No notices found</p>
            </div>
          )}
        </div>

        <div className="notice-detail-card">
          {selectedNotice ? (
            <>
              <div className="notice-detail-header">
                <button className="back-btn" onClick={() => navigate(-1)}>
                  ← Back
                </button>
                <div className="notice-actions">
                  <button className="btn-edit" onClick={() => navigate(`/authority/notices/edit/${selectedNotice.id}`)}>
                    Edit
                  </button>
                  <button className="btn-delete" onClick={() => handleDelete(selectedNotice.id)}>
                    Delete
                  </button>
                </div>
              </div>
              
              <div className="notice-detail-content">
                <span className={`priority-badge ${getPriorityBadge(selectedNotice.priority).class}`}>
                  {getPriorityBadge(selectedNotice.priority).text}
                </span>
                
                <h1>{selectedNotice.title}</h1>
                
                <div className="notice-meta">
                  <span>Posted: {selectedNotice.created_at}</span>
                  <span>By: {selectedNotice.author_name || 'Administrator'}</span>
                  {selectedNotice.target_audience && (
                    <span>Audience: {selectedNotice.target_audience}</span>
                  )}
                </div>

                <div className="notice-body">
                  {selectedNotice.content}
                </div>

                {selectedNotice.attachments && selectedNotice.attachments.length > 0 && (
                  <div className="notice-attachments">
                    <h4>Attachments</h4>
                    <div className="attachments-list">
                      {selectedNotice.attachments.map((file, index) => (
                        <a key={index} href={file.url} className="attachment-item">
                          📎 {file.name}
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <span className="empty-icon">👈</span>
              <p>Select a notice to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthorityViewNotice;
