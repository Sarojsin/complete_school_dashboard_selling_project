import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  FlaskConical, Microscope, Calendar, Users,
  UserCircle, ChevronRight, ArrowUpRight, Clock,
  CheckCircle2, Plus, Wrench, AlertTriangle
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getLabDashboardStats, getLabSchedules, getLabEquipments, getLabBookings } from '../api/lab';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const mockStats = { total_labs: 12, active_bookings: 18, equipment_count: 156, maintenance_due: 5 };
const mockSchedules = [
  { id: 1, lab_name: 'Physics Lab A', experiment: 'Wave Optics', faculty: 'Dr. Sharma', time: '09:00 AM - 12:00 PM', date: '2024-04-01' },
  { id: 2, lab_name: 'Chemistry Lab B', experiment: 'Organic Synthesis', faculty: 'Dr. Gupta', time: '02:00 PM - 05:00 PM', date: '2024-04-01' },
  { id: 3, lab_name: 'Computer Lab 1', experiment: 'Python Programming', faculty: 'Prof. Singh', time: '10:00 AM - 12:00 PM', date: '2024-04-02' },
];
const mockEquipments = [
  { id: 1, name: 'Spectrophotometer', lab: 'Physics Lab A', status: 'operational', last_maintained: '2024-01-15' },
  { id: 2, name: 'Centrifuge Machine', lab: 'Chemistry Lab B', status: 'operational', last_maintained: '2024-02-10' },
  { id: 3, name: 'Oscilloscope', lab: 'Electronics Lab', status: 'maintenance', last_maintained: '2023-11-20' },
];

export default function LabDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  const navigationItems = [
    { icon: Calendar, title: 'Lab Schedule', desc: 'View and manage lab timetables', link: '/college/lab/schedule', color: 'cyan' },
    { icon: Microscope, title: 'Experiments', desc: 'Design and review lab experiments', link: '/college/lab/experiments', color: 'blue' },
    { icon: Wrench, title: 'Equipment', desc: 'Inventory and maintenance tracking', link: '/college/lab/equipment', color: 'amber' },
    { icon: Users, title: 'Bookings', desc: 'Approve/reject lab booking requests', link: '/college/lab/bookings', color: 'purple' },
  ];

  useEffect(() => {
    getLabDashboardStats()
      .then(res => setData(res.data))
      .catch(err => { console.error('Lab Dashboard Error:', err); setData(null); })
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    total_labs: data?.total_labs || mockStats.total_labs,
    active_bookings: data?.active_bookings || mockStats.active_bookings,
    equipment_count: data?.equipment_count || mockStats.equipment_count,
    maintenance_due: data?.maintenance_due || mockStats.maintenance_due,
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
            <div className="p-2 bg-cyan-50 rounded-xl">
              <FlaskConical className="w-6 h-6 text-cyan-500" />
            </div>
            <span className="text-sm font-bold text-cyan-600 uppercase tracking-widest">Laboratory Division</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Lab Hub <span className="text-xl font-medium text-slate-400">/ Practical Learning</span>
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Where theory meets hands-on experimentation."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-4 bg-white p-4 rounded-3xl border border-slate-200 shadow-sm">
          <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
            <UserCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{storedUser.full_name || 'Lab In-Charge'}</p>
            <ModernBadge variant="success" size="xs" className="mt-1">Verified Staff</ModernBadge>
          </div>
        </motion.div>
      </section>

      {/* KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={FlaskConical} title="Total Labs" value={stats.total_labs} trend="Facilities" trendType="neutral" />
        <ModernStatCard icon={Calendar} title="Active Bookings" value={stats.active_bookings} trend="This week" trendType="positive" />
        <ModernStatCard icon={Microscope} title="Equipments" value={stats.equipment_count} trend="Total inventory" trendType="neutral" />
        <ModernStatCard icon={AlertTriangle} title="Maintenance Due" value={stats.maintenance_due} trend="Needs attention" trendType="danger" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Navigation Cards */}
        <motion.div variants={iv} className="lg:col-span-2">
          <div className="mb-6 px-2">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Lab Management</h3>
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
                  item.color === 'cyan' ? 'bg-cyan-50 text-cyan-500' :
                  item.color === 'blue' ? 'bg-blue-50 text-blue-500' :
                  item.color === 'amber' ? 'bg-amber-50 text-amber-500' : 'bg-purple-50 text-purple-500'
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

        {/* Recent Schedules */}
        <div className="space-y-8">
          <motion.div variants={iv}>
            <GlassCard noPadding title="Today's Schedule" icon={Clock}>
              <div className="divide-y divide-slate-100">
                {mockSchedules.map(s => (
                  <div key={s.id} className="p-5 flex items-start gap-3 hover:bg-slate-50/50 group">
                    <div className="w-8 h-8 bg-cyan-50 rounded-xl flex items-center justify-center text-cyan-500 shrink-0">
                      <FlaskConical className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-[10px] font-black text-slate-900 uppercase tracking-tight leading-tight">{s.lab_name}</p>
                      <span className="text-[9px] text-slate-400 font-bold uppercase">{s.experiment} · {s.time}</span>
                      <p className="text-[9px] text-slate-400">Faculty: {s.faculty}</p>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={iv}>
            <GlassCard noPadding title="Equipment Status" icon={Wrench}>
              <div className="divide-y divide-slate-100">
                {mockEquipments.map(e => (
                  <div key={e.id} className="p-4 flex items-center justify-between hover:bg-slate-50/50 group">
                    <div>
                      <p className="text-xs font-black text-slate-900">{e.name}</p>
                      <p className="text-[9px] text-slate-400">{e.lab}</p>
                    </div>
                    <ModernBadge variant={e.status === 'operational' ? 'success' : 'warning'} size="xs">
                      {e.status}
                    </ModernBadge>
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


