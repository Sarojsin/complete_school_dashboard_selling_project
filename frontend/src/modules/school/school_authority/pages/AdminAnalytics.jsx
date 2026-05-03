import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BarChart2,
  ChevronLeft,
  Users,
  UserCheck,
  IndianRupee,
  Activity,
  TrendingUp,
  TrendingDown,
  Calendar,
  GraduationCap,
  BookOpen,
  AlertCircle,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  ShieldCheck,
  Zap
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getStudentAnalytics, getAttendanceAnalytics } from '../api/authority';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

// ── Mini Bar Chart (no external lib needed) ─────────────────────────
function MiniBarChart({ data, color = 'bg-brand-500' }) {
  const max = Math.max(...data.map(d => d.value));
  return (
    <div className="flex items-end gap-1.5 h-24">
      {data.map((d, i) => (
        <div key={i} className="flex-1 flex flex-col items-center gap-1.5">
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: `${(d.value / max) * 100}%` }}
            transition={{ duration: 0.6, delay: i * 0.05 }}
            className={`w-full ${color} rounded-t-lg min-h-[4px]`}
          />
          <span className="text-[8px] font-black text-slate-400 uppercase">{d.label}</span>
        </div>
      ))}
    </div>
  );
}

// ── Horizontal Bar ─────────────────────────────────────────────────
function HBar({ label, value, max, color, subtitle }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between items-end">
        <div>
          <span className="text-xs font-black text-slate-900 uppercase tracking-tight">{label}</span>
          {subtitle && <p className="text-[9px] text-slate-400 font-bold uppercase">{subtitle}</p>}
        </div>
        <span className={`text-xs font-black uppercase tracking-widest ${color.replace('bg-', 'text-')}`}>{value}%</span>
      </div>
      <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${(value / max) * 100}%` }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className={`h-full ${color} rounded-full`}
        />
      </div>
    </div>
  );
}

export default function AdminAnalytics() {
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState(null);

  const mockAnalytics = {
    total_students: 1248,
    total_teachers: 86,
    attendance_rate: 94,
    avg_gpa: 8.2,
    revenue: '₹48.6L',
    pending_fees: '₹12.1L',
  };

  const enrollmentTrend = [
    { label: 'Jul', value: 820 },
    { label: 'Aug', value: 1050 },
    { label: 'Sep', value: 1100 },
    { label: 'Oct', value: 1080 },
    { label: 'Nov', value: 1200 },
    { label: 'Dec', value: 1230 },
    { label: 'Jan', value: 1248 },
  ];

  const revenueTrend = [
    { label: 'Jul', value: 420 },
    { label: 'Aug', value: 650 },
    { label: 'Sep', value: 720 },
    { label: 'Oct', value: 580 },
    { label: 'Nov', value: 800 },
    { label: 'Dec', value: 760 },
    { label: 'Jan', value: 890 },
  ];

  const deptPerformance = [
    { label: 'Physics', value: 88, color: 'bg-blue-500', subtitle: '14 faculty' },
    { label: 'Mathematics', value: 76, color: 'bg-purple-500', subtitle: '12 faculty' },
    { label: 'Literature', value: 92, color: 'bg-emerald-500', subtitle: '9 faculty' },
    { label: 'Engineering', value: 71, color: 'bg-amber-500', subtitle: '11 faculty' },
    { label: 'Biology', value: 85, color: 'bg-rose-500', subtitle: '8 faculty' },
  ];

  const alerts = [
    { id: 1, type: 'warning', title: 'Low Attendance in Grade 12', desc: 'Attendance dropped to 78% this week.', icon: AlertCircle },
    { id: 2, type: 'success', title: 'Q1 Results Outstanding', desc: 'Average GPA increased by 0.4 points.', icon: CheckCircle2 },
    { id: 3, type: 'info', title: 'Fee Collection Target Near', desc: '89% of term fees collected — on track.', icon: Zap },
  ];

  useEffect(() => {
    async function load() {
      try {
        const [sa] = await Promise.allSettled([getStudentAnalytics()]);
        setAnalytics(sa.value?.data || mockAnalytics);
      } catch {
        setAnalytics(mockAnalytics);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const data = analytics || mockAnalytics;

  const cvariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.09 } }
  };
  const iv = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } };

  if (loading) {
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
      variants={cvariants}
      className="p-6 lg:p-10 space-y-8"
    >
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={iv}>
          <Link
            to="/authority/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Dashboard
          </Link>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-purple-50 rounded-xl">
              <BarChart2 className="w-6 h-6 text-purple-500" />
            </div>
            <span className="text-sm font-bold text-purple-600 uppercase tracking-widest">Institutional Intelligence</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">School Analytics</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Data-driven governance for evidence-based institutional decisions."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-3">
          <select className="pl-6 pr-10 py-4 bg-white border border-slate-200 rounded-2xl text-[10px] font-black uppercase tracking-widest text-slate-600 outline-none appearance-none cursor-pointer shadow-sm">
            <option>Current Term</option>
            <option>Last Term</option>
            <option>Annual 2024</option>
          </select>
          <button className="p-4 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all shadow-sm">
            <ArrowUpRight className="w-5 h-5" />
          </button>
        </motion.div>
      </section>

      {/* Top KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Users}         title="Enrollment"       value={data.total_students?.toLocaleString() || '1,248'} trend="+2.1% MoM"     trendType="positive" />
        <ModernStatCard icon={Activity}      title="Attendance Rate"  value={`${data.attendance_rate || 94}%`}                  trend="Above KPI"     trendType="positive" />
        <ModernStatCard icon={GraduationCap} title="Average GPA"      value={data.avg_gpa || '8.2'}                             trend="Target 8.0"    trendType="positive" />
        <ModernStatCard icon={IndianRupee}   title="Annual Revenue"   value={data.revenue || '₹48.6L'}                          trend="Budget aligned" trendType="neutral" />
      </motion.section>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Enrollment Trend */}
        <motion.div variants={iv}>
          <GlassCard title="Enrollment Trend" icon={TrendingUp}>
            <MiniBarChart data={enrollmentTrend} color="bg-brand-500" />
            <div className="mt-6 pt-6 border-t border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-3xl font-black text-slate-900">+428</span>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">New students since July</p>
              </div>
              <ModernBadge variant="success" size="sm">+52% YOY</ModernBadge>
            </div>
          </GlassCard>
        </motion.div>

        {/* Revenue Trend */}
        <motion.div variants={iv}>
          <GlassCard title="Monthly Revenue (₹K)" icon={IndianRupee}>
            <MiniBarChart data={revenueTrend} color="bg-amber-500" />
            <div className="mt-6 pt-6 border-t border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-3xl font-black text-slate-900">₹48.6L</span>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">Cumulative annual collection</p>
              </div>
              <ModernBadge variant="warning" size="sm">₹12.1L pending</ModernBadge>
            </div>
          </GlassCard>
        </motion.div>
      </div>

      {/* Department Performance + Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Department Performance */}
        <motion.div variants={iv} className="lg:col-span-2">
          <GlassCard title="Departmental Performance" icon={BookOpen}>
            <div className="space-y-7">
              {deptPerformance.map(dept => (
                <HBar
                  key={dept.label}
                  label={dept.label}
                  value={dept.value}
                  max={100}
                  color={dept.color}
                  subtitle={dept.subtitle}
                />
              ))}
            </div>
            <div className="mt-8 pt-6 border-t border-slate-100 grid grid-cols-3 gap-4">
              {[
                { label: 'Highest GPA', value: 'Literature', color: 'text-emerald-500' },
                { label: 'Needs Focus', value: 'Engineering', color: 'text-amber-500' },
                { label: 'Most Staff',  value: 'Physics',     color: 'text-blue-500' },
              ].map(c => (
                <div key={c.label} className="text-center p-4 bg-slate-50 rounded-2xl">
                  <p className={`text-xs font-black uppercase tracking-tight ${c.color}`}>{c.value}</p>
                  <p className="text-[9px] text-slate-400 font-bold uppercase mt-1">{c.label}</p>
                </div>
              ))}
            </div>
          </GlassCard>
        </motion.div>

        {/* Alerts & Insights */}
        <motion.div variants={iv} className="space-y-6">
          <GlassCard noPadding title="Live Alerts" icon={Zap}>
            <div className="divide-y divide-slate-100">
              {alerts.map(a => (
                <div key={a.id} className="p-6 hover:bg-slate-50/50 transition-colors flex items-start gap-4 group cursor-pointer">
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 transition-transform group-hover:scale-110 ${
                    a.type === 'warning' ? 'bg-amber-50 text-amber-500' :
                    a.type === 'success' ? 'bg-emerald-50 text-emerald-500' : 'bg-brand-50 text-brand-500'
                  }`}>
                    <a.icon className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-xs font-black text-slate-900 uppercase tracking-tight leading-tight">{a.title}</p>
                    <p className="text-[10px] text-slate-500 font-medium mt-1 leading-relaxed italic">{a.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </GlassCard>

          {/* Attendance Pulse */}
          <div className="p-8 rounded-[3rem] bg-slate-900 border border-slate-800 shadow-2xl relative overflow-hidden">
            <div className="relative z-10 text-white space-y-6">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-white/10 rounded-2xl">
                  <Activity className="w-5 h-5 text-emerald-400" />
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest text-slate-300">Today's Pulse</span>
              </div>
              <div>
                <span className="text-5xl font-black">94%</span>
                <p className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mt-2">School-wide attendance</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '94%' }}
                    transition={{ duration: 1 }}
                    className="h-full bg-emerald-400 rounded-full"
                  />
                </div>
                <TrendingUp className="w-4 h-4 text-emerald-400" />
              </div>
            </div>
            <div className="absolute -bottom-8 -right-8 w-40 h-40 bg-emerald-500/10 blur-3xl rounded-full" />
          </div>
        </motion.div>
      </div>

      {/* Bottom Summary */}
      <motion.div variants={iv}>
        <GlassCard title="Institutional Summary" icon={ShieldCheck}>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { label: 'Active Courses',    value: '42',  icon: BookOpen,      color: 'text-blue-500',    bg: 'bg-blue-50' },
              { label: 'Pending Admissions', value: '18',  icon: UserCheck,     color: 'text-amber-500',   bg: 'bg-amber-50' },
              { label: 'Exam Schedules',    value: '5',   icon: Calendar,      color: 'text-purple-500',  bg: 'bg-purple-50' },
              { label: 'Staff On Leave',    value: '3',   icon: Clock,         color: 'text-rose-500',    bg: 'bg-rose-50' },
            ].map(item => (
              <div key={item.label} className="p-6 rounded-3xl border border-slate-100 bg-slate-50/50 hover:bg-white hover:border-brand-200 transition-all cursor-pointer group">
                <div className={`w-12 h-12 ${item.bg} rounded-2xl flex items-center justify-center ${item.color} mb-4 group-hover:scale-110 transition-transform`}>
                  <item.icon className="w-6 h-6" />
                </div>
                <span className="text-3xl font-black text-slate-900">{item.value}</span>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">{item.label}</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </motion.div>
    </motion.div>
  );
}
