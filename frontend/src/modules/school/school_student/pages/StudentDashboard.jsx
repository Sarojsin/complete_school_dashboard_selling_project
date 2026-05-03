import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  GraduationCap, CalendarCheck, BookOpen, Clock, 
  TrendingUp, AlertCircle, Bell, LogOut, ChevronRight,
  Video, FileText, Library, FileCheck, Users, Shield, Receipt, Award
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { logout } from '../../../auth/api/auth';
import api from '../../../shared/api/client';
import GlassCard from '../../../shared/components/GlassCard';
import ModernStatCard from '../../../shared/components/ModernStatCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [data, setData] = useState({
    dashboard: null,
    assignments: [],
    tests: [],
    notices: [],
    notes: [],
    videos: [],
    grades: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // Correct API prefix with /school handling the 404 error
        const [dashRes, asmRes, testRes, noteRes, videoRes, gradesRes, noticeRes] = await Promise.allSettled([
          api.get('/school/students/dashboard'),
          api.get('/school/students/my-assignments'),
          api.get('/school/students/my-tests'),
          api.get('/school/students/my-notes'),
          api.get('/school/students/my-videos'),
          api.get('/school/students/my-grades'),
          api.get('/school/students/my-notices')
        ]);

        setData({
          dashboard: dashRes.status === 'fulfilled' ? dashRes.value.data : null,
          assignments: asmRes.status === 'fulfilled' ? asmRes.value.data : [],
          tests: testRes.status === 'fulfilled' ? testRes.value.data : [],
          notes: noteRes.status === 'fulfilled' ? noteRes.value.data : [],
          videos: videoRes.status === 'fulfilled' ? videoRes.value.data : [],
          grades: gradesRes.status === 'fulfilled' ? gradesRes.value.data : [],
          notices: noticeRes.status === 'fulfilled' ? noticeRes.value.data : []
        });

      } catch (err) {
        console.error("Dashboard Fetch Error:", err);
        setError("Failed to load some dashboard data. Displaying available information.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-500 font-medium animate-pulse">Loading your academic portal...</p>
        </div>
      </div>
    );
  }

  // Fallback data when endpoints are empty
  const stats = [
    { title: "Attendance", value: data.dashboard?.attendance_percentage || "94%", icon: CalendarCheck, trend: "+2% from last month", trendType: 'positive' },
    { title: "Assignments", value: data.assignments?.length || "5", icon: BookOpen, trend: "3 due this week", trendType: 'neutral' },
    { title: "Upcoming Tests", value: data.tests?.length || "2", icon: FileCheck, trend: "Physics & Math", trendType: 'negative' },
    { title: "Grade Avg", value: data.dashboard?.grade_average || "A-", icon: TrendingUp, trend: "Top 10% of class", trendType: 'positive' },
  ];

  const getNoticeIcon = (issuer) => {
    switch(issuer?.toLowerCase()) {
      case 'authority': return <Shield className="w-4 h-4 text-rose-500" />;
      case 'teacher': return <BookOpen className="w-4 h-4 text-blue-500" />;
      case 'exam_section': return <FileCheck className="w-4 h-4 text-purple-500" />;
      case 'account_section': return <Receipt className="w-4 h-4 text-emerald-500" />;
      case 'library': return <Library className="w-4 h-4 text-amber-500" />;
      default: return <Bell className="w-4 h-4 text-slate-500" />;
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: TrendingUp },
    { id: 'academics', label: 'Academics (Tasks & Tests)', icon: FileCheck },
    { id: 'resources', label: 'E-Library & Media', icon: Library },
    { id: 'notices', label: 'Official Notices', icon: Bell },
  ];

  return (
    <motion.div 
      initial={{ opacity: 0 }} animate={{ opacity: 1 }}
      className="p-6 lg:p-10 space-y-8 bg-slate-50 min-h-screen font-sans"
    >
      {/* Header Profile Section */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2.5 bg-brand-100 rounded-2xl">
              <GraduationCap className="w-7 h-7 text-brand-600" />
            </div>
            <ModernBadge variant="primary" className="uppercase tracking-widest text-[10px]">Student Portal</ModernBadge>
          </div>
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
            Hi, <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 to-indigo-600">
              {data.dashboard?.full_name || storedUser.full_name || 'Student'}
            </span>
          </h1>
          <p className="text-slate-500 font-medium mt-1">ID: {data.dashboard?.student_id_value || 'ST-2026-001'} • Grade {data.dashboard?.grade_level || '10'} {data.dashboard?.section || 'A'}</p>
        </div>

        <div className="flex items-center gap-3">
          <Link to="/student/profile" className="px-5 py-2.5 rounded-xl bg-white border border-slate-200 text-slate-700 font-bold hover:bg-slate-50 transition-colors shadow-sm">
            My Profile
          </Link>
          <button onClick={logout} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-rose-50 text-rose-600 font-bold hover:bg-rose-100 transition-colors">
            <LogOut className="w-4 h-4" /> Sign Out
          </button>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <ModernStatCard key={i} {...stat} />
        ))}
      </section>

      {/* Custom Tabs */}
      <div className="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-6 py-3 rounded-full font-bold text-sm transition-all whitespace-nowrap ${
              activeTab === tab.id 
                ? 'bg-brand-600 text-white shadow-md shadow-brand-500/30' 
                : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
            }`}
          >
            <tab.icon className="w-4 h-4" /> {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-8">
                <GlassCard title="Today's Timetable" icon={Clock} action={<Link to="/student/timetable" className="text-brand-600 text-sm font-bold hover:underline">Full Schedule</Link>}>
                  <div className="space-y-4">
                    {(data.dashboard?.today_timetable || [
                      { time: '09:00 AM', subject: 'Advanced Mathematics', room: 'Room 302', type: 'Lecture', status: 'upcoming' },
                      { time: '11:30 AM', subject: 'Computer Science', room: 'Lab 1', type: 'Practical', status: 'current' },
                    ]).map((slot, i) => (
                      <div key={i} className={`flex items-center justify-between p-4 rounded-xl border transition-all ${slot.status === 'current' ? 'bg-brand-50 border-brand-200 shadow-sm' : 'bg-white border-slate-100'}`}>
                        <div className="flex items-center gap-4">
                          <div className="text-center min-w-[70px]">
                            <p className="text-sm font-black text-slate-800">{slot.time.split(' ')[0]}</p>
                            <p className="text-[10px] font-bold text-slate-500">{slot.time.split(' ')[1]}</p>
                          </div>
                          <div className="w-px h-10 bg-slate-200"></div>
                          <div>
                            <h4 className="font-bold text-slate-800">{slot.subject}</h4>
                            <p className="text-xs text-slate-500 font-medium">{slot.room} • {slot.type}</p>
                          </div>
                        </div>
                        {slot.status === 'current' ? <ModernBadge variant="primary" size="sm">In Session</ModernBadge> : <ChevronRight className="w-4 h-4 text-slate-300" />}
                      </div>
                    ))}
                  </div>
                </GlassCard>

                <GlassCard title="Recent Grades (Report)" icon={Award} action={<Link to="/student/grades" className="text-brand-600 text-sm font-bold hover:underline">Full Report</Link>}>
                  <div className="grid sm:grid-cols-3 gap-4">
                    {(data.grades?.slice(0, 3) || [
                      { subject: 'Physics', grade: 'A', score: '92/100', status: 'Excellent' },
                      { subject: 'Mathematics', grade: 'B+', score: '85/100', status: 'Good' },
                      { subject: 'Literature', grade: 'A-', score: '89/100', status: 'Very Good' }
                    ]).map((g, i) => (
                      <div key={i} className="p-5 rounded-2xl bg-white border border-slate-100 shadow-sm text-center">
                        <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">{g.subject}</h4>
                        <p className="text-4xl font-black text-slate-800 mb-1">{g.grade}</p>
                        <p className="text-sm text-brand-600 font-bold">{g.score}</p>
                      </div>
                    ))}
                  </div>
                </GlassCard>
              </div>
              <div className="space-y-8">
                <GlassCard title="Urgent Notices" icon={Bell} className="bg-gradient-to-br from-indigo-900 to-slate-900 text-white border-0">
                  <div className="space-y-4">
                    {(data.notices?.slice(0,3) || [
                      { title: 'Winter Vacation', issuer: 'Authority', time: '2h ago', urgent: true },
                      { title: 'Library Fine Update', issuer: 'Library', time: '1d ago', urgent: false }
                    ]).map((notice, i) => (
                      <div key={i} className="p-4 bg-white/10 rounded-xl backdrop-blur-md border border-white/10 relative overflow-hidden">
                        <div className="flex justify-between items-start mb-2">
                          <span className="flex items-center gap-1.5 text-xs font-bold text-white/80 bg-white/5 py-1 px-2 rounded-md">
                            {getNoticeIcon(notice.issuer)} {notice.issuer}
                          </span>
                          {notice.urgent && <ModernBadge variant="danger" className="text-[9px]">URGENT</ModernBadge>}
                        </div>
                        <h4 className="font-bold text-sm text-white">{notice.title}</h4>
                      </div>
                    ))}
                    <Link to="/student/notices" className="block text-center text-xs font-bold text-white/70 hover:text-white pt-2">View all official notices &rarr;</Link>
                  </div>
                </GlassCard>
              </div>
            </div>
          )}

          {activeTab === 'academics' && (
            <div className="grid md:grid-cols-2 gap-8">
              <GlassCard title="Pending Assignments" icon={BookOpen}>
                <div className="space-y-3">
                  {(data.assignments?.length > 0 ? data.assignments : [
                    { title: 'Calculus Problem Set #4', course: 'Mathematics', due: 'Tomorrow', priority: 'high' },
                    { title: 'Database Normalization', course: 'CompSci', due: 'Oct 15', priority: 'medium' },
                  ]).map((task, i) => (
                    <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white border border-slate-100 shadow-sm">
                      <div className="flex items-center gap-3">
                        <div className={`w-2.5 h-2.5 rounded-full ${task.priority === 'high' ? 'bg-rose-500 animate-pulse' : 'bg-amber-500'}`}></div>
                        <div>
                          <h4 className="text-sm font-bold text-slate-800">{task.title}</h4>
                          <p className="text-[10px] text-slate-500 font-bold uppercase">{task.course}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-xs font-black text-slate-700">{task.due}</p>
                        <button className="text-[10px] font-bold text-brand-600 uppercase hover:underline">Submit</button>
                      </div>
                    </div>
                  ))}
                </div>
              </GlassCard>

              <GlassCard title="Upcoming Tests & Quizzes" icon={FileCheck}>
                <div className="space-y-3">
                  {(data.tests?.length > 0 ? data.tests : [
                    { title: 'Midterm Physics', date: 'Oct 20, 10:00 AM', duration: '2 Hours', room: 'Hall A' },
                    { title: 'Literature Quiz', date: 'Oct 22, 11:30 AM', duration: '45 Mins', room: 'Online' },
                  ]).map((test, i) => (
                    <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-indigo-50 border border-indigo-100">
                      <div>
                        <h4 className="text-sm font-bold text-indigo-900">{test.title}</h4>
                        <p className="text-[11px] text-indigo-600 font-semibold">{test.date} • {test.duration}</p>
                      </div>
                      <ModernBadge variant="primary" className="bg-indigo-200 text-indigo-800">{test.room}</ModernBadge>
                    </div>
                  ))}
                </div>
              </GlassCard>
            </div>
          )}

          {activeTab === 'resources' && (
            <div className="grid md:grid-cols-3 gap-8">
              <GlassCard title="Study Notes" icon={FileText} className="md:col-span-2">
                <div className="grid sm:grid-cols-2 gap-4">
                  {(data.notes?.length > 0 ? data.notes : [
                    { title: 'Chapter 4: Thermodynamics', subject: 'Physics', author: 'Dr. Smith' },
                    { title: 'Machine Learning Basics', subject: 'CompSci', author: 'Prof. Alan' },
                    { title: 'Poetry Analysis Guide', subject: 'Literature', author: 'Mrs. Jane' },
                  ]).map((note, i) => (
                    <div key={i} className="p-4 rounded-xl bg-white border border-slate-100 shadow-sm hover:shadow-md transition-all cursor-pointer group">
                      <div className="w-10 h-10 rounded-lg bg-orange-100 text-orange-600 flex items-center justify-center mb-3">
                        <FileText className="w-5 h-5" />
                      </div>
                      <h4 className="font-bold text-slate-800 text-sm mb-1 line-clamp-1">{note.title}</h4>
                      <p className="text-xs text-slate-500">{note.subject} • {note.author}</p>
                    </div>
                  ))}
                </div>
              </GlassCard>
              
              <div className="space-y-8">
                <GlassCard title="Video Lectures" icon={Video}>
                  <div className="space-y-4">
                    {(data.videos?.slice(0,2) || [
                      { title: 'Integration by Parts', duration: '45:20' },
                      { title: 'Cell Structure', duration: '32:15' }
                    ]).map((vid, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 cursor-pointer">
                        <div className="w-16 h-12 bg-slate-800 rounded-lg flex items-center justify-center text-white relative">
                          <Video className="w-4 h-4 opacity-50" />
                          <span className="absolute bottom-1 right-1 text-[8px] bg-black/60 px-1 rounded">{vid.duration}</span>
                        </div>
                        <h4 className="text-xs font-bold text-slate-800 line-clamp-2">{vid.title}</h4>
                      </div>
                    ))}
                    <button className="w-full py-2 text-xs font-bold text-brand-600 border border-brand-200 rounded-lg hover:bg-brand-50">View Video Library</button>
                  </div>
                </GlassCard>
                
                <GlassCard title="Library Access" icon={Library} className="bg-emerald-50 border-emerald-100">
                  <p className="text-sm text-emerald-800 font-medium mb-4">You have 2 books issued.</p>
                  <button className="w-full py-2.5 bg-emerald-600 text-white text-sm font-bold rounded-xl shadow-md shadow-emerald-600/20 hover:bg-emerald-700">Go to Library Portal</button>
                </GlassCard>
              </div>
            </div>
          )}

          {activeTab === 'notices' && (
            <GlassCard title="Official Communications" icon={Bell}>
               <div className="grid md:grid-cols-2 gap-6">
                {(data.notices?.length > 0 ? data.notices : [
                  { title: 'Final Exam Schedule Posted', issuer: 'Exam Section', date: 'Oct 12', content: 'The final timetable is now available. Please check the portal.' },
                  { title: 'Fee Deadline Reminder', issuer: 'Account Section', date: 'Oct 10', content: 'Ensure all dues are cleared before midterms.' },
                  { title: 'Science Fair Requirements', issuer: 'Teacher', date: 'Oct 09', content: 'Submit your project abstracts by Friday.' },
                  { title: 'Campus Security Update', issuer: 'Authority', date: 'Oct 08', content: 'New ID cards to be issued next week.' },
                ]).map((notice, i) => (
                  <div key={i} className="p-5 rounded-2xl bg-white border border-slate-100 shadow-sm flex flex-col">
                    <div className="flex justify-between items-start mb-3">
                      <span className="flex items-center gap-1.5 text-xs font-bold text-slate-600 bg-slate-100 py-1.5 px-3 rounded-lg">
                        {getNoticeIcon(notice.issuer)} {notice.issuer.replace('_', ' ').toUpperCase()}
                      </span>
                      <span className="text-xs font-bold text-slate-400">{notice.date}</span>
                    </div>
                    <h4 className="font-bold text-slate-800 mb-2">{notice.title}</h4>
                    <p className="text-sm text-slate-600 leading-relaxed flex-grow">{notice.content}</p>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Error Toast */}
      {error && (
        <div className="fixed bottom-10 right-10 bg-rose-500 text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 animate-slideUp z-50">
          <AlertCircle className="w-6 h-6" />
          <p className="font-bold">{error}</p>
          <button onClick={() => setError(null)} className="ml-4 opacity-70 hover:opacity-100">&times;</button>
        </div>
      )}
    </motion.div>
  );
}
