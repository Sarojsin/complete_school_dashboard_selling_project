import { useState, useEffect } from 'react';
import { getChatContacts, getUnreadCount } from '../api/chat';
import './styles/chat.css';

const ChatList = ({ onSelectChat }) => {
  const [contacts, setContacts] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadContacts();
    loadUnreadCount();
  }, []);

  const loadContacts = async () => {
    try {
      setLoading(true);
      const response = await getChatContacts();
      setContacts(response.data);
    } catch (err) {
      setError('Failed to load contacts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadUnreadCount = async () => {
    try {
      const response = await getUnreadCount();
      setUnreadCount(response.data.count);
    } catch (err) {
      console.error(err);
    }
  };

  const filteredContacts = contacts.filter(contact =>
    contact.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getAvatarUrl = (avatar) => {
    if (!avatar) return '/images/default-avatar.png';
    return avatar.startsWith('http') ? avatar : `/uploads/avatars/${avatar}`;
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return <div className="chat-loading">Loading chats...</div>;
  }

  if (error) {
    return <div className="chat-error">{error}</div>;
  }

  return (
    <div className="chat-list-container">
      <div className="chat-header">
        <h2>Messages</h2>
        {unreadCount > 0 && (
          <span className="unread-badge">{unreadCount}</span>
        )}
      </div>

      <div className="chat-search">
        <input
          type="text"
          placeholder="Search conversations..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <i className="search-icon">🔍</i>
      </div>

      <div className="chat-contacts">
        {filteredContacts.length === 0 ? (
          <div className="no-contacts">
            <p>No conversations yet</p>
            <button onClick={loadContacts}>Refresh</button>
          </div>
        ) : (
          filteredContacts.map((contact) => (
            <div
              key={contact.id}
              className={`chat-contact ${contact.unread > 0 ? 'unread' : ''}`}
              onClick={() => onSelectChat(contact)}
            >
              <div className="contact-avatar">
                <img 
                  src={getAvatarUrl(contact.avatar)} 
                  alt={contact.name}
                  onError={(e) => {
                    e.target.src = '/images/default-avatar.png';
                  }}
                />
                {contact.online && <span className="online-indicator"></span>}
              </div>
              <div className="contact-info">
                <div className="contact-header">
                  <h3>{contact.name}</h3>
                  <span className="last-time">
                    {formatTime(contact.last_message_time)}
                  </span>
                </div>
                <p className="last-message">
                  {contact.last_message?.substring(0, 50)}
                  {contact.last_message?.length > 50 ? '...' : ''}
                </p>
                {contact.unread > 0 && (
                  <span className="message-count">{contact.unread}</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ChatList;
