import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Info, 
  ChevronLeft, 
  ChevronRight,
  TrendingUp,
  AlertCircle,
  FileText
} from 'lucide-react';
import { getStudentAttendance } from '../api/students';
import GlassCard from '../../../shared/components/GlassCard';
import ModernStatCard from '../../../shared/components/ModernStatCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function AttendancePage() {
  const [attendance, setAttendance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentMonth, setCurrentMonth] = useState(new Date());

  useEffect(() => {
    getStudentAttendance()
      .then(data => setAttendance(data))
      .catch(err => console.error("Attendance Fetch Error:", err))
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

  // Mock calendar data logic (simplified for UI demonstration)
  const daysInMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0).getDate();
  const firstDayOfMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1).getDay();
  const calendarDays = Array.from({ length: 42 }, (_, i) => {
    const day = i - firstDayOfMonth + 1;
    if (day <= 0 || day > daysInMonth) return null;
    
    // Random status for demo (1=Present, 2=Absent, 3=Late, 4=Holiday)
    const status = Math.random() > 0.1 ? 1 : Math.random() > 0.5 ? 2 : 3;
    const isWeekend = (day + firstDayOfMonth - 1) % 7 === 0 || (day + firstDayOfMonth - 1) % 7 === 6;
    return { day, status: isWeekend ? 0 : status };
  });

  const getStatusIcon = (status) => {
    switch (status) {
      case 1: return <CheckCircle2 className="w-5 h-5 text-emerald-500" />;
      case 2: return <XCircle className="w-5 h-5 text-rose-500" />;
      case 3: return <Clock className="w-5 h-5 text-amber-500" />;
      case 0: return <div className="w-1.5 h-1.5 rounded-full bg-slate-200" />;
      default: return null;
    }
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
              <Calendar className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Attendance Record</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Attendance Tracker</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Monitor your presence and stay compliant with institutional policies.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <button className="px-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold hover:bg-slate-50 transition-all shadow-sm flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Leave Request
          </button>
          <div className="flex bg-slate-100 p-1 rounded-2xl">
            <button className="p-2 rounded-xl text-slate-500 hover:bg-white hover:shadow-sm transition-all"><ChevronLeft className="w-5 h-5" /></button>
            <span className="px-4 py-2 text-sm font-bold text-slate-700">
              {currentMonth.toLocaleString('default', { month: 'long', year: 'numeric' })}
            </span>
            <button className="p-2 rounded-xl text-slate-500 hover:bg-white hover:shadow-sm transition-all"><ChevronRight className="w-5 h-5" /></button>
          </div>
        </motion.div>
      </section>

      {/* Stats Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={TrendingUp} title="Overall Attendance" value="94.2%" trend="Required: 75%" trendType="positive" />
        <ModernStatCard icon={CheckCircle2} title="Present Days" value="112" trend="Total classes: 119" trendType="positive" />
        <ModernStatCard icon={XCircle} title="Total Absence" value="7" trend="5 with permission" trendType="neutral" />
        <ModernStatCard icon={Clock} title="Late Arrivals" value="3" trend="Focus on punctuality" trendType="negative" />
      </motion.section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Calendar Card */}
        <div className="lg:col-span-2">
          <motion.div variants={itemVariants}>
            <GlassCard title="Attendance Calendar" icon={Calendar}>
              <div className="grid grid-cols-7 gap-px bg-slate-100 rounded-2xl overflow-hidden border border-slate-100">
                {['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].map(day => (
                  <div key={day} className="bg-slate-50 py-4 text-center text-[10px] font-black text-slate-400 tracking-widest">{day}</div>
                ))}
                {calendarDays.map((date, i) => (
                  <div key={i} className="bg-white min-h-[100px] p-2 relative group hover:bg-slate-50 transition-colors">
                    {date && (
                      <>
                        <span className="text-sm font-bold text-slate-400 group-hover:text-brand-500 transition-colors">{date.day}</span>
                        <div className="absolute inset-0 flex items-center justify-center">
                          {getStatusIcon(date.status)}
                        </div>
                      </>
                    )}
                  </div>
                ))}
              </div>
              
              <div className="mt-8 flex flex-wrap justify-center gap-6 pt-6 border-t border-slate-100">
                <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-emerald-500" /> <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Present</span></div>
                <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-rose-500" /> <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Absent</span></div>
                <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-amber-500" /> <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Late</span></div>
                <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-slate-200" /> <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Holiday / Weekend</span></div>
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Sidebar Insights */}
        <div className="space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard title="Attendance Policy" icon={Info}>
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-brand-50 border border-brand-100">
                  <h4 className="text-xs font-black text-brand-700 uppercase mb-2">Requirement</h4>
                  <p className="text-sm font-medium text-brand-900 leading-relaxed">
                    A minimum of <span className="font-black">75% attendance</span> is required to sit for the final examinations.
                  </p>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold uppercase tracking-wider">
                    <span className="text-slate-500">Your Standing</span>
                    <span className="text-emerald-600">Secure</span>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 rounded-full" style={{ width: '94%' }}></div>
                  </div>
                </div>
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={itemVariants}>
            <GlassCard title="Recent Remarks" icon={AlertCircle}>
              <div className="space-y-4">
                {[
                  { date: 'Oct 12', remark: 'Sick leave approved.', type: 'info' },
                  { date: 'Oct 05', remark: 'Late arrival - Transportation issue.', type: 'warning' },
                ].map((r, i) => (
                  <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex gap-3">
                    <div className="shrink-0 pt-1">
                      {r.type === 'info' ? <CheckCircle2 className="w-4 h-4 text-emerald-500" /> : <AlertCircle className="w-4 h-4 text-amber-500" />}
                    </div>
                    <div>
                      <span className="text-[10px] font-black text-slate-400 uppercase">{r.date}</span>
                      <p className="text-xs font-bold text-slate-700 mt-1">{r.remark}</p>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}
