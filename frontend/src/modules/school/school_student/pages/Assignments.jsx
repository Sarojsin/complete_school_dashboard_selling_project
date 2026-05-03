import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Filter, 
  Search, 
  Calendar,
  User,
  ExternalLink,
  ChevronRight,
  Plus,
  Upload
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getStudentAssignments } from '../api/students';
import GlassCard from '../../../shared/components/GlassCard';
import ModernStatCard from '../../../shared/components/ModernStatCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function AssignmentsPage() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    getStudentAssignments()
      .then(data => {
        setAssignments(Array.isArray(data) ? data : (data.assignments || []));
      })
      .catch(err => console.error("Assignments Fetch Error:", err))
      .finally(() => setLoading(false));
  }, []);

  const filteredAssignments = assignments.filter(a => {
    const matchesFilter = filter === 'all' || a.status === filter;
    const matchesSearch = a.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         a.subject?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const getStatusConfig = (status) => {
    switch (status) {
      case 'submitted': return { variant: 'success', icon: CheckCircle, label: 'Submitted' };
      case 'pending': return { variant: 'warning', icon: Clock, label: 'Pending' };
      case 'overdue': return { variant: 'danger', icon: AlertCircle, label: 'Overdue' };
      case 'graded': return { variant: 'primary', icon: Award, label: 'Graded' };
      default: return { variant: 'neutral', icon: HelpCircle, label: status };
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.05 } }
  };

  const itemVariants = {
    hidden: { y: 10, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

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
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <Clock className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Task Tracker</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Assignment Portal</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Manage your submissions, track deadlines, and view instructor feedback.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Filter tasks..."
              className="pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all w-64 shadow-sm"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex bg-slate-100 p-1 rounded-2xl">
            {['all', 'pending', 'submitted', 'overdue'].map((f) => (
              <button 
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all uppercase tracking-wider ${filter === f ? "bg-white shadow-sm text-brand-500" : "text-slate-500 hover:text-slate-700"}`}
              >
                {f}
              </button>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Stats Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={BookOpen} title="All Tasks" value={assignments.length} trend="Total assigned" />
        <ModernStatCard 
          icon={Clock} 
          title="To Do" 
          value={assignments.filter(a => a.status === 'pending').length} 
          trend="Action required" 
          trendType="negative" 
        />
        <ModernStatCard 
          icon={CheckCircle} 
          title="Done" 
          value={assignments.filter(a => a.status === 'submitted' || a.status === 'graded').length} 
          trend="Great work!" 
          trendType="positive" 
        />
        <ModernStatCard 
          icon={AlertCircle} 
          title="Overdue" 
          value={assignments.filter(a => a.status === 'overdue').length} 
          trend="Review ASAP" 
          trendType="negative" 
        />
      </motion.section>

      {/* Content */}
      <motion.div variants={itemVariants}>
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-slate-500 font-bold">Fetching your assignments...</p>
          </div>
        ) : filteredAssignments.length === 0 ? (
          <div className="text-center py-20 glass-card rounded-3xl">
            <CheckCircle className="w-16 h-16 text-emerald-300 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-slate-800">No tasks found</h3>
            <p className="text-slate-500">You're all caught up or no results match your filter.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {filteredAssignments.map((a, i) => {
              const statusConfig = getStatusConfig(a.status);
              const StatusIcon = statusConfig.icon;
              return (
                <GlassCard key={a.id || i} noPadding className="p-0 overflow-hidden group">
                  <div className="flex flex-col lg:flex-row lg:items-center">
                    {/* Status accent side */}
                    <div className={cn(
                      "w-full lg:w-2 h-2 lg:h-auto shrink-0",
                      statusConfig.variant === 'success' ? "bg-emerald-500" : 
                      statusConfig.variant === 'warning' ? "bg-amber-500" : 
                      statusConfig.variant === 'danger' ? "bg-rose-500" : "bg-brand-500"
                    )}></div>
                    
                    <div className="flex-1 p-6 flex flex-col lg:flex-row lg:items-center gap-6">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 mb-2">
                          <ModernBadge variant="neutral" size="sm" className="bg-slate-100 border-slate-200">{a.subject || 'Course'}</ModernBadge>
                          <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-1">
                            <Clock className="w-3 h-3" /> Due {a.due_at || a.due_date || 'TBD'}
                          </span>
                        </div>
                        <h3 className="text-xl font-black text-slate-900 mb-2 truncate group-hover:text-brand-500 transition-colors">
                          {a.title}
                        </h3>
                        <p className="text-sm text-slate-500 line-clamp-1 font-medium">{a.description}</p>
                      </div>

                      <div className="flex items-center gap-8 lg:px-8 lg:border-l lg:border-slate-100">
                        <div className="flex flex-col">
                          <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Status</span>
                          <div className="flex items-center gap-1.5">
                            <StatusIcon className={cn("w-4 h-4", `text-${statusConfig.variant}-500`)} />
                            <span className={cn("text-sm font-bold", `text-${statusConfig.variant}-600`)}>{statusConfig.label}</span>
                          </div>
                        </div>
                        <div className="flex flex-col">
                          <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Max Score</span>
                          <span className="text-sm font-black text-slate-900">{a.max_points || a.max_score || 100} PTS</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <Link 
                          to={`/student/assignments/${a.id}`}
                          className="px-6 py-3 bg-slate-50 text-slate-700 rounded-xl font-bold text-sm hover:bg-slate-100 transition-all border border-slate-200"
                        >
                          Details
                        </Link>
                        {a.status !== 'submitted' && (
                          <button className="flex items-center gap-2 px-6 py-3 bg-brand-500 text-white rounded-xl font-bold text-sm hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20">
                            <Upload className="w-4 h-4" />
                            Submit
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </GlassCard>
              );
            })}
          </div>
        )}
      </motion.div>

      {/* Footer / Calendar Link */}
      <motion.section variants={itemVariants} className="pt-8 flex flex-col md:flex-row items-center justify-between gap-6 border-t border-slate-200">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-amber-50 rounded-2xl text-amber-500">
            <AlertCircle className="w-6 h-6" />
          </div>
          <div>
            <h4 className="font-black text-slate-800 uppercase tracking-tight">Need an extension?</h4>
            <p className="text-xs text-slate-500 font-medium">Contact your instructor directly through the messaging portal.</p>
          </div>
        </div>
        <Link 
          to="/calendar" 
          className="flex items-center gap-3 px-8 py-4 bg-slate-900 text-white rounded-3xl font-black text-sm hover:bg-slate-800 transition-all"
        >
          <Calendar className="w-5 h-5" />
          VIEW DEADLINE CALENDAR
          <ChevronRight className="w-5 h-5" />
        </Link>
      </motion.section>
    </motion.div>
  );
}

// Minimal Award fallback if not imported
const Award = (props) => <BookOpen {...props} />;
const HelpCircle = (props) => <AlertCircle {...props} />;
