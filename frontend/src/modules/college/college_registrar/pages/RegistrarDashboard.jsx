import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  FileCheck, Users, ClipboardList, Calendar,
  UserCircle, ChevronRight, ArrowUpRight, Clock,
  CheckCircle2, Building2, BarChart2, AlertCircle
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getRegistrarDashboardStats } from '../api/registrar';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function RegistrarDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  const navigationItems = [
    { icon: Users, title: 'Student Records', desc: 'Manage student admissions and profiles', link: '/college/registrar/students', color: 'blue' },
    { icon: ClipboardList, title: 'Enrollments', desc: 'Course enrollments and class lists', link: '/college/registrar/enrollments', color: 'emerald' },
    { icon: Calendar, title: 'Academic Calendar', desc: 'Schedules and important dates', link: '/college/registrar/calendar', color: 'purple' },
    { icon: FileCheck, title: 'Certificates', desc: 'Generate and verify certificates', link: '/college/registrar/certificates', color: 'amber' },
  ];

  const recentUpdates = [
    { id: 1, title: 'New admissions: 150 students enrolled', time: '5 hours ago', type: 'academic' },
    { id: 2, title: 'Semester enrollment deadline approaching', time: '1 day ago', type: 'urgent' },
    { id: 3, title: 'Transcript requests: 12 pending', time: '2 days ago', type: 'admin' },
  ];

  useEffect(() => {
    getRegistrarDashboardStats()
      .then(res => setData(res.data))
      .catch(err => { console.error('Registrar Dashboard Error:', err); setData(null); })
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    total_students: data?.total_students || 2540,
    enrollments_this_sem: data?.enrollments_this_sem || 2100,
    certificates_issued: data?.certificates_issued || 145,
    pending_tasks: data?.pending_tasks || 18,
  };

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
            <div className="p-2 bg-amber-50 rounded-xl">
              <FileCheck className="w-6 h-6 text-amber-500" />
            </div>
            <span className="text-sm font-bold text-amber-600 uppercase tracking-widest">Registrar Office</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            College Registrar <span className="text-xl font-medium text-slate-400">/ Academic Records</span>
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Keeper of academic history and student records."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-4 bg-white p-4 rounded-3xl border border-slate-200 shadow-sm">
          <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
            <UserCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{storedUser.full_name || 'Registrar'}</p>
            <ModernBadge variant="success" size="xs" className="mt-1">Verified Administrator</ModernBadge>
          </div>
        </motion.div>
      </section>

      {/* KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Users} title="Total Students" value={stats.total_students} trend="Enrolled" trendType="neutral" />
        <ModernStatCard icon={ClipboardList} title="Enrollments" value={stats.enrollments_this_sem} trend="This semester" trendType="positive" />
        <ModernStatCard icon={FileCheck} title="Certificates Issued" value={stats.certificates_issued} trend="This year" trendType="neutral" />
        <ModernStatCard icon={AlertCircle} title="Pending Tasks" value={stats.pending_tasks} trend="Requires attention" trendType="danger" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Navigation Cards */}
        <motion.div variants={iv} className="lg:col-span-2">
          <div className="mb-6 px-2">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Registrar Services</h3>
          </div>
          <div className="grid grid-cols-2 gap-6">
            {navigationItems.map(item => (
              <Link
                key={item.title}
                to={item.link}
                className="group p-8 bg-white border border-slate-100 rounded-[3rem] shadow-sm hover:shadow-2xl hover:shadow-brand-500/10 hover:-translate-y-2 transition-all overflow-hidden relative"
              >
                <div className={cn(
                  "w-14 h-14 rounded-[1.5rem] mb-6 flex items-center justify-center transition-all group-hover:scale-110 group-hover:rotate-6",
                  item.color === 'blue' ? 'bg-blue-50 text-blue-500' :
                  item.color === 'emerald' ? 'bg-emerald-50 text-emerald-500' :
                  item.color === 'purple' ? 'bg-purple-50 text-purple-500' : 'bg-amber-50 text-amber-500'
                )}>
                  <item.icon className="w-7 h-7" />
                </div>
                <h4 className="text-xs font-black text-slate-900 uppercase tracking-tight mb-1">{item.title}</h4>
                <p className="text-[10px] text-slate-500 font-medium leading-relaxed italic">{item.desc}</p>
                <div className="absolute top-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity">
                  <ArrowUpRight className="w-5 h-5 text-slate-300" />
                </div>
                <div className="absolute bottom-0 right-0 w-28 h-28 bg-slate-50 rounded-full translate-x-14 translate-y-14 -z-10 group-hover:bg-brand-50 transition-colors" />
              </Link>
            ))}
          </div>
        </motion.div>

        {/* Right column: Updates */}
        <div className="space-y-8">
          <motion.div variants={iv}>
            <GlassCard noPadding title="Recent Activity" icon={Clock}>
              <div className="divide-y divide-slate-100">
                {recentUpdates.map(u => (
                  <div key={u.id} className="p-5 flex items-start gap-3 hover:bg-slate-50/50 group cursor-pointer">
                    <div className="w-8 h-8 bg-amber-50 rounded-xl flex items-center justify-center text-amber-500 shrink-0 group-hover:scale-110 transition-transform">
                      {u.type === 'urgent' ? <AlertCircle className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
                    </div>
                    <div className="min-w-0">
                      <p className="text-[10px] font-black text-slate-900 uppercase tracking-tight leading-tight">{u.title}</p>
                      <span className="text-[9px] text-slate-400 font-bold uppercase">{u.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={iv}>
            <div className="p-8 rounded-[3rem] bg-slate-900 border border-slate-800 shadow-2xl relative overflow-hidden">
              <div className="relative z-10 text-white space-y-6">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-white/10 rounded-2xl">
                    <BarChart2 className="w-5 h-5 text-amber-400" />
                  </div>
                  <span className="text-[10px] font-black uppercase tracking-widest text-slate-300">Quick Stats</span>
                </div>
                <div className="space-y-3">
                  {[
                    { label: 'Total Students', value: stats.total_students },
                    { label: 'Semester Enrollments', value: stats.enrollments_this_sem },
                    { label: 'Pending Tasks', value: stats.pending_tasks },
                  ].map(r => (
                    <div key={r.label} className="flex justify-between items-center py-3 border-b border-white/10">
                      <span className="text-[10px] font-black text-slate-400 uppercase">{r.label}</span>
                      <span className="text-sm font-black text-white">{r.value}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="absolute -bottom-8 -right-8 w-36 h-36 bg-amber-500/10 blur-3xl rounded-full" />
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

function cn(...c) { return c.filter(Boolean).join(' '); }
