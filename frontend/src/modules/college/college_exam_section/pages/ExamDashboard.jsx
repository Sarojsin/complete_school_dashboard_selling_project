import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ClipboardList, FileText, Bell, LayoutDashboard,
  Calendar, Clock, CheckCircle2, AlertCircle,
  Plus, Download, Search, Filter, Pencil, Trash2,
  BookOpen, GraduationCap, ChevronRight, ArrowUpRight
} from 'lucide-react';
import { getExamDashboardStats, getExams, getResults, getNotices } from '../api/exam';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const mockExams = [
  { id: 1, name: 'Mid-Term Physics', class_name: 'B.Sc. 2nd Year', subject: 'Physics', date: '2024-04-10', duration: 180, status: 'scheduled' },
  { id: 2, name: 'Mathematics Final', class_name: 'B.A. 1st Year', subject: 'Mathematics', date: '2024-04-14', duration: 120, status: 'scheduled' },
  { id: 3, name: 'English Unit Test', class_name: 'B.Com. 3rd Year', subject: 'English', date: '2024-03-28', duration: 90, status: 'completed' },
];
const mockResults = [
  { id: 1, exam_name: 'Chemistry Practical', class_name: 'B.Sc. 2nd Year', subject: 'Chemistry', created_at: '2024-03-25' },
  { id: 2, exam_name: 'Hindi Mid-Term', class_name: 'B.A. 1st Year', subject: 'Hindi', created_at: '2024-03-20' },
];
const mockNotices = [
  { id: 1, title: 'Board Exam Timetable Released', content: 'The board examination schedule for all UG/PG courses has been finalized.', created_at: '2024-03-28' },
  { id: 2, title: 'Hall Ticket Distribution', content: 'Hall tickets for Term 2 exams available from March 30.', created_at: '2024-03-26' },
];

const statusConfig = {
  scheduled: { variant: 'primary', icon: Clock },
  completed:  { variant: 'success', icon: CheckCircle2 },
  cancelled:  { variant: 'danger',  icon: AlertCircle },
};

