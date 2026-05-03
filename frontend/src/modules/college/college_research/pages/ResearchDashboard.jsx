import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Microscope, FlaskConical, Trophy, Award,
  UserCircle, ChevronRight, ArrowUpRight, Clock,
  CheckCircle2, TrendingUp, BookOpen, Star
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getResearchDashboardStats, getResearchProjects, getPublications, getGrants } from '../api/research';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const mockStats = { active_projects: 34, publications_this_year: 87, total_grants: 12, grant_value: 25000000 };
const mockProjects = [
  { id: 1, title: 'Nanomaterials for Energy Storage', PI: 'Dr. Rajesh Kumar', funding: 2500000, status: 'ongoing', start_date: '2023-01-01' },
  { id: 2, title: 'AI in Healthcare Diagnostics', PI: 'Dr. Meena Sharma', funding: 1800000, status: 'ongoing', start_date: '2023-06-01' },
  { id: 3, title: 'Climate Change Impact on Agriculture', PI: 'Dr. Suresh Patel', funding: 3200000, status: 'completed', start_date: '2022-01-01' },
];
const mockPublications = [
  { id: 1, title: 'Advanced Catalysis using Quantum Dots', journal: 'Nature Materials', authors: 'Kumar et al.', year: 2024, citations: 12 },
  { id: 2, title: 'Machine Learning for Drug Discovery', journal: 'Science Advances', authors: 'Sharma et al.', year: 2024, citations: 8 },
  { id: 3, title: 'Sustainable Waste Management', journal: 'Environmental Science', authors: 'Patel et al.', year: 2023, citations: 24 },
];

export default function ResearchDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  const navigationItems = [
    { icon: Microscope, title: 'Research Projects', desc: 'Track ongoing and completed projects', link: '/college/research/projects', color: 'pink' },
    { icon: BookOpen, title: 'Publications', desc: 'Manage research papers and citations', link: '/college/research/publications', color: 'purple' },
    { icon: Trophy, title: 'Grants & Funding', desc: 'Monitor research grants and budgets', link: '/college/research/grants', color: 'amber' },
    { icon: Star, title: 'Achievements', desc: 'Awards and recognitions', link: '/college/research/achievements', color: 'emerald' },
  ];

  useEffect(() => {
    getResearchDashboardStats()
      .then(res => setData(res.data))
      .catch(err => { console.error('Research Dashboard Error:', err); setData(null); })
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    active_projects: data?.active_projects || mockStats.active_projects,
    publications_this_year: data?.publications_this_year || mockStats.publications_this_year,
    total_grants: data?.total_grants || mockStats.total_grants,
    grant_value: data?.grant_value || mockStats.grant_value,
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
            <div className="p-2 bg-pink-50 rounded-xl">
              <Microscope className="w-6 h-6 text-pink-500" />
            </div>
            <span className="text-sm font-bold text-pink-600 uppercase tracking-widest">Research & Innovation</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Research Hub <span className="text-xl font-medium text-slate-400">/ Scholarly Excellence</span>
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Cultivating discovery and advancing knowledge frontiers."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-4 bg-white p-4 rounded-3xl border border-slate-200 shadow-sm">
          <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
            <UserCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{storedUser.full_name || 'Research Coordinator'}</p>
            <ModernBadge variant="success" size="xs" className="mt-1">Verified Staff</ModernBadge>
          </div>
        </motion.div>
      </section>

      {/* KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Microscope} title="Active Projects" value={stats.active_projects} trend="Ongoing" trendType="positive" />
        <ModernStatCard icon={BookOpen} title="Publications" value={stats.publications_this_year} trend="This year" trendType="neutral" />
        <ModernStatCard icon={Trophy} title="Grants Awarded" value={stats.total_grants} trend="Active grants" trendType="positive" />
        <ModernStatCard icon={TrendingUp} title="Total Funding" value={`₹${(stats.grant_value / 10000000).toFixed(1)}Cr`} trend="Value" trendType="positive" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Navigation Cards */}
        <motion.div variants={iv} className="lg:col-span-2">
          <div className="mb-6 px-2">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Research Administration</h3>
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
                  item.color === 'pink' ? 'bg-pink-50 text-pink-500' :
                  item.color === 'purple' ? 'bg-purple-50 text-purple-500' :
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

        {/* Right column: Projects & Publications */}
        <div className="space-y-8">
          <motion.div variants={iv}>
            <GlassCard noPadding title="Active Projects" icon={Clock}>
              <div className="divide-y divide-slate-100">
                {mockProjects.filter(p => p.status === 'ongoing').map(p => (
                  <div key={p.id} className="p-5 flex items-start gap-3 hover:bg-slate-50/50 group">
                    <div className="w-8 h-8 bg-pink-50 rounded-xl flex items-center justify-center text-pink-500 shrink-0">
                      <FlaskConical className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-[10px] font-black text-slate-900 uppercase tracking-tight leading-tight">{p.title}</p>
                      <span className="text-[9px] text-slate-400 font-bold uppercase">PI: {p.PI} · ₹{(p.funding / 100000).toFixed(0)}L</span>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={iv}>
            <GlassCard noPadding title="Recent Publications" icon={Award}>
              <div className="divide-y divide-slate-100">
                {mockPublications.slice(0, 3).map(pub => (
                  <div key={pub.id} className="p-4 hover:bg-slate-50/50 group">
                    <p className="text-xs font-black text-slate-900 uppercase tracking-tight leading-tight mb-1">{pub.title}</p>
                    <p className="text-[9px] text-slate-400">{pub.journal} · {pub.year}</p>
                    <p className="text-[9px] text-slate-400 mt-1">{pub.citations} citations</p>
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

function cn(...c) { return c.filter(Boolean).join(' '); }


