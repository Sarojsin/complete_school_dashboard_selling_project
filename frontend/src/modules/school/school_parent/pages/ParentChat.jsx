import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageSquare, 
  Search, 
  Send, 
  Paperclip, 
  MoreVertical, 
  ChevronLeft, 
  UserCircle,
  Clock,
  CheckCheck,
  Phone,
  Video,
  Info,
  Smile
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getChatContacts, getMessages, sendMessage } from '../api/parents';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function ParentChat() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Mocks for visual presentation
  const mockConversations = [
    { id: 1, user_name: 'Dr. Sarah Wilson', user_role: 'Physics Teacher', last_message: 'Alex has shown great progress in the latest lab...', last_message_time: '2024-03-29T10:30:00', unread: 2 },
    { id: 2, user_name: 'Prof. James Bond', user_role: 'Principal', last_message: 'Regarding the upcoming school trip...', last_message_time: '2024-03-28T15:45:00', unread: 0 },
  ];

  const mockMessages = [
    { id: 1, content: 'Hello Dr. Wilson, I wanted to ask about Alex\'s performance in the last test.', is_sent: true, created_at: '2024-03-29T09:00:00' },
    { id: 2, content: 'Hi! Alex did quite well. He scored 94%. We can discuss more in the next PTM.', is_sent: false, created_at: '2024-03-29T09:15:00', sender_name: 'Dr. Sarah Wilson' },
    { id: 3, content: 'That is great news! Thank you.', is_sent: true, created_at: '2024-03-29T09:20:00' },
  ];

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages(selectedConversation.id);
    }
  }, [selectedConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchConversations = async () => {
    try {
      setLoading(true);
      const res = await getChatContacts();
      const convList = res.data?.conversations || mockConversations;
      setConversations(convList);
      if (convList.length > 0) setSelectedConversation(convList[0]);
    } catch (err) {
      console.error('Error fetching conversations:', err);
      setConversations(mockConversations);
      setSelectedConversation(mockConversations[0]);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async (id) => {
    try {
      const res = await getMessages(id);
      setMessages(res.data?.messages || mockMessages);
    } catch (err) {
      setMessages(mockMessages);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedConversation) return;

    const msg = {
      id: Date.now(),
      content: newMessage,
      is_sent: true,
      created_at: new Date().toISOString()
    };

    setMessages([...messages, msg]);
    setNewMessage('');

    try {
      await sendMessage({
        contact_id: selectedConversation.id,
        content: newMessage
      });
    } catch (err) {
      console.error('Failed to send message');
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  if (loading && !conversations.length) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="p-6 lg:p-10 h-[calc(100vh-100px)] overflow-hidden flex flex-col space-y-8"
    >
      {/* Header */}
      <section className="flex items-center justify-between pb-4 border-b border-slate-200 flex-shrink-0">
        <div>
          <Link 
            to="/parent/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-2 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Dashboard
          </Link>
          <div className="flex items-center gap-3">
             <div className="p-2 bg-brand-50 rounded-xl">
                <MessageSquare className="w-6 h-6 text-brand-500" />
             </div>
             <h1 className="text-3xl font-black text-slate-900 tracking-tight">Parent Chat</h1>
          </div>
        </div>
        <div className="flex -space-x-3">
           {[1,2,3].map(i => (
              <div key={i} className="w-10 h-10 rounded-full border-2 border-white bg-slate-100 flex items-center justify-center text-slate-400">
                 <UserCircle className="w-6 h-6" />
              </div>
           ))}
        </div>
      </section>

      {/* Chat Layout */}
      <motion.div variants={containerVariants} className="flex-1 flex gap-8 min-h-0">
        {/* Sidebar: Conversations List */}
        <div className="w-full md:w-80 lg:w-96 flex flex-col gap-6 flex-shrink-0 min-h-0">
           <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input 
                 type="text" 
                 placeholder="Search contacts..." 
                 className="w-full pl-12 pr-6 py-4 bg-white border border-slate-200 rounded-[2rem] text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 shadow-sm transition-all"
              />
           </div>

           <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => setSelectedConversation(conv)}
                  className={cn(
                    "w-full p-4 rounded-3xl flex items-center gap-4 transition-all group border-2",
                    selectedConversation?.id === conv.id 
                    ? "bg-white border-brand-500 shadow-xl shadow-brand-500/10" 
                    : "bg-slate-50/50 border-transparent hover:bg-white hover:border-slate-200"
                  )}
                >
                   <div className="relative">
                      <div className={cn(
                         "w-12 h-12 rounded-2xl flex items-center justify-center transition-colors",
                         selectedConversation?.id === conv.id ? "bg-brand-50 text-brand-500" : "bg-white text-slate-400"
                      )}>
                         <UserCircle className="w-8 h-8" />
                      </div>
                      <div className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-emerald-500 border-2 border-white rounded-full shadow-sm" />
                   </div>
                   
                   <div className="flex-1 text-left min-w-0">
                      <div className="flex justify-between items-center mb-1">
                         <h4 className="text-xs font-black text-slate-900 uppercase truncate pr-2">{conv.user_name}</h4>
                         <span className="text-[9px] font-black text-slate-400 uppercase">{new Date(conv.last_message_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                      <p className="text-[11px] text-slate-500 font-medium truncate italic leading-relaxed">"{conv.last_message}"</p>
                   </div>
                   
                   {conv.unread > 0 && (
                      <div className="w-5 h-5 rounded-full bg-brand-500 flex items-center justify-center text-[10px] font-black text-white shadow-lg shadow-brand-500/20">
                         {conv.unread}
                      </div>
                   )}
                </button>
              ))}
           </div>
        </div>

        {/* Main Chat Area */}
        <div className="hidden md:flex flex-1 flex-col bg-white border border-slate-200 rounded-[3rem] shadow-2xl relative overflow-hidden min-h-0">
           {selectedConversation ? (
              <>
                 {/* Chat Top Bar */}
                 <div className="px-8 py-5 border-b border-slate-100 flex items-center justify-between bg-white/80 backdrop-blur-md sticky top-0 z-20">
                    <div className="flex items-center gap-4">
                       <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
                          <UserCircle className="w-8 h-8" />
                       </div>
                       <div>
                          <h3 className="text-sm font-black text-slate-900 uppercase tracking-tight">{selectedConversation.user_name}</h3>
                          <div className="flex items-center gap-2">
                             <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                             <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{selectedConversation.user_role}</span>
                          </div>
                       </div>
                    </div>
                    <div className="flex items-center gap-2">
                       <button className="p-3 bg-slate-50 text-slate-400 hover:text-brand-500 hover:bg-brand-50 rounded-2xl transition-all shadow-sm">
                          <Phone className="w-4 h-4" />
                       </button>
                       <button className="p-3 bg-slate-50 text-slate-400 hover:text-brand-500 hover:bg-brand-50 rounded-2xl transition-all shadow-sm">
                          <Video className="w-4 h-4" />
                       </button>
                       <button className="p-3 bg-slate-50 text-slate-400 hover:text-brand-500 hover:bg-brand-50 rounded-2xl transition-all shadow-sm">
                          <Info className="w-4 h-4" />
                       </button>
                       <button className="p-3 text-slate-400 hover:text-slate-900 rounded-2xl transition-all">
                          <MoreVertical className="w-5 h-5" />
                       </button>
                    </div>
                 </div>

                 {/* Messages Scrollable Area */}
                 <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar bg-slate-50/30">
                    <AnimatePresence mode="popLayout">
                       {messages.map((msg, idx) => (
                          <motion.div 
                            key={msg.id}
                            initial={{ opacity: 0, y: 10, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            className={cn(
                               "flex w-full group",
                               msg.is_sent ? "justify-end" : "justify-start"
                            )}
                          >
                             <div className={cn(
                                "flex gap-3 max-w-[75%]",
                                msg.is_sent ? "flex-row-reverse" : "flex-row"
                             )}>
                                {!msg.is_sent && (
                                   <div className="w-8 h-8 rounded-xl bg-brand-50 flex-shrink-0 flex items-center justify-center text-brand-500 mt-auto mb-1">
                                      <UserCircle className="w-5 h-5" />
                                   </div>
                                )}
                                <div className="space-y-1">
                                   <div className={cn(
                                      "p-4 px-6 rounded-[2rem] shadow-sm relative group/bubble",
                                      msg.is_sent 
                                      ? "bg-slate-900 text-white rounded-tr-none" 
                                      : "bg-white border border-slate-100 text-slate-700 rounded-tl-none"
                                   )}>
                                      <p className="text-xs font-bold leading-relaxed">{msg.content}</p>
                                   </div>
                                   <div className={cn(
                                      "flex items-center gap-2 px-2",
                                      msg.is_sent ? "justify-end" : "justify-start"
                                   )}>
                                      <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest">
                                         {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                      </span>
                                      {msg.is_sent && <CheckCheck className="w-3.5 h-3.5 text-brand-500" />}
                                   </div>
                                </div>
                             </div>
                          </motion.div>
                       ))}
                    </AnimatePresence>
                    <div ref={messagesEndRef} />
                 </div>

                 {/* Input Area */}
                 <div className="p-8 bg-white border-t border-slate-100 relative z-20">
                    <form 
                      onSubmit={handleSend}
                      className="flex items-center gap-4 bg-slate-50/50 p-2 pl-6 pr-2 rounded-[2.5rem] border border-slate-200 focus-within:ring-2 focus-within:ring-brand-500 transition-all shadow-inner"
                    >
                       <button type="button" className="p-2 text-slate-400 hover:text-brand-500 transition-colors"><Smile className="w-5 h-5" /></button>
                       <input 
                          type="text" 
                          placeholder="Compose message..." 
                          value={newMessage}
                          onChange={(e) => setNewMessage(e.target.value)}
                          className="flex-1 bg-transparent border-none outline-none text-sm font-bold text-slate-700 py-3"
                       />
                       <button type="button" className="p-3 text-slate-400 hover:text-brand-500 transition-colors"><Paperclip className="w-5 h-5" /></button>
                       <button 
                          type="submit"
                          disabled={!newMessage.trim()}
                          className="p-4 bg-brand-500 text-white rounded-[1.75rem] hover:bg-brand-600 shadow-lg shadow-brand-500/20 disabled:scale-90 disabled:opacity-50 transition-all active:scale-95 flex items-center justify-center"
                       >
                          <Send className="w-5 h-5" />
                       </button>
                    </form>
                 </div>
              </>
           ) : (
              <div className="flex-1 flex flex-col items-center justify-center p-20 text-center opacity-50">
                  <div className="p-8 bg-slate-50 rounded-[3rem] mb-6 border border-slate-100">
                     <MessageSquare className="w-16 h-16 text-slate-300" />
                  </div>
                  <h3 className="text-2xl font-black text-slate-900 uppercase">Select a Conversation</h3>
                  <p className="text-xs text-slate-400 font-bold mt-2 uppercase tracking-widest">Ongoing dialogue with faculty members is vital for academic synergy.</p>
              </div>
           )}

           {/* Decorative Elements */}
           <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-brand-500/5 blur-3xl rounded-full" />
        </div>
      </motion.div>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #e2e8f0;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #cbd5e1;
        }
      `}</style>
    </motion.div>
  );
}

// Utility
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}
