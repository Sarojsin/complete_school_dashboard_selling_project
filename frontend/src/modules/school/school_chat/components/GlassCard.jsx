// =====================
// GLASSCARD - Chat Module
// =====================

import { motion } from 'framer-motion';

// Base GlassCard
export const GlassCard = ({ children, className = '', padding = 'md' }) => {
  const paddings = { none: '', sm: 'p-3', md: 'p-4', lg: 'p-6' };
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
      className={`bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl ${paddings[padding]} ${className}`}>
      {children}
    </motion.div>
  );
};

// Chat Contact Item
export const ChatContactItem = ({ contact, isSelected, onClick, unreadCount = 0, isOnline = false, lastMessage, lastMessageTime, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay }}
    onClick={onClick} whileHover={{ backgroundColor: 'rgba(255,255,255,0.05)' }}
    className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${isSelected ? 'bg-primary-500/20 border border-primary-500/30' : ''}`}>
    <div className="relative">
      <div className="h-12 w-12 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center text-white font-semibold">
        {contact?.name?.charAt(0) || 'U'}
      </div>
      {isOnline && <div className="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-emerald-500 border-2 border-slate-800" />}
    </div>
    <div className="flex-1 min-w-0">
      <div className="flex items-center justify-between mb-1">
        <h4 className="text-white font-medium truncate">{contact?.name || 'User'}</h4>
        {lastMessageTime && <span className="text-white/40 text-xs">{lastMessageTime}</span>}
      </div>
      <div className="flex items-center justify-between">
        <p className="text-white/50 text-sm truncate">{lastMessage || 'No messages yet'}</p>
        {unreadCount > 0 && (
          <span className="min-w-[20px] h-5 flex items-center justify-center rounded-full bg-primary-500 text-white text-xs font-medium">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </div>
    </div>
  </motion.div>
);

// Message Bubble
export const MessageBubble = ({ message, isOwn, showAvatar = true, avatar }) => {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
      className={`flex ${isOwn ? 'justify-end' : 'justify-start'} mb-3`}>
      <div className={`flex items-end gap-2 max-w-[70%] ${isOwn ? 'flex-row-reverse' : ''}`}>
        {!isOwn && showAvatar && (
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex-shrink-0 flex items-center justify-center text-white text-xs font-medium">
            {avatar?.charAt(0) || 'U'}
          </div>
        )}
        <div className={`px-4 py-2 rounded-2xl ${isOwn ? 'bg-primary-600 text-white rounded-br-md' : 'bg-white/10 text-white rounded-bl-md'}`}>
          <p className="text-sm">{message?.content || ''}</p>
          <div className={`flex items-center gap-1 mt-1 ${isOwn ? 'justify-end' : ''}`}>
            <span className="text-xs text-white/50">{message?.time || ''}</span>
            {isOwn && message?.read && <span className="text-xs text-emerald-400">✓✓</span>}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Online Status Indicator
export const OnlineStatus = ({ isOnline, size = 'md' }) => {
  const sizes = { sm: 'w-2 h-2', md: 'w-3 h-3', lg: 'w-4 h-4' };
  return (
    <div className={`${sizes[size]} rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-slate-500'} ${isOnline ? 'animate-pulse' : ''}`} />
  );
};

// Chat Group Card
export const ChatGroupCard = ({ group, onClick, memberCount = 0, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }}
    onClick={onClick} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
    className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4 cursor-pointer hover:border-white/20 transition-all">
    <div className="flex items-center gap-3 mb-3">
      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center">
        <span className="text-white font-bold text-lg">{group?.name?.charAt(0) || 'G'}</span>
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="text-white font-medium truncate">{group?.name || 'Group'}</h4>
        <p className="text-white/50 text-sm">{memberCount} members</p>
      </div>
    </div>
    {group?.lastMessage && (
      <p className="text-white/60 text-sm truncate">{group.lastMessage}</p>
    )}
  </motion.div>
);

