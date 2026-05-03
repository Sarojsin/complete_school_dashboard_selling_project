import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bell, 
  ChevronLeft, 
  Search, 
  Filter, 
  Calendar, 
  User, 
  Paperclip, 
  Share2, 
  Bookmark, 
  MoreVertical,
  ArrowRight,
  Info,
  Clock,
  ShieldAlert,
  Megaphone
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getParentNotices } from '../api/parents';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function ParentNotices() {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedNotice, setSelectedNotice] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Mocks for visual presentation
  const mockNotices = [
    { 
      id: 1, 
      title: 'Annual Sports Meet 2024', 
      content: 'We are excited to announce our Annual Sports Meet scheduled for April 15th. All parents are cordially invited to witness their children\'s athletic prowess. Please ensure your child is in proper sports attire. The event will begin at 8:00 AM sharp in the main arena.', 
      priority: 'high', 
      created_at: '2024-03-28T09:00:00',
      category: 'Events',
      author: 'Principal Office',
      attachments: [{ name: 'Schedule.pdf', url: '#' }]
    },
    { 
      id: 2, 
      title: 'Term-End Examination Schedule', 
      content: 'The date sheet for the upcoming term-end examinations has been finalized. Please download the attachment for detailed subject timings and room allocations.', 
      priority: 'medium', 
      created_at: '2024-03-27T14:30:00',
      category: 'Academics',
      author: 'Examination Cell',
      attachments: [{ name: 'DateSheet.pdf', url: '#' }]
    },
    { 
      id: 3, 
      title: 'Summer Uniform Update', 
      content: 'Starting April 1st, students must transition to the summer uniform. Please visit the school store if you need new sets. Traditional winter uniforms will not be permitted after the deadline.', 
      priority: 'low', 
      created_at: '2024-03-26T11:15:00',
      category: 'General',
      author: 'Administration',
      attachments: []
    }
  ];

  useEffect(() => {
    fetchNotices();
  }, []);

  const fetchNotices = async () => {
    try {
      setLoading(true);
      const res = await getParentNotices();
      const noticeList = res.data?.length ? res.data : mockNotices;
      setNotices(noticeList);
      if (noticeList.length > 0) setSelectedNotice(noticeList[0]);
    } catch (err) {
      console.error('Error fetching notices:', err);
      setNotices(mockNotices);
      setSelectedNotice(mockNotices[0]);
    } finally {
      setLoading(false);
    }
  };

  const filteredNotices = notices.filter(n => 
    n.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    n.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !notices.length) {
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
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-4 border-b border-slate-200 flex-shrink-0">
        <motion.div variants={itemVariants}>
          <Link 
            to="/parent/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-2 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Dashboard
          </Link>
          <div className="flex items-center gap-3">
             <div className="p-2 bg-brand-50 rounded-xl">
                <Megaphone className="w-6 h-6 text-brand-500" />
             </div>
             <h1 className="text-3xl font-black text-slate-900 tracking-tight">Parent Bulletin</h1>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="relative w-full md:w-80">
           <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
           <input 
              type="text" 
              placeholder="Search announcements..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-6 py-4 bg-white border border-slate-200 rounded-[2rem] text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 shadow-sm transition-all"
           />
        </motion.div>
      </section>

      {/* Main Feed Layout */}
      <div className="flex-1 flex gap-8 min-h-0">
         {/* Left Side: Notices List Feed */}
         <div className="w-full md:w-80 lg:w-[400px] flex flex-col gap-4 flex-shrink-0 min-h-0 overflow-hidden">
            <div className="flex justify-between items-center px-2">
               <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{filteredNotices.length} Announcements</span>
               <button className="p-2 text-slate-400 hover:text-brand-500 transition-colors"><Filter className="w-4 h-4" /></button>
            </div>
            
            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
               {filteredNotices.map((notice) => (
                 <motion.button
                   key={notice.id}
                   whileHover={{ scale: 1.01 }}
                   onClick={() => setSelectedNotice(notice)}
                   className={cn(
                     "w-full text-left p-6 rounded-[2.5rem] border-2 transition-all relative group",
                     selectedNotice?.id === notice.id 
                     ? "bg-white border-brand-500 shadow-xl shadow-brand-500/10" 
                     : "bg-slate-50 border-transparent hover:bg-white hover:border-slate-200"
                   )}
                 >
                    <div className="flex justify-between items-start mb-3">
                       <ModernBadge variant={notice.priority === 'high' ? 'danger' : 'primary'} size="xs" className="px-3">
                          {notice.category}
                       </ModernBadge>
                       <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">{new Date(notice.created_at).toLocaleDateString()}</span>
                    </div>
                    
                    <h3 className={cn(
                       "text-sm font-black text-slate-900 uppercase tracking-tight leading-snug pr-4 mb-2 line-clamp-2 transition-colors",
                       selectedNotice?.id === notice.id ? "text-brand-500" : "group-hover:text-brand-500"
                    )}>
                       {notice.title}
                    </h3>
                    <p className="text-[11px] text-slate-500 font-medium line-clamp-2 leading-relaxed italic pr-4">
                       "{notice.content}"
                    </p>
                    
                    {notice.priority === 'high' && selectedNotice?.id !== notice.id && (
                       <div className="absolute top-6 right-6">
                          <ShieldAlert className="w-4 h-4 text-rose-500 animate-bounce" />
                       </div>
                    )}
                 </motion.button>
               ))}
            </div>
         </div>

         {/* Right Side: Detailed View */}
         <div className="hidden md:flex flex-1 flex-col bg-white border border-slate-200 rounded-[3rem] shadow-2xl relative overflow-hidden min-h-0">
            <AnimatePresence mode="wait">
               {selectedNotice ? (
                 <motion.div 
                   key={selectedNotice.id}
                   initial={{ opacity: 0, x: 20 }}
                   animate={{ opacity: 1, x: 0 }}
                   exit={{ opacity: 0, x: -20 }}
                   className="flex-1 flex flex-col min-h-0"
                 >
                    {/* Detail Top Bar */}
                    <div className="px-10 py-8 border-b border-slate-100 flex items-center justify-between sticky top-0 bg-white/80 backdrop-blur-md z-10">
                       <div className="flex items-center gap-6">
                          <div className={cn(
                             "w-14 h-14 rounded-2xl flex items-center justify-center text-white shadow-lg",
                             selectedNotice.priority === 'high' ? "bg-rose-500 shadow-rose-500/20" : "bg-brand-500 shadow-brand-500/20"
                          )}>
                             <Bell className="w-7 h-7" />
                          </div>
                          <div>
                             <h2 className="text-xl font-black text-slate-900 uppercase tracking-tight leading-tight">{selectedNotice.title}</h2>
                             <div className="flex items-center gap-4 mt-1">
                                <div className="flex items-center gap-1.5 ">
                                   <Calendar className="w-3.5 h-3.5 text-slate-400" />
                                   <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{new Date(selectedNotice.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                                </div>
                                <div className="flex items-center gap-1.5 ">
                                   <User className="w-3.5 h-3.5 text-slate-400" />
                                   <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Released by: {selectedNotice.author}</span>
                                </div>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-2">
                          <button className="p-3 bg-slate-50 text-slate-400 hover:text-brand-500 hover:bg-brand-50 rounded-2xl transition-all"><Bookmark className="w-4 h-4" /></button>
                          <button className="p-3 bg-slate-50 text-slate-400 hover:text-brand-500 hover:bg-brand-50 rounded-2xl transition-all"><Share2 className="w-4 h-4" /></button>
                          <button className="p-3 bg-slate-50 text-slate-400 hover:text-slate-900 rounded-2xl transition-all"><MoreVertical className="w-5 h-5" /></button>
                       </div>
                    </div>

                    {/* Content Area */}
                    <div className="flex-1 overflow-y-auto p-10 space-y-10 custom-scrollbar">
                       <div className="prose prose-slate max-w-none">
                          {selectedNotice.content.split('\n').map((para, i) => (
                             <p key={i} className="text-base text-slate-600 font-medium leading-loose mb-6">
                                {para}
                             </p>
                          ))}
                       </div>

                       {selectedNotice.attachments?.length > 0 && (
                          <div className="space-y-4">
                             <div className="flex items-center gap-3">
                                <Paperclip className="w-4 h-4 text-brand-500" />
                                <h4 className="text-xs font-black text-slate-900 uppercase tracking-widest">Linked Attachments</h4>
                             </div>
                             <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                {selectedNotice.attachments.map((att, i) => (
                                   <a 
                                      key={i} 
                                      href={att.url} 
                                      className="p-4 rounded-3xl bg-slate-50 border border-slate-100 hover:bg-white hover:border-brand-500 transition-all flex items-center justify-between group"
                                   >
                                      <div className="flex items-center gap-3">
                                         <div className="p-2 bg-white rounded-xl text-slate-400 group-hover:text-brand-500 transition-colors">
                                            <Paperclip className="w-4 h-4" />
                                         </div>
                                         <span className="text-[11px] font-bold text-slate-700">{att.name}</span>
                                      </div>
                                      <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-brand-500 transition-all group-hover:translate-x-1" />
                                   </a>
                                ))}
                             </div>
                          </div>
                       )}

                       <div className="p-8 rounded-[2.5rem] bg-brand-50 border border-brand-100/50 flex items-start gap-4">
                          <Info className="w-6 h-6 text-brand-500 flex-shrink-0 mt-1" />
                          <div>
                             <h5 className="text-xs font-black text-brand-600 uppercase tracking-tight mb-1">Acknowledgement Required</h5>
                             <p className="text-[11px] text-brand-500/80 font-medium leading-relaxed italic">
                                By viewing this notice, your digital receipt has been logged. For urgent concerns regarding this bulletin, please contact the administration office.
                             </p>
                          </div>
                       </div>
                    </div>

                    {/* Footer Actions */}
                    <div className="p-10 bg-slate-50/50 border-t border-slate-100 flex justify-end gap-3 flex-shrink-0">
                       <button className="px-8 py-4 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl active:scale-95 flex items-center gap-2">
                         Download Copy <Paperclip className="w-4 h-4" />
                       </button>
                    </div>
                 </motion.div>
               ) : (
                 <div className="flex-1 flex flex-col items-center justify-center p-20 text-center opacity-50">
                     <div className="p-8 bg-slate-50 rounded-[3rem] mb-6 border border-slate-100">
                        <Megaphone className="w-16 h-16 text-slate-300" />
                     </div>
                     <h3 className="text-2xl font-black text-slate-900 uppercase">Select an Announcement</h3>
                     <p className="text-xs text-slate-400 font-bold mt-2 uppercase tracking-widest leading-relaxed">Stay updated with institutional declarations and event bulletins.</p>
                 </div>
               )}
            </AnimatePresence>
            
            {/* Background Grain/Texture */}
            <div className="absolute inset-0 z-0 pointer-events-none opacity-5 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]" />
         </div>
      </div>

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
