import { useState } from 'react';
import ChatList from './ChatList';
import ChatWindow from './ChatWindow';
import './styles/chat.css';

const ChatDashboard = () => {
  const [selectedContact, setSelectedContact] = useState(null);

  const handleSelectChat = (contact) => {
    setSelectedContact(contact);
  };

  const handleBack = () => {
    setSelectedContact(null);
  };

  return (
    <div className="chat-dashboard">
      <div className={`chat-view ${selectedContact ? 'chat-open' : ''}`}>
        <div className="chat-list-view">
          <ChatList onSelectChat={handleSelectChat} />
        </div>
        
        {selectedContact && (
          <div className="chat-window-view">
            <ChatWindow 
              contact={selectedContact} 
              onBack={handleBack} 
            />
          </div>
        )}
        
        {!selectedContact && (
          <div className="chat-placeholder">
            <div className="placeholder-content">
              <span className="placeholder-icon">💬</span>
              <h3>Select a conversation</h3>
              <p>Choose a contact from the list to start messaging</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatDashboard;