const tabs = [
  { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
  { id: 'exams', label: 'Examinations', icon: ClipboardList },
  { id: 'results', label: 'Results', icon: FileText },
  { id: 'notices', label: 'Circulars', icon: Bell },
];

export default function ExamDashboard() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [exams, setExams] = useState([]);
  const [results, setResults] = useState([]);
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [er, rr, nr] = await Promise.allSettled([getExams(), getResults(), getNotices()]);
        setExams(er.value?.data?.length ? er.value.data : mockExams);
        setResults(rr.value?.data?.length ? rr.value.data : mockResults);
        setNotices(nr.value?.data?.length ? nr.value.data : mockNotices);
      } catch { setExams(mockExams); setResults(mockResults); setNotices(mockNotices); }
      finally { setLoading(false); }
    }
    load();
  }, []);

  const upcoming = exams.filter(e => new Date(e.date) >= new Date());

  const cv = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.08 } } };
  const iv = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <motion.div initial="hidden" animate="visible" variants={cv} className="p-6 lg:p-10 space-y-8">
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={iv}>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-purple-50 rounded-xl"><ClipboardList className="w-6 h-6 text-purple-500" /></div>
            <span className="text-sm font-bold text-purple-600 uppercase tracking-widest">Examination Cell</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Exam Control</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Academic performance evaluation and result governance."</p>
        </motion.div>
        <motion.div variants={iv} className="flex gap-2">
          <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl flex items-center gap-2">
            <Plus className="w-4 h-4" /> Schedule Exam
          </button>
        </motion.div>
      </section>

      {/* Tabs */}
      <motion.div variants={iv} className="flex gap-2 bg-slate-100/60 p-2 rounded-[2rem] w-fit">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={cn(
              "flex items-center gap-2 px-6 py-3 rounded-[1.5rem] text-[10px] font-black uppercase tracking-widest transition-all",
              activeTab === t.id ? "bg-white text-slate-900 shadow-lg" : "text-slate-400 hover:text-slate-700"
            )}
          >
            <t.icon className="w-4 h-4" /> {t.label}
          </button>
        ))}
      </motion.div>

      <AnimatePresence mode="wait">
        {/* ── OVERVIEW ── */}
        {activeTab === 'dashboard' && (
          <motion.div key="dashboard" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }} className="space-y-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <ModernStatCard icon={ClipboardList} title="Scheduled Exams" value={upcoming.length} trend="Upcoming" trendType="neutral" />
              <ModernStatCard icon={CheckCircle2} title="Results Posted" value={results.length} trend="This term" trendType="positive" />
              <ModernStatCard icon={Bell} title="Circulars" value={notices.length} trend="Published" trendType="neutral" />
              <ModernStatCard icon={GraduationCap} title="Classes Covered" value="12" trend="All grades" trendType="positive" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <GlassCard noPadding title="Upcoming Examinations" icon={Calendar}>
                <div className="divide-y divide-slate-100">
                  {upcoming.length === 0
                    ? <p className="p-8 text-xs text-slate-400 font-bold uppercase text-center">No exams scheduled</p>
                    : upcoming.slice(0, 4).map(e => (
                        <div key={e.id} className="p-6 flex items-center justify-between hover:bg-slate-50/50 transition-all group">
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 bg-purple-50 rounded-xl flex items-center justify-center text-purple-500">
                              <BookOpen className="w-5 h-5" />
                            </div>
                            <div>
                              <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{e.name}</p>
                              <p className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">{e.class_name} · {e.subject}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-[10px] font-black text-slate-900 uppercase">{new Date(e.date).toLocaleDateString()}</p>
                            <p className="text-[9px] text-slate-400 font-bold uppercase">{e.duration} mins</p>
                          </div>
                        </div>
                      ))
                  }
                </div>
                <button className="w-full py-5 text-[10px] font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest border-t border-slate-100 transition-all hover:bg-slate-50">
                  View All Exams
                </button>
              </GlassCard>

              <GlassCard noPadding title="Recent Results" icon={FileText}>
                <div className="divide-y divide-slate-100">
                  {results.length === 0
                    ? <p className="p-8 text-xs text-slate-400 font-bold uppercase text-center">No results posted yet</p>
                    : results.map(r => (
                        <div key={r.id} className="p-6 flex items-center justify-between hover:bg-slate-50/50 group cursor-pointer">
                          <div>
                            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{r.exam_name}</p>
                            <p className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">{r.class_name} · {r.subject}</p>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-[9px] font-black text-slate-400 uppercase">{new Date(r.created_at).toLocaleDateString()}</span>
                            <ChevronRight className="w-4 h-4 text-slate-200 group-hover:text-brand-500 transition-all" />
                          </div>
                        </div>
                      ))
                  }
                </div>
              </GlassCard>
            </div>
          </motion.div>
        )}

        {/* ── EXAMINATIONS ── */}
        {activeTab === 'exams' && (
          <motion.div key="exams" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }}>
            <GlassCard noPadding title="Exam Schedule" icon={ClipboardList}>
              <div className="p-6 border-b border-slate-100 flex gap-4">
                <div className="relative flex-1 max-w-sm">
                  <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input type="text" placeholder="Search exams..." className="w-full pl-12 pr-6 py-3 bg-slate-50 border border-slate-100 rounded-2xl text-xs font-bold outline-none focus:ring-2 focus:ring-brand-500 transition-all" />
                </div>
                <button className="p-3 border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all"><Filter className="w-5 h-5" /></button>
                <button className="p-3 border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all"><Download className="w-5 h-5" /></button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50 text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100">
                      <th className="px-8 py-4">Exam</th>
                      <th className="px-8 py-4">Class / Subject</th>
                      <th className="px-8 py-4">Date</th>
                      <th className="px-8 py-4 text-center">Duration</th>
                      <th className="px-8 py-4">Status</th>
                      <th className="px-8 py-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {exams.map(e => {
                      const cfg = statusConfig[e.status] || statusConfig.scheduled;
                      return (
                        <tr key={e.id} className="group hover:bg-slate-50/50 transition-all">
                          <td className="px-8 py-5">
                            <div className="flex items-center gap-3">
                              <div className="w-9 h-9 bg-purple-50 rounded-xl flex items-center justify-center text-purple-500">
                                <ClipboardList className="w-5 h-5" />
                              </div>
                              <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{e.name}</p>
                            </div>
                          </td>
                          <td className="px-8 py-5">
                            <p className="text-xs font-black text-slate-700 uppercase">{e.class_name}</p>
                            <p className="text-[10px] text-slate-400 font-bold uppercase italic">{e.subject}</p>
                          </td>
                          <td className="px-8 py-5">
                            <p className="text-xs font-black text-slate-900 uppercase">{new Date(e.date).toLocaleDateString()}</p>
                          </td>
                          <td className="px-8 py-5 text-center">
                            <span className="text-xs font-black text-slate-700">{e.duration} <span className="text-slate-400 font-bold">min</span></span>
                          </td>
                          <td className="px-8 py-5">
                            <ModernBadge variant={cfg.variant} size="sm">{e.status}</ModernBadge>
                          </td>
                          <td className="px-8 py-5 text-right">
                            <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                              <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all"><Pencil className="w-4 h-4" /></button>
                              <button className="p-2 border border-slate-200 text-slate-400 hover:text-rose-500 hover:border-rose-500 rounded-xl transition-all"><Trash2 className="w-4 h-4" /></button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* ── RESULTS ── */}
        {activeTab === 'results' && (
          <motion.div key="results" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }}>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest">Published Results</h3>
              <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl flex items-center gap-2">
                <Plus className="w-4 h-4" /> Post New Result
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map(r => (
                <div key={r.id} className="p-8 bg-white border border-slate-100 rounded-[3rem] shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group">
                  <div className="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center text-emerald-500 mb-6 group-hover:scale-110 transition-transform">
                    <FileText className="w-7 h-7" />
                  </div>
                  <h3 className="text-sm font-black text-slate-900 uppercase tracking-tight mb-1">{r.exam_name}</h3>
                  <p className="text-[10px] text-slate-500 font-bold uppercase mb-4">{r.class_name} · {r.subject}</p>
                  <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <span className="text-[9px] text-slate-400 font-black uppercase">{new Date(r.created_at).toLocaleDateString()}</span>
                    <button className="flex items-center gap-1 text-[9px] font-black text-brand-500 uppercase tracking-widest hover:underline">
                      View Details <ArrowUpRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* ── NOTICES ── */}
        {activeTab === 'notices' && (
          <motion.div key="notices" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }}>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest">Examination Circulars</h3>
              <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl flex items-center gap-2">
                <Plus className="w-4 h-4" /> Issue Circular
              </button>
            </div>
            <div className="space-y-4">
              {notices.map(n => (
                <div key={n.id} className="p-8 bg-white border border-slate-100 rounded-[3rem] shadow-sm hover:shadow-xl hover:-translate-y-0.5 transition-all">
                  <div className="flex items-start justify-between gap-6 mb-4">
                    <h3 className="text-sm font-black text-slate-900 uppercase tracking-tight">{n.title}</h3>
                    <span className="text-[9px] font-black text-slate-400 uppercase shrink-0">{new Date(n.created_at).toLocaleDateString()}</span>
                  </div>
                  <p className="text-xs text-slate-600 font-medium leading-relaxed italic mb-6">"{n.content}"</p>
                  <div className="flex gap-3">
                    <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all"><Pencil className="w-4 h-4" /></button>
                    <button className="p-2 border border-slate-200 text-slate-400 hover:text-rose-500 hover:border-rose-500 rounded-xl transition-all"><Trash2 className="w-4 h-4" /></button>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function cn(...c) { return c.filter(Boolean).join(' '); }
