import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Users, 
  BookOpen, 
  CheckSquare, 
  ClipboardList, 
  PlusCircle, 
  Calendar, 
  FileText, 
  Video, 
  Megaphone,
  ChevronRight,
  TrendingUp,
  Clock,
  LogOut
} from 'lucide-react';
import { getTeacherDashboard } from '../api/teachers';
import { logout } from '../../../auth/api/auth';
import GlassCard from '../../../shared/components/GlassCard';
import ModernStatCard from '../../../shared/components/ModernStatCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function TeacherDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTeacherDashboard()
      .then(res => setDashboard(res))
      .catch(err => {
        console.error("Teacher Dashboard Error:", err);
        setDashboard(null);
      })
      .finally(() => setLoading(false));
  }, []);

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
        <div className="relative w-20 h-20">
          <div className="absolute inset-0 border-4 border-brand-500/20 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-brand-500 rounded-full border-t-transparent animate-spin"></div>
        </div>
      </div>
    );
  }

  const stats = {
    total_students: dashboard?.total_students || 124, // Mock if null
    active_courses: dashboard?.my_courses_count || 5,
    pending_grading: dashboard?.pending_grading_count || 12,
    upcoming_tests: dashboard?.upcoming_tests || 3,
  };

  const actions = [
    { label: 'View Students', icon: Users, link: '/teacher/students', color: 'bg-indigo-50 text-indigo-600 border-indigo-100' },
    { label: 'Add Assignment', icon: PlusCircle, link: '/teacher/assignments/create', color: 'bg-emerald-50 text-emerald-600 border-emerald-100' },
    { label: 'Take Attendance', icon: ClipboardList, link: '/teacher/attendance', color: 'bg-sky-50 text-sky-600 border-sky-100' },
    { label: 'Upload Notes', icon: FileText, link: '/teacher/notes/upload', color: 'bg-amber-50 text-amber-600 border-amber-100' },
    { label: 'Upload Video', icon: Video, link: '/teacher/videos/upload', color: 'bg-rose-50 text-rose-600 border-rose-100' },
    { label: 'Create Notice', icon: Megaphone, link: '/teacher/notices/create', color: 'bg-slate-50 text-slate-600 border-slate-100' },
  ];

  const courses = dashboard?.courses || [
    { id: 1, name: 'Advanced Engineering Mathematics', student_count: 42, pending: 5 },
    { id: 2, name: 'Intro to Quantum Computing', student_count: 28, pending: 0 },
    { id: 3, name: 'Data Structures & Algorithms', student_count: 54, pending: 7 },
  ];

  const schedule = dashboard?.schedule || [
    { time: '09:00 AM', title: 'Mathematics L-4', description: 'Section A - Room 402', status: 'Completed' },
    { time: '11:30 AM', title: 'Quantum Computing', description: 'Section B - Lab 1', status: 'Ongoing' },
    { time: '02:00 PM', title: 'Staff Meeting', description: 'Main Conference Hall', status: 'Upcoming' },
  ];

  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="p-6 lg:p-10 space-y-10"
    >
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <BookOpen className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Faculty Management</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Teacher Dashboard
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">
            Welcome back, <span className="text-slate-900 font-bold">{dashboard?.full_name || storedUser.full_name || 'Professor'}</span>. Here's your mission overview.
          </p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <div className="flex bg-slate-100 p-1 rounded-2xl">
            <button className="px-5 py-2.5 text-xs font-bold text-slate-500 hover:text-slate-700 transition-all">Today</button>
            <button className="px-5 py-2.5 text-xs font-bold bg-white text-brand-500 rounded-xl shadow-sm transition-all border border-brand-100">Weekly</button>
          </div>
          <button 
            onClick={logout}
            className="p-3 bg-rose-50 text-rose-600 rounded-2xl hover:bg-rose-100 transition-all border border-rose-100"
            title="Sign Out"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </motion.div>
      </section>

      {/* Stats Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={Users} title="Total Students" value={stats.total_students} trend="+4 new this month" trendType="positive" />
        <ModernStatCard icon={BookOpen} title="My Courses" value={stats.active_courses} trend="3 Departments" trendType="neutral" />
        <ModernStatCard icon={CheckSquare} title="Pending Grading" value={stats.pending_grading} trend="Due by Friday" trendType="negative" />
        <ModernStatCard icon={TrendingUp} title="Class Avg" value="82%" trend="↑ 4% performance" trendType="positive" />
      </motion.section>

      {/* Quick Actions Grid */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <PlusCircle className="w-4 h-4" /> Quick Tools
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {actions.map((action, i) => (
            <Link 
              key={i} 
              to={action.link}
              className={cn(
                "group p-6 rounded-3xl border flex flex-col items-center justify-center gap-3 transition-all hover:scale-105 active:scale-95 text-center shadow-sm",
                action.color
              )}
            >
              <action.icon className="w-8 h-8 group-hover:rotate-12 transition-transform" />
              <span className="text-xs font-black uppercase tracking-tight leading-tight">{action.label}</span>
            </Link>
          ))}
        </div>
      </motion.section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Active Courses List */}
        <div className="lg:col-span-2 space-y-6">
          <motion.div variants={itemVariants}>
            <GlassCard 
              title="Academic Modules" 
              icon={BookOpen} 
              action={<Link to="/teacher/courses" className="text-xs font-black text-brand-500 hover:text-brand-600 uppercase tracking-widest flex items-center gap-1">View All <ChevronRight className="w-3 h-3" /></Link>}
              noPadding
            >
              <div className="divide-y divide-slate-100">
                {courses.map((course, i) => (
                  <div key={i} className="group p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/50 transition-colors">
                    <div>
                      <h4 className="text-lg font-black text-slate-900 group-hover:text-brand-500 transition-colors">{course.name}</h4>
                      <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1 flex items-center gap-2">
                        <Users className="w-3 h-3" /> {course.student_count} Students Enrolled
                      </p>
                    </div>
                    <div className="flex items-center gap-3 self-end md:self-auto">
                      {course.pending > 0 && (
                        <ModernBadge variant="warning" size="sm">
                          {course.pending} Pending Submissions
                        </ModernBadge>
                      )}
                      <Link 
                        to={`/teacher/courses/${course.id}`} 
                        className="p-3 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-2xl transition-all shadow-sm group-hover:shadow-md"
                      >
                        <ChevronRight className="w-5 h-5" />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={itemVariants}>
            <GlassCard title="Recent Performance Insight" icon={TrendingUp}>
              <div className="flex items-center gap-6 p-4 bg-emerald-50 rounded-2xl border border-emerald-100">
                <div className="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center">
                  <span className="text-2xl font-black text-emerald-600">A+</span>
                </div>
                <div>
                  <h5 className="text-sm font-black text-slate-900 uppercase">Class Excellence Award</h5>
                  <p className="text-xs text-slate-500 font-medium mt-1 leading-relaxed">
                    Mathematics L-4 has achieved an average score of 88% in the last unit test. Great job!
                  </p>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Schedule & Timeline */}
        <div className="space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard title="Today's Timeline" icon={Calendar}>
              <div className="space-y-8 relative before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-100">
                {schedule.map((slot, i) => (
                  <div key={i} className="relative pl-10">
                    {/* Dot */}
                    <div className={cn(
                      "absolute left-1.5 top-1.5 w-3.5 h-3.5 rounded-full border-4 border-white shadow-sm ring-2",
                      slot.status === 'Completed' ? "ring-emerald-500 bg-emerald-500" :
                      slot.status === 'Ongoing' ? "ring-brand-500 bg-brand-500 animate-pulse" :
                      "ring-slate-300 bg-slate-300"
                    )} />
                    
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-1">
                        <Clock className="w-3 h-3" /> {slot.time}
                      </span>
                      <ModernBadge 
                        variant={slot.status === 'Completed' ? 'success' : slot.status === 'Ongoing' ? 'primary' : 'neutral'} 
                        size="sm"
                      >
                        {slot.status}
                      </ModernBadge>
                    </div>
                    <h5 className="text-sm font-black text-slate-900">{slot.title}</h5>
                    <p className="text-[10px] text-slate-500 font-medium mt-0.5 uppercase tracking-widest">{slot.description}</p>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          {/* Quick Notice Card */}
          <motion.div variants={itemVariants}>
            <GlassCard title="Quick Notice" icon={Megaphone}>
              <div className="space-y-4">
                <textarea 
                  placeholder="Post an announcement to your classes..." 
                  className="w-full min-h-[100px] p-4 bg-slate-50 border border-slate-100 rounded-2xl text-sm focus:ring-2 focus:ring-brand-500 outline-none transition-all placeholder:text-slate-400"
                />
                <button className="w-full py-4 bg-brand-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 active:scale-95">
                  Broadcast Now
                </button>
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
