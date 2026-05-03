import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, 
  Users, 
  UserPlus, 
  UserCheck, 
  BookOpen, 
  IndianRupee, 
  TrendingUp, 
  Activity, 
  Bell, 
  Settings, 
  Search, 
  LogOut,
  ChevronRight,
  PieChart,
  Calendar,
  Layers,
  Building2,
  Lock,
  ArrowUpRight,
  Briefcase,
  GraduationCap
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { getAuthorityDashboard } from '../api/authority';
import { logout } from '../../../auth/api/auth';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function AuthorityDashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    fetchDashboardData();
    return () => clearInterval(timer);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const res = await getAuthorityDashboard();
      setData(res.data);
    } catch (err) {
      console.error("Authority Dashboard Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const mockStats = {
    total_students: 1248,
    total_teachers: 86,
    active_courses: 42,
    revenue_growth: '+12.5%',
    attendance_rate: '94.2%',
    pending_tasks: 8
  };

  const modules = [
    { id: 'students', label: 'Enrollment', icon: Users, color: 'blue', path: '/authority/students', count: '1,248' },
    { id: 'teachers', label: 'Faculty', icon: UserCheck, color: 'emerald', path: '/authority/teachers', count: '86' },
    { id: 'finance', label: 'Treasury', icon: IndianRupee, color: 'amber', path: '/authority/fees', count: '₹4.2M' },
    { id: 'academics', label: 'Curriculum', icon: BookOpen, color: 'purple', path: '/authority/courses', count: '42' },
    { id: 'announcements', label: 'Directives', icon: Bell, color: 'rose', path: '/authority/notices', count: '12' },
    { id: 'infrastructure', label: 'Facilities', icon: Building2, color: 'slate', path: '/authority/departments', count: '8' },
  ];

  const recentEvents = [
    { id: 1, type: 'enrollment', title: 'New Admission', user: 'Rahul Sharma', time: '10 mins ago', status: 'verified' },
    { id: 2, type: 'finance', title: 'Audit Completed', user: 'Account Section', time: '1 hour ago', status: 'system' },
    { id: 3, type: 'academic', title: 'Board Results In', user: 'Exam Controller', time: '4 hours ago', status: 'urgent' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="relative">
           <div className="w-16 h-16 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
           <ShieldCheck className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-6 h-6 text-brand-500" />
        </div>
      </div>
    );
  }

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="p-6 lg:p-10 space-y-10 bg-slate-50/50 min-h-screen"
    >
      {/* Top Navigation Bar */}
      <section className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2.5 bg-brand-500 rounded-2xl shadow-lg shadow-brand-500/20 text-white">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <span className="text-xs font-black text-brand-600 uppercase tracking-[0.2em]">Institutional Command</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight flex items-baseline gap-3">
             Administrator <span className="text-xl font-medium text-slate-400">/ Dashboard</span>
          </h1>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-4 bg-white p-2 pl-6 rounded-3xl border border-slate-200 shadow-sm">
           <div className="text-right">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{time.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' })}</p>
              <p className="text-sm font-black text-slate-900 tabular-nums">{time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
           </div>
           <div className="w-[1px] h-8 bg-slate-100 mx-2" />
           <button onClick={() => navigate('/authority/profile')} className="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center text-slate-500 hover:text-brand-500 hover:bg-brand-50 transition-all">
              <Settings className="w-6 h-6" />
           </button>
           <button onClick={logout} className="w-12 h-12 bg-rose-50 rounded-2xl flex items-center justify-center text-rose-500 hover:bg-rose-500 hover:text-white transition-all">
              <LogOut className="w-6 h-6" />
           </button>
        </motion.div>
      </section>

      {/* Primary Analytics Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
         <ModernStatCard 
            icon={Users} 
            title="Active Enrollment" 
            value={mockStats.total_students.toLocaleString()} 
            trend="+24 This Month" 
            trendType="positive" 
         />
         <ModernStatCard 
            icon={Activity} 
            title="School Attendance" 
            value={mockStats.attendance_rate} 
            trend="Above threshold" 
            trendType="positive" 
         />
         <ModernStatCard 
            icon={IndianRupee} 
            title="Monthly Revenue" 
            value="₹12.8L" 
            trend="Budget on track" 
            trendType="neutral" 
         />
         <ModernStatCard 
            icon={TrendingUp} 
            title="Institutional Growth" 
            value={mockStats.revenue_growth} 
            trend="Annual projected" 
            trendType="positive" 
         />
      </motion.section>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
         {/* Center: Admin Module Grid */}
         <div className="xl:col-span-2 space-y-8">
            <motion.div variants={itemVariants}>
               <div className="flex items-center justify-between mb-6 px-2">
                  <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] flex items-center gap-2">
                     <Layers className="w-4 h-4" /> Operational Modules
                  </h3>
                  <button className="text-[10px] font-black text-brand-500 uppercase tracking-widest hover:underline decoration-2 underline-offset-4">Customize Layout</button>
               </div>
               
               <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                  {modules.map((mod) => (
                    <Link 
                      key={mod.id} 
                      to={mod.path}
                      className="group relative bg-white p-8 rounded-[3rem] border border-slate-200 shadow-sm hover:shadow-2xl hover:shadow-brand-500/10 hover:-translate-y-2 transition-all overflow-hidden"
                    >
                       <div className={cn(
                          "w-14 h-14 rounded-[1.5rem] mb-6 flex items-center justify-center transition-all group-hover:scale-110 group-hover:rotate-6",
                          mod.color === 'blue' ? "bg-blue-50 text-blue-500" :
                          mod.color === 'emerald' ? "bg-emerald-50 text-emerald-500" :
                          mod.color === 'amber' ? "bg-amber-50 text-amber-500" :
                          mod.color === 'purple' ? "bg-purple-50 text-purple-500" :
                          mod.color === 'rose' ? "bg-rose-50 text-rose-500" : "bg-slate-50 text-slate-500"
                       )}>
                          <mod.icon className="w-7 h-7" />
                       </div>
                       
                       <div className="space-y-1">
                          <h4 className="text-xs font-black text-slate-400 uppercase tracking-wider">{mod.label}</h4>
                          <span className="text-3xl font-black text-slate-900">{mod.count}</span>
                       </div>

                       <div className="absolute top-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity">
                          <ArrowUpRight className="w-5 h-5 text-slate-300" />
                       </div>
                       
                       {/* Decorative Gradient Overlay */}
                       <div className="absolute bottom-0 right-0 w-32 h-32 bg-slate-50 rounded-full translate-x-16 translate-y-16 -z-10 group-hover:bg-brand-50 transition-colors" />
                    </Link>
                  ))}
               </div>
            </motion.div>

            {/* Institutional Health & Analytics */}
            <motion.div variants={itemVariants}>
               <GlassCard title="Academic Synergy" icon={PieChart}>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
                     <div className="relative flex items-center justify-center">
                        {/* Custom SVG Gauge */}
                        <svg className="w-56 h-56 transform -rotate-90">
                           <circle cx="112" cy="112" r="100" stroke="currentColor" strokeWidth="24" fill="transparent" className="text-slate-100" />
                           <circle cx="112" cy="112" r="100" stroke="currentColor" strokeWidth="24" fill="transparent" strokeDasharray={628} strokeDashoffset={628 * (1 - 0.75)} className="text-brand-500 transition-all duration-1000" />
                        </svg>
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
                           <span className="text-4xl font-black text-slate-900">75%</span>
                           <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">GPA Target</p>
                        </div>
                     </div>
                     <div className="space-y-6">
                        <div className="space-y-2">
                           <div className="flex justify-between items-end">
                              <span className="text-xs font-black text-slate-900 uppercase">Faculty Efficiency</span>
                              <span className="text-xs font-black text-emerald-500 uppercase">92%</span>
                           </div>
                           <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                              <motion.div initial={{ width: 0 }} animate={{ width: '92%' }} className="h-full bg-emerald-500" />
                           </div>
                        </div>
                        <div className="space-y-2">
                           <div className="flex justify-between items-end">
                              <span className="text-xs font-black text-slate-900 uppercase">Resources Utilization</span>
                              <span className="text-xs font-black text-blue-500 uppercase">68%</span>
                           </div>
                           <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                              <motion.div initial={{ width: 0 }} animate={{ width: '68%' }} className="h-full bg-blue-500" />
                           </div>
                        </div>
                        <p className="text-xs font-medium text-slate-500 leading-loose italic pt-4">
                           "System data indicates high operational resonance. Academic metrics are currently tracking 4.2% above previous quarterly benchmarks."
                        </p>
                     </div>
                  </div>
               </GlassCard>
            </motion.div>
         </div>

         {/* Right Side: Activity & Verification */}
         <div className="space-y-8">
            <motion.div variants={itemVariants}>
               <GlassCard noPadding title="Strategic Logs" icon={Activity}>
                  <div className="divide-y divide-slate-100">
                     {recentEvents.map(event => (
                       <div key={event.id} className="p-6 hover:bg-slate-50/50 transition-all group flex items-start gap-4 cursor-pointer">
                          <div className={cn(
                             "w-10 h-10 rounded-xl flex items-center justify-center shrink-0",
                             event.status === 'urgent' ? "bg-rose-50 text-rose-500" : "bg-brand-50 text-brand-500"
                          )}>
                             {event.type === 'enrollment' ? <UserPlus className="w-5 h-5" /> : event.type === 'finance' ? <Lock className="w-5 h-5" /> : <GraduationCap className="w-5 h-5" />}
                          </div>
                          <div className="flex-1 min-w-0">
                             <div className="flex justify-between items-start mb-1">
                                <h4 className="text-xs font-black text-slate-900 uppercase truncate pr-2">{event.title}</h4>
                                <span className="text-[9px] font-black text-slate-400 uppercase shrink-0">{event.time}</span>
                             </div>
                             <p className="text-[10px] text-slate-500 font-medium">Identity: {event.user}</p>
                             <div className="flex items-center gap-1.5 mt-2">
                                <ModernBadge variant={event.status === 'urgent' ? 'danger' : 'success'} size="xs" className="px-2">
                                   {event.status}
                                </ModernBadge>
                             </div>
                          </div>
                          <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-brand-500 transition-all mt-1" />
                       </div>
                     ))}
                  </div>
                  <button className="w-full py-5 text-[10px] font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest border-t border-slate-100 transition-all hover:bg-slate-50">
                     View Complete System Audit
                  </button>
               </GlassCard>
            </motion.div>

            <motion.div variants={itemVariants}>
               <div className="p-8 rounded-[3rem] bg-slate-900 border border-slate-800 shadow-2xl relative overflow-hidden group">
                  <div className="relative z-10 text-white space-y-8">
                     <div className="flex justify-between items-start">
                        <div className="p-3 bg-white/10 rounded-2xl">
                           <Briefcase className="w-6 h-6 text-brand-400" />
                        </div>
                        <ModernBadge variant="warning" size="sm">Staff Alerts</ModernBadge>
                     </div>
                     <div>
                        <h4 className="text-xl font-black leading-tight uppercase">HR Optimization <br />Pending Review</h4>
                        <p className="text-slate-400 text-[10px] font-medium mt-3 leading-relaxed">
                           3 teaching positions are currently awaiting interview scheduling for the upcoming academic session.
                        </p>
                     </div>
                     <button className="w-full py-4 bg-brand-500 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg active:scale-95">
                        Initiate Hiring Flow
                     </button>
                  </div>
                  <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/10 blur-3xl rounded-full translate-x-12 -translate-y-12" />
               </div>
            </motion.div>

            {/* Quick Navigation Drawer/Panel */}
            <motion.div variants={itemVariants}>
               <GlassCard title="Quick Directives" icon={ShieldCheck}>
                  <div className="grid grid-cols-2 gap-4">
                     {['Add Student', 'Post Notice', 'Fee Setup', 'Class Load'].map((act, i) => (
                        <button key={i} className="p-4 rounded-2xl bg-white border border-slate-100 hover:border-brand-500 hover:text-brand-500 transition-all text-left group">
                           <p className="text-[10px] font-black text-slate-900 uppercase mb-1 group-hover:text-brand-500">{act}</p>
                           <ArrowUpRight className="w-3 h-3 text-slate-300 group-hover:text-brand-500 transition-all" />
                        </button>
                     ))}
                  </div>
               </GlassCard>
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
