import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Users, 
  Calendar, 
  TrendingUp, 
  CreditCard, 
  Bell, 
  MessageSquare, 
  ChevronRight, 
  MoreVertical,
  UserCircle,
  BookOpen,
  GraduationCap,
  ShieldCheck,
  Headset,
  ArrowRight
} from 'lucide-react';
import { getParentDashboard, getParentNotices } from '../api/parents';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function ParentDashboard() {
  const [children, setChildren] = useState([]);
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedChild, setSelectedChild] = useState(null);

  // Mocks for when API fails or is empty
  const mockChildren = [
    { id: 1, student_id: 'STU-2024-001', full_name: 'Alex Johnson', grade_level: 'Class 10', section: 'A', attendance: 92, performance: 'Good' },
    { id: 2, student_id: 'STU-2024-002', full_name: 'Emma Johnson', grade_level: 'Class 8', section: 'B', attendance: 88, performance: 'Excellent' },
  ];

  const mockNotices = [
    { id: 1, title: 'Parent-Teacher Meeting', date: '28 Mar 2024', content: 'The parent-teacher meeting is scheduled for April 10th. Please attend.' },
    { id: 2, title: 'Fee Payment Reminder', date: '27 Mar 2024', content: 'Last date for fee payment is March 31st.' },
  ];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const res = await getParentDashboard();
      const childrenData = res.data?.children || mockChildren;
      setChildren(childrenData);
      if (childrenData.length > 0) setSelectedChild(childrenData[0]);
      
      const noticesRes = await getParentNotices().catch(() => ({ data: mockNotices }));
      setNotices(noticesRes.data?.slice(0, 3) || mockNotices);
    } catch (err) {
      console.error('Error fetching dashboard:', err);
      setChildren(mockChildren);
      setSelectedChild(mockChildren[0]);
      setNotices(mockNotices);
    } finally {
      setLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="relative w-24 h-24">
          <div className="absolute inset-0 border-4 border-brand-500/10 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-brand-500 rounded-full border-t-transparent animate-spin"></div>
          <Users className="absolute inset-0 m-auto w-8 h-8 text-brand-500 animate-pulse" />
        </div>
      </div>
    );
  }

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="p-6 lg:p-10 space-y-8"
    >
      {/* Header & Child Selector */}
      <section className="flex flex-col lg:flex-row lg:items-end justify-between gap-8 pb-4 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <Users className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Parent Portal</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Guardian Overview</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Monitoring academic progress & school interactions.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex flex-col gap-2 min-w-[300px]">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Select Child</label>
          <div className="flex bg-white p-1.5 rounded-[1.5rem] border border-slate-200 shadow-sm">
            {children.map((child) => (
              <button
                key={child.id}
                onClick={() => setSelectedChild(child)}
                className={cn(
                  "flex-1 px-4 py-2.5 rounded-2xl text-xs font-bold transition-all",
                  selectedChild?.id === child.id 
                    ? "bg-brand-500 text-white shadow-lg shadow-brand-500/20" 
                    : "text-slate-500 hover:bg-slate-50"
                )}
              >
                {child.full_name?.split(' ')[0]}
              </button>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Main Stats with dynamic data for selected child */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard 
          icon={Calendar} 
          title="Attendance" 
          value={`${selectedChild?.attendance || 0}%`} 
          trend="Present this month" 
          trendType="neutral" 
        />
        <ModernStatCard 
          icon={GraduationCap} 
          title="Academic Rank" 
          value={selectedChild?.performance || "Good"} 
          trend="Overall performance" 
          trendType="positive" 
        />
        <ModernStatCard 
          icon={CreditCard} 
          title="Pending Fees" 
          value="â‚¹5,000" 
          trend="Due by 31st Mar" 
          trendType="warning" 
        />
      </motion.section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Child Detailed Profile Card */}
        <div className="lg:col-span-2 space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard noPadding className="overflow-hidden border-transparent hover:border-brand-200 group">
              <div className="h-32 bg-brand-500 relative">
                 <div className="absolute -bottom-12 left-8 p-1 bg-white rounded-3xl shadow-xl">
                    <div className="w-24 h-24 bg-brand-50 rounded-[1.5rem] flex items-center justify-center text-brand-500">
                       <UserCircle className="w-16 h-16" />
                    </div>
                 </div>
              </div>
              
              <div className="p-8 pt-16 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div>
                  <h3 className="text-2xl font-black text-slate-900">{selectedChild?.full_name}</h3>
                  <div className="flex items-center gap-3 mt-1">
                    <ModernBadge variant="primary" size="sm">{selectedChild?.grade_level}</ModernBadge>
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Student ID: {selectedChild?.student_id}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Link 
                    to={`/parent/child/${selectedChild?.id}/grades`}
                    className="px-6 py-3 bg-slate-900 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg active:scale-95"
                  >
                    View Grades
                  </Link>
                  <button className="p-3 border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all">
                    <MoreVertical className="w-5 h-5" />
                  </button>
                </div>
              </div>

              <div className="px-8 pb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                 <Link to={`/parent/child/${selectedChild?.id}/attendance`} className="p-4 rounded-3xl bg-slate-50 border border-slate-100 hover:border-brand-200 transition-all group/action">
                    <Calendar className="w-5 h-5 text-brand-500 mb-2" />
                    <h5 className="text-xs font-black text-slate-900 uppercase">Attendance</h5>
                    <p className="text-[10px] text-slate-400 font-bold mt-1 group-hover/action:text-brand-500">View detailed logs <ArrowRight className="inline w-3 h-3" /></p>
                 </Link>
                 <Link to={`/parent/child/${selectedChild?.id}/homework`} className="p-4 rounded-3xl bg-slate-50 border border-slate-100 hover:border-brand-200 transition-all group/action">
                    <BookOpen className="w-5 h-5 text-amber-500 mb-2" />
                    <h5 className="text-xs font-black text-slate-900 uppercase">Homework</h5>
                    <p className="text-[10px] text-slate-400 font-bold mt-1 group-hover/action:text-amber-500">Check assignments <ArrowRight className="inline w-3 h-3" /></p>
                 </Link>
                 <Link to={`/parent/chat`} className="p-4 rounded-3xl bg-slate-50 border border-slate-100 hover:border-brand-200 transition-all group/action">
                    <MessageSquare className="w-5 h-5 text-emerald-500 mb-2" />
                    <h5 className="text-xs font-black text-slate-900 uppercase">Communicate</h5>
                    <p className="text-[10px] text-slate-400 font-bold mt-1 group-hover/action:text-emerald-500">Message teacher <ArrowRight className="inline w-3 h-3" /></p>
                 </Link>
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={itemVariants}>
            <GlassCard title="Recent Activity" icon={TrendingUp}>
              <div className="space-y-6">
                {[1, 2].map((i) => (
                  <div key={i} className="flex gap-4">
                    <div className="relative">
                      <div className="w-10 h-10 rounded-xl bg-brand-50 flex items-center justify-center text-brand-500 relative z-10">
                        <ShieldCheck className="w-5 h-5" />
                      </div>
                      {i === 1 && <div className="absolute top-10 bottom-[-24px] left-1/2 -translate-x-1/2 w-0.5 bg-slate-100" />}
                    </div>
                    <div className="pt-1">
                      <h5 className="text-sm font-black text-slate-900 tracking-tight uppercase">Module Completed</h5>
                      <p className="text-xs text-slate-500 font-medium mt-1">{selectedChild?.full_name} scored 85% in Mathematics Chapter 4. <span className="text-brand-500 font-bold">Excellent work!</span></p>
                      <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest block mt-2">2 Hours Ago</span>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Sidebar */}
        <div className="space-y-8">
          {/* Notices Section */}
          <motion.div variants={itemVariants}>
            <GlassCard title="School Notices" icon={Bell}>
               <div className="space-y-4">
                  {notices.map((notice) => (
                    <div key={notice.id} className="p-4 rounded-2xl bg-amber-50/50 border border-amber-100/50 group hover:bg-white hover:border-brand-200 transition-all cursor-pointer">
                       <div className="flex justify-between items-start mb-2">
                          <h6 className="text-xs font-black text-slate-900 uppercase tracking-tight line-clamp-1">{notice.title}</h6>
                          <ModernBadge variant="danger" size="xs">NEW</ModernBadge>
                       </div>
                       <p className="text-[11px] text-slate-500 font-medium line-clamp-2 leading-relaxed">{notice.content}</p>
                       <span className="text-[9px] font-black text-amber-600 uppercase tracking-widest mt-2 block">{notice.date}</span>
                    </div>
                  ))}
                  <Link to="/parent/notices" className="w-full flex items-center justify-center gap-2 py-3 text-[10px] font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors">
                    View All Bulletin <ChevronRight className="w-3 h-3" />
                  </Link>
               </div>
            </GlassCard>
          </motion.div>

          {/* Quick Support Card */}
          <motion.div variants={itemVariants}>
            <div className="p-8 rounded-[2.5rem] bg-slate-900 border border-slate-800 shadow-2xl relative overflow-hidden group">
               <div className="relative z-10 space-y-6">
                  <div className="p-3 bg-white/10 rounded-2xl w-fit text-brand-400">
                     <Headset className="w-6 h-6" />
                  </div>
                  <div>
                     <h4 className="text-xl font-black text-white leading-tight uppercase">Need Expert <br />Support?</h4>
                     <p className="text-slate-400 text-xs font-medium mt-2">Our administration team is available 24/7 for your queries.</p>
                  </div>
                  <button className="w-full py-4 bg-brand-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 active:scale-95">
                    Contact Liaison
                  </button>
               </div>
               {/* Decorative Gradient */}
               <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/20 blur-3xl rounded-full translate-x-12 -translate-y-12 transition-transform group-hover:scale-110" />
            </div>
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

