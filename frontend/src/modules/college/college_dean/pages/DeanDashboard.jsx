import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BookOpen, Users, Trophy, Award,
  UserCircle, ChevronRight, ArrowUpRight, Clock,
  CheckCircle2, Building2, BarChart2, Target
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getDeanDashboardStats } from '../api/dean';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function DeanDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  const navigationItems = [
    { icon: Users, title: 'Faculty Departments', desc: 'Oversee all academic departments', link: '/college/dean/departments', color: 'purple' },
    { icon: Trophy, title: 'Research & Grants', desc: 'Monitor research outputs and funding', link: '/college/dean/research', color: 'pink' },
    { icon: Award, title: 'Accreditation', desc: 'Track accreditation and rankings', link: '/college/dean/accreditation', color: 'amber' },
    { icon: Target, title: 'Strategic Goals', desc: 'Academic development initiatives', link: '/college/dean/goals', color: 'emerald' },
  ];

  const recentUpdates = [
    { id: 1, title: 'NBA accreditation visit scheduled', time: '1 day ago', type: 'academic' },
    { id: 2, title: 'Research grant approved — Dr. Gupta', time: '3 days ago', type: 'research' },
    { id: 3, title: 'New PG program proposal submitted', time: '1 week ago', type: 'academic' },
  ];

  useEffect(() => {
    getDeanDashboardStats()
      .then(res => setData(res.data))
      .catch(err => { console.error('Dean Dashboard Error:', err); setData(null); })
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    total_faculties: data?.total_faculties || 120,
    total_departments: data?.total_departments || 12,
    research_projects: data?.research_projects || 45,
    accreditation_status: data?.accreditation_status || 'A+',
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
            <div className="p-2 bg-purple-50 rounded-xl">
              <BookOpen className="w-6 h-6 text-purple-500" />
            </div>
            <span className="text-sm font-bold text-purple-600 uppercase tracking-widest">Dean of Academia</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Academic Dean <span className="text-xl font-medium text-slate-400">/ College Leadership</span>
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Fostering scholarly excellence and institutional advancement."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-4 bg-white p-4 rounded-3xl border border-slate-200 shadow-sm">
          <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
            <UserCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{storedUser.full_name || 'Academic Dean'}</p>
            <ModernBadge variant="success" size="xs" className="mt-1">Verified Administrator</ModernBadge>
          </div>
        </motion.div>
      </section>

      {/* KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Users} title="Total Faculties" value={stats.total_faculties} trend="Across college" trendType="neutral" />
        <ModernStatCard icon={Building2} title="Departments" value={stats.total_departments} trend="Academic units" trendType="neutral" />
        <ModernStatCard icon={Trophy} title="Research Projects" value={stats.research_projects} trend="Active" trendType="positive" />
        <ModernStatCard icon={Award} title="Accreditation" value={stats.accreditation_status} trend="Current status" trendType="positive" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Navigation Cards */}
        <motion.div variants={iv} className="lg:col-span-2">
          <div className="mb-6 px-2">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Academic Administration</h3>
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
                  item.color === 'purple' ? 'bg-purple-50 text-purple-500' :
                  item.color === 'pink' ? 'bg-pink-50 text-pink-500' :
                  item.color === 'amber' ? 'bg-amber-50 text-amber-500' : 'bg-emerald-50 text-emerald-500'
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
            <GlassCard noPadding title="Dean's Desk" icon={Clock}>
              <div className="divide-y divide-slate-100">
                {recentUpdates.map(u => (
                  <div key={u.id} className="p-5 flex items-start gap-3 hover:bg-slate-50/50 group cursor-pointer">
                    <div className="w-8 h-8 bg-purple-50 rounded-xl flex items-center justify-center text-purple-500 shrink-0 group-hover:scale-110 transition-transform">
                      {u.type === 'report' ? <BarChart2 className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
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
            <div className="p-8 rounded-[3rem] bg-gradient-to-br from-purple-900 to-indigo-900 border border-purple-700 shadow-2xl relative overflow-hidden">
              <div className="relative z-10 text-white space-y-6">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-white/10 rounded-2xl">
                    <Target className="w-5 h-5 text-purple-300" />
                  </div>
                  <span className="text-[10px] font-black uppercase tracking-widest text-purple-200">Institutional Goal</span>
                </div>
                <p className="text-sm font-medium italic leading-relaxed">
                  "Achieve 100% faculty PhD qualification and double research publications by 2026."
                </p>
                <div className="flex items-center gap-3">
                  <div className="h-2 flex-1 bg-purple-800 rounded-full overflow-hidden">
                    <div className="h-full bg-purple-400 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                  <span className="text-xs font-bold text-purple-200">65%</span>
                </div>
              </div>
              <div className="absolute -bottom-8 -right-8 w-40 h-40 bg-purple-500/20 blur-3xl rounded-full" />
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

function cn(...c) { return c.filter(Boolean).join(' '); }
