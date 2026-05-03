import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  ClipboardList, 
  Plus, 
  Calendar, 
  Users, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  MoreVertical,
  ChevronRight,
  Search,
  BookOpen,
  Filter,
  FileText
} from 'lucide-react';
import { getTeacherAssignments } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function TeacherAssignmentsPage() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  useEffect(() => {
    getTeacherAssignments()
      .then(data => setAssignments(data))
      .catch(err => console.error("Assignments Fetch Error:", err))
      .finally(() => setLoading(false));
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  const filteredAssignments = assignments.filter(a => 
    a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    a.course_name?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getStatusBadge = (dueDate, submissionCount, totalStudents) => {
    const now = new Date();
    const due = new Date(dueDate);
    const ratio = totalStudents > 0 ? (submissionCount / totalStudents) : 0;

    if (due < now) return <ModernBadge variant="danger" size="sm">Past Due</ModernBadge>;
    if (ratio === 1) return <ModernBadge variant="success" size="sm">All Submitted</ModernBadge>;
    return <ModernBadge variant="primary" size="sm">Active</ModernBadge>;
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
              <ClipboardList className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Academic Evaluation</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Assignment Portal</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Track submissions, manage deadlines, and grade with precision.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <Link 
            to="/teacher/assignments/create"
            className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-sm font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 flex items-center gap-2 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            Create Assignment
          </Link>
        </motion.div>
      </section>

      {/* Stats Quick View */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard icon={FileText} title="Total Issued" value={assignments.length} trend="Active this semester" trendType="neutral" />
        <ModernStatCard icon={CheckCircle2} title="Avg Submission" value="84%" trend="Target reach: 90%" trendType="positive" />
        <ModernStatCard icon={AlertCircle} title="Pending Grading" value="12" trend="Next due in 48h" trendType="warning" />
      </motion.section>

      {/* Search & Layout Toggle */}
      <motion.section variants={itemVariants} className="flex flex-col md:flex-row gap-4 items-center">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search by topic, unit, or course..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-4 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium text-slate-700 shadow-sm"
          />
        </div>
        <div className="flex items-center gap-2">
          <button className="px-6 py-4 bg-white border border-slate-200 rounded-2xl text-slate-600 font-bold flex items-center gap-2 hover:bg-slate-50 transition-all shadow-sm">
            <Filter className="w-4 h-4" /> All Courses
          </button>
        </div>
      </motion.section>

      {/* Assignments List */}
      <motion.section variants={itemVariants} className="space-y-4">
        {loading ? (
          [1,2,3].map(i => <div key={i} className="h-32 bg-slate-50 rounded-3xl animate-pulse" />)
        ) : filteredAssignments.length === 0 ? (
          <div className="py-20 text-center bg-slate-50/50 rounded-3xl border-2 border-dashed border-slate-200">
            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
              <ClipboardList className="w-8 h-8 text-slate-300" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">No assignments found</h3>
            <p className="text-slate-500 mt-2">Create your first evaluation task to get started.</p>
          </div>
        ) : (
          filteredAssignments.map((a) => (
            <div 
              key={a.id} 
              className="group relative bg-white border border-slate-200 rounded-3xl p-6 hover:shadow-xl hover:border-brand-200 transition-all flex flex-col md:flex-row items-start md:items-center justify-between gap-6 overflow-hidden"
            >
              {/* Left Side: Info */}
              <div className="flex-1 space-y-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-brand-50 rounded-xl">
                    <BookOpen className="w-4 h-4 text-brand-500" />
                  </div>
                  <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{a.course_name || 'General Course'}</span>
                  {getStatusBadge(a.due_date, a.submission_count, a.total_students)}
                </div>
                <h3 className="text-xl font-bold text-slate-900 group-hover:text-brand-500 transition-colors leading-tight">{a.title}</h3>
                <div className="flex flex-wrap items-center gap-6 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                  <div className="flex items-center gap-1.5"><Calendar className="w-4 h-4 text-slate-400" /> DUE {new Date(a.due_date).toLocaleDateString()}</div>
                  <div className="flex items-center gap-1.5"><Users className="w-4 h-4 text-slate-400" /> {a.submission_count || 0} / {a.total_students || 0} SUBMITTED</div>
                </div>
              </div>

              {/* Progress Indicator */}
              <div className="w-full md:w-32 space-y-2">
                <div className="flex justify-between text-[10px] font-bold uppercase text-slate-400">
                  <span>Grading</span>
                  <span>75%</span>
                </div>
                <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full transition-all duration-1000" style={{ width: '75%' }} />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2 self-end md:self-auto">
                <Link 
                  to={`/teacher/assignments/${a.id}/submissions`}
                  className="px-6 py-3 bg-slate-900 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg shadow-slate-900/10 active:scale-95 flex items-center gap-2"
                >
                  Grade Samples <ChevronRight className="w-4 h-4" />
                </Link>
                <button className="p-3 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all shadow-sm">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>
              
              {/* Animated Side-Bar Interaction */}
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-brand-500 scale-y-0 group-hover:scale-y-100 transition-transform origin-top" />
            </div>
          ))
        )}
      </motion.section>

      {/* Help Tip */}
      <motion.div variants={itemVariants} className="p-4 bg-brand-50 border border-brand-100 rounded-3xl flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-brand-500">
          <Clock className="w-5 h-5" />
        </div>
        <p className="text-xs font-bold text-brand-700 uppercase tracking-widest">
          Tip: You can now set auto-grading rules for multiple-choice unit tests. Check the "Academic Settings" for more.
        </p>
      </motion.div>
    </motion.div>
  );
}
