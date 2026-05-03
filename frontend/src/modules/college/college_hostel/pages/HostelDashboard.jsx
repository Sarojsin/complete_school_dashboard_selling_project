import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Home, Users, Bed, Calendar,
  UserCircle, ChevronRight, ArrowUpRight, Clock,
  CheckCircle2, AlertTriangle, Key
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getHostelDashboardStats, getHostels, getStudents } from '../api/hostel';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const mockStats = { total_hostels: 6, total_rooms: 240, occupied_rooms: 198, available_beds: 42 };
const mockHostels = [
  { id: 1, name: 'Boys Hostel A', warden: 'Dr. Rajesh Kumar', total_rooms: 80, occupied: 78, type: 'Boys' },
  { id: 2, name: 'Girls Hostel B', warden: 'Dr. Meena Sharma', total_rooms: 60, occupied: 58, type: 'Girls' },
  { id: 3, name: 'International Hostel', warden: 'Prof. Alan Smith', total_rooms: 100, occupied: 62, type: 'Mixed' },
];
const mockResidents = [
  { id: 1, name: 'Amit Kumar', roll_number: 'CS2021-001', hostel: 'Boys Hostel A', room_no: 'A-101', check_in: '2024-01-10' },
  { id: 2, name: 'Priya Singh', roll_number: 'PH2021-045', hostel: 'Girls Hostel B', room_no: 'B-203', check_in: '2024-01-12' },
  { id: 3, name: 'Rahul Verma', roll_number: 'MATH2020-023', hostel: 'International Hostel', room_no: 'I-056', check_in: '2023-08-15' },
];

export default function HostelDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  const navigationItems = [
    { icon: Home, title: 'Hostel List', desc: 'Manage hostel buildings and wards', link: '/college/hostel/hostels', color: 'orange' },
    { icon: Bed, title: 'Room Allocation', desc: 'Assign rooms to students', link: '/college/hostel/rooms', color: 'blue' },
    { icon: Users, title: 'Residents', desc: 'View current hostel occupants', link: '/college/hostel/residents', color: 'purple' },
    { icon: Calendar, title: 'Schedule', desc: 'In-out timings and visits', link: '/college/hostel/schedule', color: 'emerald' },
  ];

  useEffect(() => {
    getHostelDashboardStats()
      .then(res => setData(res.data))
      .catch(err => { console.error('Hostel Dashboard Error:', err); setData(null); })
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    total_hostels: data?.total_hostels || mockStats.total_hostels,
    total_rooms: data?.total_rooms || mockStats.total_rooms,
    occupied_rooms: data?.occupied_rooms || mockStats.occupied_rooms,
    available_beds: data?.available_beds || mockStats.available_beds,
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
            <div className="p-2 bg-orange-50 rounded-xl">
              <Home className="w-6 h-6 text-orange-500" />
            </div>
            <span className="text-sm font-bold text-orange-600 uppercase tracking-widest">Hostel Management</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Residence Hub <span className="text-xl font-medium text-slate-400">/ Student Housing</span>
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Providing comfortable living spaces for scholars."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-4 bg-white p-4 rounded-3xl border border-slate-200 shadow-sm">
          <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
            <UserCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{storedUser.full_name || 'Hostel Warden'}</p>
            <ModernBadge variant="success" size="xs" className="mt-1">Verified Staff</ModernBadge>
          </div>
        </motion.div>
      </section>

      {/* KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Home} title="Hostels" value={stats.total_hostels} trend="Buildings" trendType="neutral" />
        <ModernStatCard icon={Bed} title="Total Rooms" value={stats.total_rooms} trend="Capacity" trendType="neutral" />
        <ModernStatCard icon={Users} title="Occupied" value={stats.occupied_rooms} trend="Currently filled" trendType="positive" />
        <ModernStatCard icon={Key} title="Available Beds" value={stats.available_beds} trend="Free slots" trendType="warning" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Navigation Cards */}
        <motion.div variants={iv} className="lg:col-span-2">
          <div className="mb-6 px-2">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Hostel Operations</h3>
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
                  item.color === 'orange' ? 'bg-orange-50 text-orange-500' :
                  item.color === 'blue' ? 'bg-blue-50 text-blue-500' :
                  item.color === 'purple' ? 'bg-purple-50 text-purple-500' : 'bg-emerald-50 text-emerald-500'
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

        {/* Residents List */}
        <div className="space-y-8">
          <motion.div variants={iv}>
            <GlassCard noPadding title="Current Residents" icon={Users}>
              <div className="divide-y divide-slate-100">
                {mockResidents.map(r => (
                  <div key={r.id} className="p-4 flex items-center gap-3 hover:bg-slate-50/50 group">
                    <div className="w-10 h-10 bg-orange-50 rounded-xl flex items-center justify-center text-orange-500">
                      <UserCircle className="w-5 h-5" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{r.name}</p>
                      <p className="text-[9px] text-slate-400">{r.roll_number} · {r.hostel}</p>
                    </div>
                    <div className="ml-auto text-right">
                      <p className="text-xs font-black text-slate-700">{r.room_no}</p>
                      <p className="text-[9px] text-slate-400">Since {r.check_in}</p>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={iv}>
            <GlassCard noPadding title="Hostel Occupancy" icon={Home}>
              <div className="p-4 space-y-4">
                {mockHostels.map(h => {
                  const occupancy = Math.round((h.occupied / h.total_rooms) * 100);
                  return (
                    <div key={h.id} className="p-4 bg-slate-50 rounded-xl">
                      <div className="flex justify-between items-center mb-2">
                        <p className="text-xs font-black text-slate-900 uppercase">{h.name}</p>
                        <span className="text-[10px] font-bold text-slate-600">{occupancy}%</span>
                      </div>
                      <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div className="h-full bg-orange-500 rounded-full" style={{ width: `${occupancy}%` }}></div>
                      </div>
                      <p className="text-[9px] text-slate-400 mt-2">{h.occupied}/{h.total_rooms} rooms occupied</p>
                    </div>
                  );
                })}
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

function cn(...c) { return c.filter(Boolean).join(' '); }


