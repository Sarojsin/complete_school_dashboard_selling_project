import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpen, 
  ChevronLeft, 
  Clock, 
  CheckCircle2, 
  AlertCircle, 
  Calendar, 
  Paperclip, 
  ChevronRight,
  Filter,
  Search,
  Download,
  Info,
  ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getLinkedChildren, getChildHomework } from '../api/parents';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function ParentHomework() {
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [homework, setHomework] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');

  // Mocks for visual presentation
  const mockHomework = [
    { 
      id: 1, 
      title: 'Quantum Mechanics Basics', 
      subject_name: 'Physics', 
      description: 'Solve problems on wave-particle duality and uncertainty principle.', 
      course_name: 'Advanced Science', 
      assigned_date: '2024-03-25', 
      due_date: '2024-03-30', 
      submitted: true,
      total_marks: 50,
      attachments: [{ name: 'ProblemSet1.pdf', url: '#' }]
    },
    { 
      id: 2, 
      title: 'Economic Revolution', 
      subject_name: 'History', 
      description: 'Write a 500-word essay on the Industrial Revolution impacts.', 
      course_name: 'Humanities', 
      assigned_date: '2024-03-27', 
      due_date: '2024-03-29', 
      submitted: false,
      total_marks: 30,
      attachments: []
    },
    { 
      id: 3, 
      title: 'Calculus IV: Integration', 
      subject_name: 'Mathematics', 
      description: 'Complete exercies from Chapter 5.2 - 5.5.', 
      course_name: 'Core Mathematics', 
      assigned_date: '2024-03-20', 
      due_date: '2024-03-24', 
      submitted: false,
      total_marks: 40,
      attachments: []
    }
  ];

  useEffect(() => {
    fetchChildren();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchHomework(selectedChild.id || selectedChild.student_id);
    }
  }, [selectedChild]);

  const fetchChildren = async () => {
    try {
      const res = await getLinkedChildren();
      const childrenList = res.data?.children || [];
      setChildren(childrenList);
      if (childrenList.length > 0) setSelectedChild(childrenList[0]);
    } catch (err) {
      console.error('Error fetching children:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchHomework = async (studentId) => {
    try {
      setLoading(true);
      const res = await getChildHomework(studentId);
      setHomework(res.data || mockHomework);
    } catch (err) {
      console.error('Error fetching homework:', err);
      setHomework(mockHomework);
    } finally {
      setLoading(false);
    }
  };

  const getStatus = (hw) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const dueDate = new Date(hw.due_date);
    
    if (hw.submitted) return { label: 'Submitted', variant: 'success', icon: CheckCircle2 };
    if (dueDate < today) return { label: 'Overdue', variant: 'danger', icon: AlertCircle };
    if (dueDate.toDateString() === today.toDateString()) return { label: 'Due Today', variant: 'warning', icon: Clock };
    return { label: 'Pending', variant: 'primary', icon: Clock };
  };

  const filteredHomework = homework.filter(hw => {
    const matchesSearch = hw.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         hw.subject_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const status = getStatus(hw).label.toLowerCase();
    if (activeFilter === 'all') return matchesSearch;
    if (activeFilter === 'pending') return matchesSearch && (status === 'pending' || status === 'due today');
    if (activeFilter === 'submitted') return matchesSearch && status === 'submitted';
    if (activeFilter === 'overdue') return matchesSearch && status === 'overdue';
    return matchesSearch;
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !homework.length) {
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
      className="p-6 lg:p-10 space-y-8"
    >
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <Link 
            to="/parent/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Back to Dashboard
          </Link>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <BookOpen className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Academic Tasks</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Assignment Tracker</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Support your child's learning journey through timely engagement."</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex flex-col gap-2 min-w-[240px]">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Viewing Records For</label>
          <select 
            value={selectedChild?.id || ''} 
            onChange={(e) => {
              const child = children.find(c => (c.id || c.student_id) == e.target.value);
              setSelectedChild(child);
            }}
            className="px-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all shadow-sm"
          >
            {children.map((child) => (
              <option key={child.id || child.student_id} value={child.id || child.student_id}>
                {child.full_name || child.student_name}
              </option>
            ))}
          </select>
        </motion.div>
      </section>

      {/* Stats Overview */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard 
          icon={Clock} 
          title="Pending Tasks" 
          value={homework.filter(h => !h.submitted && new Date(h.due_date) >= new Date().setHours(0,0,0,0)).length} 
          trend="Requires attention" 
          trendType="warning" 
        />
        <ModernStatCard 
          icon={CheckCircle2} 
          title="Completed" 
          value={homework.filter(h => h.submitted).length} 
          trend="Overall progress" 
          trendType="positive" 
        />
        <ModernStatCard 
          icon={AlertCircle} 
          title="Overdue" 
          value={homework.filter(h => !h.submitted && new Date(h.due_date) < new Date().setHours(0,0,0,0)).length} 
          trend="Critical priority" 
          trendType="danger" 
        />
      </motion.section>

      {/* Filters & Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <motion.div variants={itemVariants} className="flex flex-col md:flex-row gap-4 justify-between items-center">
             <div className="relative flex-1 w-full max-w-md">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input 
                  type="text"
                  placeholder="Search by assignment or subject..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-12 pr-6 py-4 bg-white border border-slate-200 rounded-[2rem] text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 shadow-sm transition-all"
                />
             </div>
             <div className="flex bg-slate-100 p-1.5 rounded-[2rem] border border-slate-200 shadow-inner">
                {['all', 'pending', 'submitted', 'overdue'].map((f) => (
                  <button
                    key={f}
                    onClick={() => setActiveFilter(f)}
                    className={cn(
                      "px-6 py-2 rounded-[1.5rem] text-[10px] font-black uppercase tracking-tight transition-all",
                      activeFilter === f 
                        ? "bg-white text-brand-500 shadow-sm" 
                        : "text-slate-400 hover:text-slate-600"
                    )}
                  >
                    {f}
                  </button>
                ))}
             </div>
          </motion.div>

          <motion.div variants={itemVariants} className="space-y-4">
             <AnimatePresence mode="popLayout">
                {filteredHomework.length > 0 ? (
                  filteredHomework.map((hw) => {
                    const status = getStatus(hw);
                    return (
                      <motion.div
                        key={hw.id}
                        layout
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                      >
                         <GlassCard noPadding className="overflow-hidden border-transparent hover:border-brand-200 group transition-all">
                            <div className="p-8">
                               <div className="flex justify-between items-start mb-4">
                                  <div className="space-y-1">
                                     <div className="flex items-center gap-2">
                                        <ModernBadge variant="primary" size="xs" className="px-3 bg-brand-50 text-brand-600 border-none">{hw.subject_name}</ModernBadge>
                                        <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{hw.course_name}</span>
                                     </div>
                                     <h3 className="text-xl font-black text-slate-900 leading-tight group-hover:text-brand-500 transition-colors uppercase tracking-tight ">{hw.title}</h3>
                                  </div>
                                  <ModernBadge variant={status.variant} size="sm" className="shadow-sm">
                                     <status.icon className="w-3 h-3 mr-1.5 inline" /> {status.label}
                                  </ModernBadge>
                               </div>

                               <p className="text-xs text-slate-500 font-medium leading-relaxed line-clamp-2 mb-6">{hw.description}</p>

                               <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-6 border-y border-slate-100 mb-6">
                                  <div className="space-y-1">
                                     <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Assigned On</span>
                                     <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5"><Calendar className="w-3.5 h-3.5 text-brand-400" /> {new Date(hw.assigned_date).toLocaleDateString()}</span>
                                  </div>
                                  <div className="space-y-1">
                                     <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Deadline</span>
                                     <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5"><Clock className="w-3.5 h-3.5 text-rose-400" /> {new Date(hw.due_date).toLocaleDateString()}</span>
                                  </div>
                                  <div className="space-y-1">
                                     <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Max Marks</span>
                                     <span className="text-xs font-bold text-slate-700">{hw.total_marks} Pts</span>
                                  </div>
                                  <div className="space-y-1">
                                     <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Resources</span>
                                     <span className="text-xs font-bold text-slate-700">{hw.attachments?.length || 0} Files</span>
                                  </div>
                               </div>

                               <div className="flex justify-between items-center">
                                  <div className="flex -space-x-2">
                                     {hw.attachments?.map((att, i) => (
                                        <div key={i} className="w-8 h-8 rounded-lg bg-slate-900 border-2 border-white flex items-center justify-center text-white cursor-pointer hover:-translate-y-1 transition-transform shadow-md" title={att.name}>
                                           <Paperclip className="w-4 h-4" />
                                        </div>
                                     ))}
                                  </div>
                                  <button className="px-8 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg active:scale-95 flex items-center gap-2 group/btn">
                                     Detailed view <ArrowRight className="w-3.5 h-3.5 group-hover/btn:translate-x-1 transition-transform" />
                                  </button>
                               </div>
                            </div>
                         </GlassCard>
                      </motion.div>
                    );
                  })
                ) : (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-20 text-center">
                     <div className="p-6 bg-slate-50 border border-slate-100 rounded-[3rem] inline-flex mb-4">
                        <BookOpen className="w-12 h-12 text-slate-300" />
                     </div>
                     <h4 className="text-xl font-black text-slate-900 uppercase">No Assignments Found</h4>
                     <p className="text-xs text-slate-400 font-bold mt-2 uppercase tracking-tight">Try adjusting your filters or search terms.</p>
                  </motion.div>
                )}
             </AnimatePresence>
          </motion.div>
        </div>

        {/* Sidebar Insights */}
        <div className="space-y-8">
           <motion.div variants={itemVariants}>
              <GlassCard title="Learning Insights" icon={Info}>
                 <div className="space-y-4">
                    <div className="p-5 rounded-3xl bg-brand-50 border border-brand-100/50 space-y-4">
                       <div className="flex items-center gap-2">
                          <CheckCircle2 className="w-5 h-5 text-brand-500" />
                          <h6 className="text-xs font-black text-slate-900 uppercase tracking-tight">Consistency Alert</h6>
                       </div>
                       <p className="text-xs font-bold text-slate-700 leading-relaxed italic">
                         {selectedChild?.full_name} has submitted 80% of Science homework ahead of time this month. Great motivation!
                       </p>
                    </div>
                    <button className="w-full py-4 border border-slate-200 text-slate-500 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:text-brand-500 hover:border-brand-500 transition-all">
                       Email Section In-charge
                    </button>
                 </div>
              </GlassCard>
           </motion.div>

           <motion.div variants={itemVariants}>
              <div className="p-8 rounded-[2.5rem] bg-slate-900 border border-slate-800 shadow-2xl relative overflow-hidden group">
                 <div className="relative z-10 text-white space-y-6">
                    <div className="p-3 bg-white/10 rounded-2xl w-fit text-amber-400">
                       <Clock className="w-6 h-6" />
                    </div>
                    <div>
                       <h4 className="text-xl font-black leading-tight uppercase">Upcoming <br />Deadline</h4>
                       <p className="text-slate-400 text-[10px] font-bold mt-2 uppercase tracking-widest italic">Science: Quantum Basics</p>
                    </div>
                    <div className="flex items-center justify-between">
                       <span className="text-2xl font-black text-brand-400 tracking-tighter">02:24:15</span>
                       <ModernBadge variant="warning" size="xs">STRICT</ModernBadge>
                    </div>
                    <p className="text-[10px] text-slate-500 font-medium">Please ensure submission before Thursday midnight.</p>
                 </div>
                 {/* Decorative Pulse */}
                 <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/10 blur-3xl rounded-full translate-x-12 -translate-y-12 animate-pulse" />
              </div>
           </motion.div>

           <motion.div variants={itemVariants}>
              <GlassCard title="Submission Rules" icon={AlertCircle}>
                 <ul className="space-y-4">
                    {[
                       'PDF format is mandatory for all essays.',
                       'Handwritten notes must be scanned clearly.',
                       'Plagiarism check is active for all uploads.'
                    ].map((rule, i) => (
                       <li key={i} className="flex gap-3 text-[11px] font-bold text-slate-600">
                          <div className="w-1.5 h-1.5 rounded-full bg-brand-500 mt-1.5" />
                          {rule}
                       </li>
                    ))}
                 </ul>
              </GlassCard>
           </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

// Utility
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}
