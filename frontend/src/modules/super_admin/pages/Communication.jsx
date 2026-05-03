import { useState, useEffect } from 'react';
import { getCommunications, sendCommunication } from '../api/superadmin';
import './AdminPages.css';

const Communication = () => {
  const [communications, setCommunications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    type: 'email',
    subject: '',
    message: '',
    recipients: 'all',
    priority: 'normal'
  });

  useEffect(() => {
    loadCommunications();
  }, []);

  const loadCommunications = async () => {
    try {
      const response = await getCommunications();
      setCommunications(response.data);
    } catch (err) {
      console.error('Failed to load communications:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    try {
      await sendCommunication(formData);
      setShowForm(false);
      setFormData({
        type: 'email',
        subject: '',
        message: '',
        recipients: 'all',
        priority: 'normal'
      });
      loadCommunications();
    } catch (err) {
      console.error('Failed to send:', err);
    }
  };

  const getTypeIcon = (type) => {
    const icons = {
      email: '📧',
      sms: '💬',
      push: '🔔',
      notification: '📢'
    };
    return icons[type] || '📧';
  };

  if (loading) {
    return <div className="admin-loading">Loading communications...</div>;
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <div>
          <h1>Communication Center</h1>
          <p>Send messages to users across the platform</p>
        </div>
        <button className="btn-add" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Message'}
        </button>
      </div>

      {showForm && (
        <div className="content-card">
          <div className="communication-form">
            <h3>Send New Message</h3>
            <form onSubmit={handleSend}>
              <div className="form-group">
                <label>Message Type</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                >
                  <option value="email">Email</option>
                  <option value="sms">SMS</option>
                  <option value="push">Push Notification</option>
                  <option value="notification">In-App Notification</option>
                </select>
              </div>

              <div className="form-group">
                <label>Subject</label>
                <input
                  type="text"
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Recipients</label>
                <select
                  value={formData.recipients}
                  onChange={(e) => setFormData({...formData, recipients: e.target.value})}
                >
                  <option value="all">All Users</option>
                  <option value="students">All Students</option>
                  <option value="teachers">All Teachers</option>
                  <option value="parents">All Parents</option>
                  <option value="staff">Staff Only</option>
                </select>
              </div>

              <div className="form-group">
                <label>Priority</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: e.target.value})}
                >
                  <option value="low">Low</option>
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              <div className="form-group">
                <label>Message</label>
                <textarea
                  value={formData.message}
                  onChange={(e) => setFormData({...formData, message: e.target.value})}
                  rows={6}
                  required
                />
              </div>

              <button type="submit" className="btn-submit">Send Message</button>
            </form>
          </div>
        </div>
      )}

      <div className="content-card">
        <h3>Communication History</h3>
        {communications.length > 0 ? (
          <table className="data-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Subject</th>
                <th>Recipients</th>
                <th>Sent</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {communications.map((comm) => (
                <tr key={comm.id}>
                  <td>
                    <span className="type-icon">{getTypeIcon(comm.type)}</span>
                  </td>
                  <td>{comm.subject}</td>
                  <td>{comm.recipients}</td>
                  <td>{comm.sent_at}</td>
                  <td>
                    <span className={`status-badge ${comm.status}`}>
                      {comm.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="empty-text">No communications sent yet</p>
        )}
      </div>
    </div>
  );
};

export default Communication;
