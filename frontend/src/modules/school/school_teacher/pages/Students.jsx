import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  Search, 
  Filter, 
  Mail, 
  UserCircle, 
  ChevronRight, 
  ExternalLink,
  BookOpen,
  TrendingUp,
  MoreHorizontal,
  X,
  CheckCircle2,
  Phone
} from 'lucide-react';
import { getTeacherCourses, getTeacherStudents, getStudentDetails } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function StudentsPage() {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStudent, setSelectedStudent] = useState(null);

  useEffect(() => {
    getTeacherCourses()
      .then(data => {
        setCourses(data);
        if (data.length > 0) {
          // Default to first course
          handleCourseSelect(data[0].id);
        }
      })
      .catch(err => console.error("Initial Fetch Error:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleCourseSelect = async (courseId) => {
    setSelectedCourse(courseId);
    if (courseId) {
      setLoading(true);
      try {
        const data = await getTeacherStudents(courseId);
        setStudents(data);
      } catch (err) {
        console.error("Students Fetch Error:", err);
      } finally {
        setLoading(false);
      }
    } else {
      setStudents([]);
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

  const filteredStudents = students.filter(s => 
    s.full_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.email.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="p-6 lg:p-10 space-y-8"
    >
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <Users className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Student Roster</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Active Learners</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Manage student performance, enrollment, and contact details.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex flex-col gap-2">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Current Class Filter</label>
          <select 
            onChange={e => handleCourseSelect(e.target.value)} 
            value={selectedCourse}
            className="px-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all shadow-sm min-w-[240px]"
          >
            <option value="">All Active Classes</option>
            {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </motion.div>
      </section>

      {/* Stats Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard icon={Users} title="Total Students" value={students.length} trend="In selected class" trendType="neutral" />
        <ModernStatCard icon={TrendingUp} title="Avg Performance" value="78.5%" trend="↑ 2.1% this week" trendType="positive" />
        <ModernStatCard icon={CheckCircle2} title="Daily Attendance" value="94%" trend="Target: 90%" trendType="positive" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Student List Section */}
        <div className="lg:col-span-3 space-y-6">
          <motion.div variants={itemVariants}>
            <GlassCard noPadding>
              {/* Toolbar */}
              <div className="p-6 border-b border-slate-100 flex flex-col md:flex-row gap-4 items-center justify-between">
                <div className="relative w-full md:w-96">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input 
                    type="text" 
                    placeholder="Search by name or email..." 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-brand-500/20 transition-all text-sm font-medium"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <button className="p-3 bg-white border border-slate-200 rounded-xl text-slate-400 hover:text-brand-500 transition-all"><Filter className="w-4 h-4" /></button>
                  <button className="px-5 py-3 bg-slate-100 text-slate-600 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-slate-200 transition-all">Export CSV</button>
                </div>
              </div>

              {/* Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50/50 border-b border-slate-100">
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Student</th>
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Status</th>
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Performance</th>
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {loading ? (
                      [1,2,3,4].map(i => (
                        <tr key={i} className="animate-pulse">
                          <td colSpan="4" className="px-6 py-4"><div className="h-10 bg-slate-50 rounded-lg w-full" /></td>
                        </tr>
                      ))
                    ) : filteredStudents.length === 0 ? (
                      <tr>
                        <td colSpan="4" className="px-6 py-20 text-center text-slate-400 font-medium">No students found matching your criteria.</td>
                      </tr>
                    ) : (
                      filteredStudents.map((student) => (
                        <tr key={student.id} className="group hover:bg-slate-50/50 transition-colors">
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-xl bg-brand-50 flex items-center justify-center text-brand-600">
                                <UserCircle className="w-6 h-6" />
                              </div>
                              <div>
                                <h4 className="font-bold text-slate-900 group-hover:text-brand-500 transition-colors">{student.full_name}</h4>
                                <p className="text-xs text-slate-500 font-medium">{student.email}</p>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <ModernBadge variant="success" size="sm">Active</ModernBadge>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                              <div className="w-16 h-2 bg-slate-100 rounded-full overflow-hidden">
                                <div className="h-full bg-brand-500" style={{ width: '85%' }} />
                              </div>
                              <span className="text-xs font-bold text-slate-600">85%</span>
                            </div>
                          </td>
                          <td className="px-6 py-4 text-right">
                            <button 
                              onClick={() => setSelectedStudent(student)}
                              className="p-2 border border-slate-200 text-slate-400 hover:text-brand-600 hover:border-brand-600 rounded-xl transition-all shadow-sm"
                            >
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Sidebar Mini-Profile or Course Info */}
        <div className="space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard title="Attendance Summary" icon={CheckCircle2}>
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-amber-50 border border-amber-100 flex items-center gap-3">
                  <div className="shrink-0 pt-1">
                    <TrendingUp className="w-4 h-4 text-amber-500" />
                  </div>
                  <div>
                    <h5 className="text-[10px] font-black text-amber-600 uppercase">Action Required</h5>
                    <p className="text-xs font-bold text-slate-700 mt-1">3 students have missed 2+ classes this week.</p>
                  </div>
                </div>
                <button className="w-full py-4 bg-slate-900 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg shadow-slate-900/20 active:scale-95">
                  Send Warnings
                </button>
              </div>
            </GlassCard>
          </motion.div>

          {/* Quick Contact Form */}
          <motion.div variants={itemVariants}>
            <GlassCard title="Class Announcement" icon={Mail}>
              <div className="space-y-4">
                <textarea 
                  placeholder="Message the entire class..." 
                  className="w-full min-h-[120px] p-4 bg-slate-50 border border-slate-100 rounded-2xl text-sm outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                />
                <button className="w-full py-4 bg-brand-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 active:scale-95">
                  Broadcast Message
                </button>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>

      {/* Student Detail Modal */}
      <AnimatePresence>
        {selectedStudent && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedStudent(null)}
              className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl overflow-hidden"
            >
              <div className="h-24 bg-brand-500 w-full relative">
                <button 
                  onClick={() => setSelectedStudent(null)}
                  className="absolute right-4 top-4 p-2 bg-white/20 hover:bg-white/40 text-white rounded-xl transition-all"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <div className="p-8 -mt-12 space-y-8">
                <div className="flex flex-col md:flex-row gap-6 items-end">
                  <div className="w-24 h-24 rounded-3xl bg-white shadow-xl border-4 border-white flex items-center justify-center text-brand-500">
                    <UserCircle className="w-16 h-16" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-black text-slate-900 leading-none">{selectedStudent.full_name}</h3>
                    <p className="text-sm font-bold text-slate-400 mt-2 uppercase tracking-widest">ID: ST-00{selectedStudent.id}</p>
                  </div>
                  <div className="flex gap-2">
                    <button className="p-3 bg-slate-100 text-slate-600 rounded-2xl hover:bg-slate-200 transition-all"><Mail className="w-5 h-5" /></button>
                    <button className="p-3 bg-slate-100 text-slate-600 rounded-2xl hover:bg-slate-200 transition-all"><Phone className="w-5 h-5" /></button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
                  <div className="space-y-3">
                    <h5 className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Academic Info</h5>
                    <div className="space-y-2">
                      <div className="flex justify-between p-3 bg-slate-50 rounded-xl">
                        <span className="text-xs font-bold text-slate-500">Current GPA</span>
                        <span className="text-xs font-black text-slate-900">3.8 / 4.0</span>
                      </div>
                      <div className="flex justify-between p-3 bg-slate-50 rounded-xl">
                        <span className="text-xs font-bold text-slate-500">Absences</span>
                        <span className="text-xs font-black text-rose-500">02</span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <h5 className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Teacher Remarks</h5>
                    <textarea 
                      placeholder="Add an internal note about this student..."
                      className="w-full min-h-[80px] p-4 bg-slate-50 border border-slate-200 rounded-2xl text-xs font-medium outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-6 border-t border-slate-100">
                  <button onClick={() => setSelectedStudent(null)} className="px-6 py-3 text-sm font-bold text-slate-500 hover:text-slate-700 transition-all">Close</button>
                  <button className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-sm font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 active:scale-95 flex items-center gap-2">
                    View Full Profile <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
