import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Zap, Users, Activity, Database, HardDrive, ShieldCheck,
  Settings, FileText, Archive, BarChart2, BookOpen, Wifi,
  CreditCard, Bell, Globe, Lock, Server, TrendingUp,
  AlertCircle, CheckCircle2, Clock, ArrowUpRight, LogOut
} from 'lucide-react';
import { getAdminDashboard } from '../api/superadmin';
import { logout } from '../../auth/api/auth';
import GlassCard from '../../shared/components/GlassCard';
import ModernBadge from '../../shared/components/ModernBadge';
import ModernStatCard from '../../shared/components/ModernStatCard';

// ─── Module registry ──────────────────────────────────────────────────────────
const modules = [
  { path: '/admin/users',        icon: Users,       label: 'User Management',    color: 'blue',    desc: 'Manage all platform users' },
  { path: '/admin/academic',     icon: BookOpen,    label: 'Academic Config',    color: 'purple',  desc: 'Courses, terms, curricula' },
  { path: '/admin/finance',      icon: CreditCard,  label: 'Financial Ops',      color: 'amber',   desc: 'Revenue, billing, ledgers' },
  { path: '/admin/features',     icon: Zap,         label: 'Feature Matrix',     color: 'emerald', desc: 'Toggle platform features' },
  { path: '/admin/audit-logs',   icon: FileText,    label: 'Audit Spectrum',     color: 'rose',    desc: 'All system activity logs' },
  { path: '/admin/settings',     icon: Settings,    label: 'System Tuning',      color: 'slate',   desc: 'Platform-wide config' },
  { path: '/admin/system',       icon: Server,      label: 'System Monitor',     color: 'cyan',    desc: 'Memory, CPU, uptime' },
  { path: '/admin/security',     icon: Lock,        label: 'Security Control',   color: 'red',     desc: 'Auth, tokens, firewall' },
  { path: '/admin/backups',      icon: Archive,     label: 'Data Backups',       color: 'teal',    desc: 'Scheduled & manual backups' },
  { path: '/admin/reports',      icon: BarChart2,   label: 'Global Reports',     color: 'violet',  desc: 'Performance analytics' },
  { path: '/admin/communication',icon: Bell,        label: 'Communications',     color: 'orange',  desc: 'Announcements, broadcasts' },
  { path: '/admin/notices',      icon: Globe,       label: 'Admin Notices',      color: 'indigo',  desc: 'System-wide notices' },
];

const systemHealth = [
  { label: 'Database',        value: 98, status: 'Healthy', variant: 'success' },
  { label: 'API Server',      value: 99, status: 'Online',  variant: 'success' },
  { label: 'Cache Layer',     value: 95, status: 'Active',  variant: 'success' },
  { label: 'Background Jobs', value: 60, status: '2 Pending', variant: 'warning' },
  { label: 'Storage',         value: 45, status: '45% Used',  variant: 'primary' },
];

const recentActivity = [
  { id: 1, action: 'New authority registered',         role: 'authority',    time: '2m ago', type: 'user' },
  { id: 2, action: 'Auto-backup completed',             role: 'system',       time: '1h ago', type: 'system' },
  { id: 3, action: 'Feature "assignments" toggled ON', role: 'super_admin',  time: '3h ago', type: 'config' },
  { id: 4, action: 'Security scan — 0 threats',        role: 'system',       time: '6h ago', type: 'security' },
  { id: 5, action: 'Q1 reports generated',              role: 'super_admin',  time: 'Yesterday', type: 'report' },
];