// Input Field
export const ChatInput = ({ value, onChange, onSend, placeholder = 'Type a message...', disabled = false }) => (
  <div className="flex items-center gap-2 p-3 bg-white/5 rounded-xl border border-white/10">
    <input type="text" value={value} onChange={onChange} placeholder={placeholder} disabled={disabled}
      className="flex-1 bg-transparent text-white placeholder-white/40 focus:outline-none text-sm"
      onKeyPress={(e) => e.key === 'Enter' && onSend?.()} />
    <button onClick={onSend} disabled={disabled || !value?.trim()} 
      className="p-2 rounded-lg bg-primary-600 text-white hover:bg-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
      </svg>
    </button>
  </div>
);

// Typing Indicator
export const TypingIndicator = ({ users = [] }) => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-1 p-3">
    <div className="flex items-center gap-1 px-3 py-2 rounded-2xl bg-white/10">
      {[0, 1, 2].map((i) => (
        <motion.div key={i} initial={{ opacity: 0.3 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.15, duration: 0.5, repeat: Infinity, repeatType: 'reverse' }}
          className="w-2 h-2 rounded-full bg-white/60" />
      ))}
    </div>
    <span className="text-white/50 text-sm ml-2">
      {users.length > 0 ? `${users.join(', ')} is typing...` : 'Typing...'}
    </span>
  </motion.div>
);

// Unread Badge
export const UnreadBadge = ({ count }) => {
  if (count <= 0) return null;
  return (
    <span className="min-w-[20px] h-5 flex items-center justify-center px-1.5 rounded-full bg-primary-500 text-white text-xs font-medium">
      {count > 99 ? '99+' : count}
    </span>
  );
};

// Action Button
export const ChatActionButton = ({ icon: Icon, label, onClick, variant = 'default', size = 'md' }) => {
  const variants = { default: 'bg-white/10 hover:bg-white/20', primary: 'bg-primary-600 hover:bg-primary-500', danger: 'bg-red-600/80 hover:bg-red-600' };
  const sizes = { sm: 'p-1.5', md: 'p-2', lg: 'p-3' };
  return (
    <button onClick={onClick} title={label}
      className={`rounded-lg text-white/70 hover:text-white transition-colors ${variants[variant]} ${sizes[size]}`}>
      {Icon && <Icon className="w-5 h-5" />}
    </button>
  );
};

// Empty State
export const EmptyChatState = ({ title = 'No conversations yet', description = 'Start a new conversation', action }) => (
  <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} 
    className="flex flex-col items-center justify-center h-full p-8 text-center">
    <div className="w-24 h-24 mb-6 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center">
      <svg className="w-12 h-12 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
    </div>
    <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
    <p className="text-white/50 max-w-sm mb-6">{description}</p>
    {action && <button className="bg-primary-600 hover:bg-primary-500 text-white font-medium py-2 px-6 rounded-xl transition-colors">{action}</button>}
  </motion.div>
);

// Search Input
export const ChatSearchInput = ({ value, onChange, placeholder = 'Search chats...' }) => (
  <div className="relative">
    <input type="text" value={value} onChange={onChange} placeholder={placeholder}
      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 pl-10 text-white placeholder-white/40 focus:outline-none focus:border-primary-500/50 transition-colors text-sm" />
    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  </div>
);

// Modal
export const ChatModal = ({ isOpen, onClose, title, children, size = 'md' }) => {
  if (!isOpen) return null;
  const sizes = { sm: 'max-w-md', md: 'max-w-lg', lg: 'max-w-2xl', xl: 'max-w-4xl' };
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
      <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }}
        onClick={(e) => e.stopPropagation()} className={`bg-gradient-to-br from-slate-800/95 to-slate-900/95 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl w-full ${sizes[size]} max-h-[90vh] overflow-auto`}>
        {title && <div className="p-4 border-b border-white/10"><h2 className="text-lg font-semibold text-white">{title}</h2></div>}
        <div className="p-4">{children}</div>
      </motion.div>
    </motion.div>
  );
};

export default { 
  GlassCard, 
  ChatContactItem, 
  MessageBubble, 
  OnlineStatus, 
  ChatGroupCard, 
  ChatInput, 
  TypingIndicator, 
  UnreadBadge, 
  ChatActionButton, 
  EmptyChatState, 
  ChatSearchInput, 
  ChatModal 
};
