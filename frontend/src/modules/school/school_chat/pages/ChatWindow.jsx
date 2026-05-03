import { useState, useEffect, useRef } from 'react';
import { getMessages, sendMessage, markAsRead } from '../api/chat';
import { useWebSocket } from '../hooks/useWebSocket';
import './styles/chat.css';

const ChatWindow = ({ contact, onBack }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const { messages: wsMessages, connected, sendMessage: wsSendMessage } = useWebSocket(contact?.id);

  useEffect(() => {
    if (contact) {
      loadMessages();
      markAsReadContact();
    }
  }, [contact?.id]);

  useEffect(() => {
    if (wsMessages.length > 0) {
      setMessages((prev) => [...prev, ...wsMessages]);
      scrollToBottom();
    }
  }, [wsMessages]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadMessages = async () => {
    try {
      setLoading(true);
      const response = await getMessages(contact.id);
      setMessages(response.data.messages || []);
    } catch (err) {
      console.error('Failed to load messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const markAsReadContact = async () => {
    try {
      await markAsRead(contact.id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    try {
      setSending(true);
      const messageData = {
        recipient_id: contact.id,
        content: newMessage.trim()
      };

      const response = await sendMessage(messageData);
      setMessages((prev) => [...prev, response.data.message]);
      setNewMessage('');
      
      // Also try WebSocket
      wsSendMessage(newMessage.trim());
      
      inputRef.current?.focus();
    } catch (err) {
      console.error('Failed to send message:', err);
    } finally {
      setSending(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getAvatarUrl = (avatar) => {
    if (!avatar) return '/images/default-avatar.png';
    return avatar.startsWith('http') ? avatar : `/uploads/avatars/${avatar}`;
  };

  const currentUserId = parseInt(localStorage.getItem('user_id') || '0');

  return (
    <div className="chat-window-container">
      <div className="chat-window-header">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <div className="contact-info">
          <img 
            src={getAvatarUrl(contact?.avatar)} 
            alt={contact?.name}
            className="header-avatar"
            onError={(e) => {
              e.target.src = '/images/default-avatar.png';
            }}
          />
          <div>
            <h3>{contact?.name}</h3>
            <span className={`status ${connected ? 'online' : 'offline'}`}>
              {connected ? 'Online' : 'Offline'}
            </span>
          </div>
        </div>
      </div>

      <div className="messages-container">
        {loading ? (
          <div className="messages-loading">Loading messages...</div>
        ) : messages.length === 0 ? (
          <div className="no-messages">
            <p>No messages yet. Start the conversation!</p>
          </div>
        ) : (
          messages.map((message, index) => {
            const isOwn = message.sender_id === currentUserId || message.is_own;
            const showAvatar = index === 0 || 
              messages[index - 1].sender_id !== message.sender_id;

            return (
              <div 
                key={message.id || index} 
                className={`message ${isOwn ? 'sent' : 'received'}`}
              >
                {!isOwn && showAvatar && (
                  <img 
                    src={getAvatarUrl(message.sender_avatar)} 
                    alt="Avatar"
                    className="message-avatar"
                  />
                )}
                <div className="message-bubble">
                  <p>{message.content}</p>
                  <span className="message-time">
                    {formatTime(message.timestamp)}
                    {isOwn && message.read && <span className="read">✓✓</span>}
                  </span>
                </div>
              </div>
            );
          })
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="message-input-container" onSubmit={handleSend}>
        <button type="button" className="attach-btn">
          📎
        </button>
        <input
          ref={inputRef}
          type="text"
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          disabled={sending}
        />
        <button 
          type="submit" 
          className="send-btn"
          disabled={!newMessage.trim() || sending}
        >
          {sending ? '...' : '➤'}
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;