const colorMap = {
  blue:   { icon: 'bg-blue-50 text-blue-500',   glow: 'hover:shadow-blue-100' },
  purple: { icon: 'bg-purple-50 text-purple-500', glow: 'hover:shadow-purple-100' },
  amber:  { icon: 'bg-amber-50 text-amber-500',  glow: 'hover:shadow-amber-100' },
  emerald:{ icon: 'bg-emerald-50 text-emerald-500', glow: 'hover:shadow-emerald-100' },
  rose:   { icon: 'bg-rose-50 text-rose-500',   glow: 'hover:shadow-rose-100' },
  slate:  { icon: 'bg-slate-100 text-slate-500', glow: 'hover:shadow-slate-100' },
  cyan:   { icon: 'bg-cyan-50 text-cyan-500',   glow: 'hover:shadow-cyan-100' },
  red:    { icon: 'bg-red-50 text-red-500',     glow: 'hover:shadow-red-100' },
  teal:   { icon: 'bg-teal-50 text-teal-500',   glow: 'hover:shadow-teal-100' },
  violet: { icon: 'bg-violet-50 text-violet-500', glow: 'hover:shadow-violet-100' },
  orange: { icon: 'bg-orange-50 text-orange-500', glow: 'hover:shadow-orange-100' },
  indigo: { icon: 'bg-indigo-50 text-indigo-500', glow: 'hover:shadow-indigo-100' },
};

const activityColor = {
  user:     'bg-blue-50 text-blue-500',
  system:   'bg-emerald-50 text-emerald-500',
  config:   'bg-purple-50 text-purple-500',
  security: 'bg-rose-50 text-rose-500',
  report:   'bg-amber-50 text-amber-500',
};

function cn(...c) { return c.filter(Boolean).join(' '); }

