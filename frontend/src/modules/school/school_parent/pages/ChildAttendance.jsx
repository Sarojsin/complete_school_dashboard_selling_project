import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Calendar, 
  ChevronLeft, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Filter, 
  Download,
  Users,
  Info,
  ChevronRight,
  TrendingUp,
  AlertCircle
} from 'lucide-react';
import { getLinkedChildren, getChildAttendance } from '../api/parents';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function ChildAttendance() {
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [attendanceData, setAttendanceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mocks for presentation
  const mockAttendance = {
    present: 18,
    absent: 2,
    late: 1,
    percentage: 86,
    month: 'March 2024',
    details: [
      { date: '2024-03-25', status: 'present' },
      { date: '2024-03-24', status: 'present' },
      { date: '2024-03-23', status: 'absent' },
      { date: '2024-03-22', status: 'late' },
      { date: '2024-03-21', status: 'present' },
    ]
  };

  useEffect(() => {
    fetchChildren();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchAttendance(selectedChild.id || selectedChild.student_id);
    }
  }, [selectedChild]);

  const fetchChildren = async () => {
    try {
      const res = await getLinkedChildren();
      const childrenList = res.data?.children || [];
      setChildren(childrenList);
      if (childrenList.length > 0) {
        setSelectedChild(childrenList[0]);
      }
    } catch (err) {
      console.error('Error fetching children:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAttendance = async (studentId) => {
    try {
      setLoading(true);
      const res = await getChildAttendance(studentId);
      setAttendanceData(res.data || mockAttendance);
    } catch (err) {
      console.error('Error fetching attendance:', err);
      setAttendanceData(mockAttendance);
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

  if (loading && !attendanceData) {
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
              <Calendar className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Attendance Logs</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Presence Tracking</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Consistency in attendance correlates with academic success."</p>
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

      {/* Summary Stats */}
      {attendanceData && (
        <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <ModernStatCard icon={CheckCircle2} title="Total Present" value={attendanceData.present || 0} trend="Days tracked" trendType="neutral" />
          <ModernStatCard icon={XCircle} title="Total Absent" value={attendanceData.absent || 0} trend="Requires justification" trendType="warning" />
          <ModernStatCard icon={Clock} title="Late Arrivals" value={attendanceData.late || 0} trend="Last 30 days" trendType="neutral" />
          <ModernStatCard icon={TrendingUp} title="Attendance %" value={`${attendanceData.percentage || 0}%`} trend="Target: 90%+" trendType={attendanceData.percentage >= 90 ? "positive" : "warning"} />
        </motion.section>
      )}

      {/* Detailed Logs & Tools */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <motion.div variants={itemVariants}>
            <GlassCard title={`${selectedChild?.full_name}'s Log - ${attendanceData?.month || 'Current Month'}`} icon={Calendar} noPadding>
              <div className="p-6 border-b border-slate-100 flex justify-between items-center">
                 <div className="flex gap-2">
                    <button className="px-4 py-2 bg-slate-900 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center gap-2">
                       <Download className="w-3.5 h-3.5" /> PDF Report
                    </button>
                    <button className="p-2.5 border border-slate-200 text-slate-400 hover:text-brand-500 rounded-xl transition-all"><Filter className="w-4 h-4" /></button>
                 </div>
                 <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1.5 ">
                       <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Present</span>
                    </div>
                    <div className="flex items-center gap-1.5 ">
                       <div className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Absent</span>
                    </div>
                 </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50/50 border-b border-slate-100">
                      <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Date</th>
                      <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Status</th>
                      <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Remarks</th>
                      <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {attendanceData?.details?.map((day, idx) => (
                      <tr key={idx} className="group hover:bg-slate-50/50 transition-colors">
                        <td className="px-8 py-4">
                          <span className="text-sm font-bold text-slate-900">{new Date(day.date).toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' })}</span>
                        </td>
                        <td className="px-8 py-4">
                          <ModernBadge 
                            variant={day.status === 'present' ? 'success' : day.status === 'absent' ? 'danger' : 'warning'} 
                            size="sm"
                          >
                            {day.status}
                          </ModernBadge>
                        </td>
                        <td className="px-8 py-4">
                          <span className="text-xs text-slate-500 font-medium italic">-- {day.status === 'absent' ? 'Needs Justification' : 'Routine Session'}</span>
                        </td>
                        <td className="px-8 py-4 text-right">
                           <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all group-hover:shadow-sm">
                              <ChevronRight className="w-4 h-4" />
                           </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard title="Quick Insight" icon={Info}>
               <div className="space-y-4">
                  <div className="p-4 rounded-2xl bg-amber-50 border border-amber-100/50 space-y-3">
                     <div className="flex items-center gap-2">
                        <AlertCircle className="w-4 h-4 text-amber-500" />
                        <span className="text-[10px] font-black text-amber-600 uppercase tracking-widest">Recommendation</span>
                     </div>
                     <p className="text-xs font-bold text-slate-700 leading-relaxed">
                        Attendance has dropped by <span className="text-rose-500">2%</span> this week. Maintaining 95% is critical for final exam eligibility.
                     </p>
                  </div>
                  <button className="w-full py-4 bg-slate-900 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg active:scale-95">
                    Request Leave
                  </button>
               </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={itemVariants}>
            <div className="p-8 rounded-[2rem] bg-brand-500 border border-brand-400 shadow-2xl relative overflow-hidden">
               <div className="relative z-10 space-y-4 text-white">
                  <h4 className="text-xl font-black leading-tight uppercase">Monthly Recap</h4>
                  <div className="space-y-2">
                     <div className="flex justify-between text-[10px] font-black uppercase text-white/70 tracking-widest">
                        <span>Completion goal</span>
                        <span>90%</span>
                     </div>
                     <div className="h-2 w-full bg-white/20 rounded-full overflow-hidden">
                        <div className="h-full bg-white transition-all duration-1000" style={{ width: '86%' }} />
                     </div>
                  </div>
                  <p className="text-white/80 text-[10px] font-medium italic">86% attendance recorded for {selectedChild?.full_name} in {attendanceData?.month}.</p>
               </div>
               <div className="absolute -bottom-12 -right-12 w-40 h-40 bg-white/10 blur-3xl rounded-full" />
            </div>
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
