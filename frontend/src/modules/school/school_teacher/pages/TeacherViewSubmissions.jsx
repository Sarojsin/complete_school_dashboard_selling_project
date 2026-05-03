import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ChevronLeft, 
  FileCheck, 
  Users, 
  CheckCircle2, 
  Clock, 
  Search, 
  Filter, 
  ExternalLink,
  MoreVertical,
  Download,
  Eye,
  Edit3,
  X
} from 'lucide-react';
import { getAssignment, getSubmissions } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const TeacherViewSubmissions = () => {
  const { assignmentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [assignment, setAssignment] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSubmission, setSelectedSubmission] = useState(null);

  useEffect(() => {
    loadData();
  }, [assignmentId]);

  const loadData = async () => {
    try {
      const [assignmentRes, submissionsRes] = await Promise.all([
        getAssignment(assignmentId),
        getSubmissions(assignmentId)
      ]);
      setAssignment(assignmentRes.data || assignmentRes);
      setSubmissions(submissionsRes.data || submissionsRes);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  const filteredSubmissions = submissions.filter(s => 
    s.student_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.student_id?.toString().includes(searchQuery)
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="relative w-24 h-24">
          <div className="absolute inset-0 border-4 border-brand-500/10 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-brand-500 rounded-full border-t-transparent animate-spin"></div>
          <FileCheck className="absolute inset-0 m-auto w-8 h-8 text-brand-500 animate-pulse" />
        </div>
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
          <button 
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Back to Assignments
          </button>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <FileCheck className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Grading Portal</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">{assignment?.title || 'Assignment Submissions'}</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium max-w-2xl">{assignment?.description || 'Review and grade student submissions for this task.'}</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <button className="px-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold hover:bg-slate-50 transition-all shadow-sm flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export Grades
          </button>
        </motion.div>
      </section>

      {/* Stats Quick View */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard icon={Users} title="Total Submissions" value={submissions.length} trend="Active participants" trendType="neutral" />
        <ModernStatCard icon={Clock} title="Pending Review" value={submissions.filter(s => s.status === 'submitted' || !s.marks).length} trend="Review required" trendType="warning" />
        <ModernStatCard icon={CheckCircle2} title="Graded Items" value={submissions.filter(s => s.status === 'graded' || s.marks).length} trend="Done & Synced" trendType="positive" />
      </motion.section>

      {/* Roster & Grading Table */}
      <motion.div variants={itemVariants}>
        <GlassCard noPadding>
          {/* Table Header / Filter */}
          <div className="p-6 border-b border-slate-100 flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative w-full md:w-96">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input 
                type="text" 
                placeholder="Find a student or submission..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-brand-500/20 transition-all text-sm font-medium"
              />
            </div>
            <div className="flex items-center gap-2">
              <button className="px-5 py-3 bg-slate-100 text-slate-600 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-slate-200 transition-all">Show Graded</button>
              <button className="p-3 bg-white border border-slate-200 rounded-xl text-slate-400 hover:text-brand-500 transition-all"><Filter className="w-4 h-4" /></button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-slate-50/50 border-b border-slate-100">
                  <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Student</th>
                  <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Submitted At</th>
                  <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Status</th>
                  <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Marks</th>
                  <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredSubmissions.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="px-6 py-20 text-center text-slate-400 font-medium italic">No submissions found for this query.</td>
                  </tr>
                ) : (
                  filteredSubmissions.map((s) => (
                    <tr key={s.id} className="group hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center font-black text-slate-400">
                            {s.student_name?.charAt(0)}
                          </div>
                          <div>
                            <h4 className="font-bold text-slate-900 group-hover:text-brand-500 transition-colors">{s.student_name}</h4>
                            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">ID: {s.student_id}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-xs font-bold text-slate-600">{s.submitted_at || 'Jan 12, 10:20 AM'}</span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <ModernBadge variant={s.status === 'graded' ? 'success' : 'warning'} size="sm">
                          {s.status || 'Submitted'}
                        </ModernBadge>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="inline-block px-3 py-1.5 bg-brand-50 text-brand-700 rounded-lg text-sm font-black ring-1 ring-brand-100">
                          {s.marks || '--'} / {assignment?.points || 100}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button 
                            onClick={() => setSelectedSubmission(s)}
                            className="p-2.5 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all shadow-sm"
                            title="Quick View"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="p-2.5 bg-slate-900 text-white hover:bg-slate-700 rounded-xl transition-all shadow-lg shadow-slate-900/10">
                            <Edit3 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </motion.div>

      {/* Submission Detail Modal */}
      <AnimatePresence>
        {selectedSubmission && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedSubmission(null)}
              className="absolute inset-0 bg-slate-900/60 backdrop-blur-md"
            />
            <motion.div 
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              className="relative w-full max-w-4xl bg-white rounded-[2rem] shadow-2xl overflow-hidden flex flex-col md:flex-row h-[80vh]"
            >
              {/* Left Content Area */}
              <div className="flex-1 bg-slate-50 p-8 overflow-y-auto">
                <div className="flex justify-between items-start mb-8">
                  <div>
                    <h3 className="text-2xl font-black text-slate-900 tracking-tight">{selectedSubmission.student_name}</h3>
                    <p className="text-sm font-bold text-slate-400 uppercase tracking-widest mt-1">Submitted on Oct 12, 10:20 AM</p>
                  </div>
                  <button className="p-3 bg-white border border-slate-200 rounded-xl text-brand-500 hover:bg-brand-50 transition-all shadow-sm">
                    <Download className="w-5 h-5" />
                  </button>
                </div>
                
                {/* File Preview Mock */}
                <div className="aspect-[4/5] bg-white rounded-3xl border border-slate-200 shadow-sm p-10 flex flex-col items-center justify-center text-center space-y-4">
                  <div className="w-20 h-20 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
                    <FileCheck className="w-10 h-10" />
                  </div>
                  <h4 className="text-lg font-bold text-slate-900">Submission_Doc.pdf</h4>
                  <p className="text-sm text-slate-500 font-medium">Click to open full preview in a new tab</p>
                  <button className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 flex items-center gap-2">
                    Open Document <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Right Grading Panel */}
              <div className="w-full md:w-[360px] bg-white border-l border-slate-100 p-8 flex flex-col justify-between">
                <div className="space-y-8">
                  <div className="flex justify-between items-center">
                    <h4 className="text-sm font-black text-slate-900 uppercase tracking-widest">Grading Panel</h4>
                    <button onClick={() => setSelectedSubmission(null)} className="p-2 hover:bg-slate-100 rounded-xl transition-all">
                      <X className="w-5 h-5 text-slate-400" />
                    </button>
                  </div>

                  <div className="space-y-4">
                    <div className="space-y-2">
                      <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Score / {assignment?.points || 100}</label>
                      <input 
                        type="number" 
                        defaultValue={selectedSubmission.marks || ''}
                        placeholder="Enter marks..."
                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-black text-xl text-slate-900" 
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Feedback & Remarks</label>
                      <textarea 
                        placeholder="Type personalized feedback..."
                        className="w-full min-h-[160px] p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all text-sm font-medium leading-relaxed" 
                      />
                    </div>
                  </div>
                </div>

                <div className="pt-8 space-y-3">
                  <button className="w-full py-4 bg-emerald-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-emerald-600 transition-all shadow-lg shadow-emerald-500/20 active:scale-95">
                    Save & Publish Grade
                  </button>
                  <button className="w-full py-4 bg-slate-100 text-slate-600 rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-200 transition-all active:scale-95">
                    Return for Revision
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default TeacherViewSubmissions;