export default function SuperAdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    getAdminDashboard()
      .then(res => setStats(res.data))
      .catch(err => { console.error('Super Admin Dashboard Error:', err); setStats(null); })
      .finally(() => setLoading(false));

    const tick = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(tick);
  }, []);

  const cv = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.07 } } };
  const iv = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <motion.div initial="hidden" animate="visible" variants={cv} className="p-6 lg:p-10 space-y-10">

      {/* ── Header ── */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={iv}>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-slate-900 rounded-xl">
              <Zap className="w-6 h-6 text-amber-400" />
            </div>
            <span className="text-sm font-bold text-slate-500 uppercase tracking-widest">Root Access</span>
          </div>
          <h1 className="text-5xl font-black text-slate-900 tracking-tighter leading-none">System<br/>Command</h1>
          <p className="text-slate-500 text-base mt-3 font-medium italic max-w-lg">
            "Omniscient oversight of all modules, users, security, and institutional infrastructure."
          </p>
        </motion.div>

        <motion.div variants={iv} className="flex flex-col items-end gap-4">
          {/* Live clock */}
          <div className="px-8 py-4 bg-slate-900 rounded-[2rem] text-right shadow-2xl">
            <div className="text-2xl font-black text-white font-mono tracking-widest">
              {time.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
            </div>
            <p className="text-[9px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">
              {time.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}
            </p>
          </div>
          <div className="flex gap-3">
            <Link to="/admin/settings" className="px-6 py-3 border border-slate-200 rounded-2xl text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-brand-500 hover:border-brand-500 transition-all flex items-center gap-2">
              <Settings className="w-4 h-4" /> Settings
            </Link>
            <button
              onClick={() => { logout(); window.location.href = '/login'; }}
              className="px-6 py-3 border border-rose-200 rounded-2xl text-[10px] font-black uppercase tracking-widest text-rose-400 hover:text-rose-600 hover:border-rose-400 transition-all flex items-center gap-2"
            >
              <LogOut className="w-4 h-4" /> Logout
            </button>
          </div>
        </motion.div>
      </section>

      {/* ── KPI Row ── */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Users}      title="Total Users"       value={stats?.total_users       || 1342}      trend="All roles"       trendType="positive" />
        <ModernStatCard icon={Wifi}       title="Active Sessions"   value={stats?.active_sessions   || 48}        trend="Right now"       trendType="neutral" />
        <ModernStatCard icon={Activity}   title="System Health"     value={stats?.system_health     || 'Optimal'} trend="All systems go"  trendType="positive" />
        <ModernStatCard icon={HardDrive}  title="Storage Used"      value="45%"                                   trend="of 500 GB"       trendType="warning" />
      </motion.section>

      {/* ── Module Grid ── */}
      <motion.section variants={iv}>
        <div className="mb-6 flex items-center justify-between">
          <div>
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-1">Administrative Control Plane</p>
            <h2 className="text-2xl font-black text-slate-900">Management Modules</h2>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
          {modules.map((m, i) => {
            const cfg = colorMap[m.color] || colorMap.slate;
            return (
              <motion.div
                key={m.path}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.04 }}
              >
                <Link
                  to={m.path}
                  className={cn(
                    "group flex flex-col items-center text-center p-6 bg-white border border-slate-100 rounded-[2.5rem] shadow-sm",
                    "hover:shadow-2xl hover:-translate-y-2 transition-all duration-300",
                    cfg.glow
                  )}
                >
                  <div className={cn("w-14 h-14 rounded-[1.5rem] flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all", cfg.icon)}>
                    <m.icon className="w-7 h-7" />
                  </div>
                  <span className="text-[10px] font-black text-slate-900 uppercase tracking-tight leading-tight">{m.label}</span>
                  <span className="text-[9px] text-slate-400 font-medium mt-1 leading-tight hidden group-hover:block transition-all">{m.desc}</span>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </motion.section>

      {/* ── Bottom Row: System Health + Activity ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* System Health */}
        <motion.div variants={iv} className="lg:col-span-2">
          <GlassCard title="System Integrity" icon={ShieldCheck}>
            <div className="space-y-6">
              {systemHealth.map(s => (
                <div key={s.label}>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-black text-slate-900 uppercase tracking-tight">{s.label}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-[10px] font-black text-slate-400 uppercase">{s.value}%</span>
                      <ModernBadge variant={s.variant} size="xs">{s.status}</ModernBadge>
                    </div>
                  </div>
                  <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${s.value}%` }}
                      transition={{ duration: 0.8, delay: 0.3 }}
                      className={cn(
                        "h-full rounded-full",
                        s.variant === 'success' ? 'bg-emerald-400' :
                        s.variant === 'warning' ? 'bg-amber-400'  : 'bg-brand-500'
                      )}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 grid grid-cols-3 gap-4 pt-6 border-t border-slate-100">
              {[
                { label: 'Uptime',    value: '99.9%',    icon: TrendingUp    },
                { label: 'Incidents', value: '0 Active', icon: AlertCircle   },
                { label: 'Last Scan', value: '6h ago',   icon: Clock         },
              ].map(m => (
                <div key={m.label} className="text-center p-4 bg-slate-50 rounded-2xl">
                  <m.icon className="w-5 h-5 text-slate-400 mx-auto mb-2" />
                  <p className="text-sm font-black text-slate-900">{m.value}</p>
                  <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-0.5">{m.label}</p>
                </div>
              ))}
            </div>
          </GlassCard>
        </motion.div>

        {/* Activity Log */}
        <motion.div variants={iv}>
          <GlassCard noPadding title="System Activity" icon={Activity}>
            <div className="divide-y divide-slate-100">
              {recentActivity.map(a => (
                <div key={a.id} className="p-5 flex items-start gap-3 hover:bg-slate-50/50 cursor-pointer group">
                  <div className={cn("w-8 h-8 rounded-xl flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform", activityColor[a.type])}>
                    {a.type === 'user'     && <Users className="w-4 h-4" />}
                    {a.type === 'system'   && <Server className="w-4 h-4" />}
                    {a.type === 'config'   && <Settings className="w-4 h-4" />}
                    {a.type === 'security' && <Lock className="w-4 h-4" />}
                    {a.type === 'report'   && <BarChart2 className="w-4 h-4" />}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-[10px] font-black text-slate-900 uppercase tracking-tight leading-tight">{a.action}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[9px] text-slate-400 font-bold uppercase">{a.time}</span>
                      <span className="w-1 h-1 bg-slate-200 rounded-full" />
                      <span className="text-[9px] text-slate-400 font-bold uppercase">{a.role}</span>
                    </div>
                  </div>
                  <ArrowUpRight className="w-3.5 h-3.5 text-slate-200 group-hover:text-brand-500 transition-all shrink-0 mt-0.5" />
                </div>
              ))}
            </div>
            <button className="w-full py-5 text-[10px] font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest border-t border-slate-100 transition-all hover:bg-slate-50">
              View Full Audit Trail →
            </button>
          </GlassCard>
        </motion.div>
      </div>
    </motion.div>
  );
}
