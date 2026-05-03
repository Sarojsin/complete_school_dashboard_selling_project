import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Search, 
  Filter, 
  GraduationCap, 
  Award, 
  Clock, 
  MoreHorizontal,
  ChevronRight,
  User,
  LayoutGrid,
  List as ListIcon
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getStudentCourses } from '../api/students';
import GlassCard from '../../../shared/components/GlassCard';
import ModernStatCard from '../../../shared/components/ModernStatCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    getStudentCourses()
      .then(data => {
        // Handle both mock and real API data structures
        setCourses(Array.isArray(data) ? data : (data.courses || []));
      })
      .catch(err => console.error("Courses Fetch Error:", err))
      .finally(() => setLoading(false));
  }, []);

  const filteredCourses = courses.filter(course => 
    course.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    course.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

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
              <BookOpen className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Academic Hub</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">My Courses</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Explore your learning path and track your progress across all subjects.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search courses..."
              className="pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all w-64 shadow-sm"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex bg-slate-100 p-1 rounded-2xl">
            <button 
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-xl transition-all ${viewMode === 'grid' ? "bg-white shadow-sm text-brand-500" : "text-slate-500 hover:text-slate-700"}`}
            >
              <LayoutGrid className="w-5 h-5" />
            </button>
            <button 
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-xl transition-all ${viewMode === 'list' ? "bg-white shadow-sm text-brand-500" : "text-slate-500 hover:text-slate-700"}`}
            >
              <ListIcon className="w-5 h-5" />
            </button>
          </div>
        </motion.div>
      </section>

      {/* Stats Quick View */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={BookOpen} title="Total Courses" value={courses.length} trend="Active this term" />
        <ModernStatCard icon={Award} title="Credits Earned" value="18" trend="Requirerd: 24" trendType="positive" />
        <ModernStatCard icon={Clock} title="Learning Hours" value="124" trend="+12 this week" trendType="positive" />
        <ModernStatCard icon={GraduationCap} title="Current GPA" value="3.82" trend="Top 5% of class" trendType="positive" />
      </motion.section>

      {/* Courses Grid/List */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-slate-500 font-bold">Synchronizing your curriculum...</p>
        </div>
      ) : filteredCourses.length === 0 ? (
        <div className="text-center py-20 glass-card rounded-3xl">
          <BookOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-slate-800">No courses found</h3>
          <p className="text-slate-500">We couldn't find any courses matching your search.</p>
          <button 
            onClick={() => setSearchQuery('')}
            className="mt-4 px-6 py-2 bg-brand-500 text-white rounded-xl font-bold hover:bg-brand-600 transition-all"
          >
            Clear Search
          </button>
        </div>
      ) : (
        <motion.div 
          variants={itemVariants} 
          className={viewMode === 'grid' ? "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8" : "space-y-4"}
        >
          {filteredCourses.map((course, i) => (
            viewMode === 'grid' ? (
              <GlassCard 
                key={course.id || i}
                className="group relative"
                noPadding
              >
                <div className={`h-24 mesh-gradient relative`}>
                  <div className="absolute top-4 left-6">
                    <ModernBadge variant="primary" className="bg-white/20 text-white border-white/20 backdrop-blur-md">
                      {course.code || 'CS101'}
                    </ModernBadge>
                  </div>
                  <div className="absolute -bottom-6 right-6">
                    <img 
                      src={course.teacher_avatar || `https://ui-avatars.com/api/?name=${course.teacher || 'Teacher'}&background=random`}
                      alt={course.teacher}
                      className="w-12 h-12 rounded-2xl border-4 border-white shadow-xl"
                    />
                  </div>
                </div>
                <div className="p-6 pt-8">
                  <h3 className="text-xl font-black text-slate-900 mb-1 group-hover:text-brand-500 transition-colors uppercase tracking-tight">
                    {course.name}
                  </h3>
                  <div className="flex items-center gap-2 text-slate-500 text-sm font-medium mb-4">
                    <User className="w-4 h-4" />
                    <span>{course.teacher}</span>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-xs font-bold text-slate-400 mb-1 tracking-wider uppercase">
                        <span>Course Progress</span>
                        <span className="text-slate-900">{course.progress || 0}%</span>
                      </div>
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${course.progress || 0}%` }}
                          className="h-full bg-brand-500 rounded-full"
                        ></motion.div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-100">
                      <div>
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Attendance</p>
                        <p className="font-bold text-slate-800">{course.attendance || 0}%</p>
                      </div>
                      <div>
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Tasks Done</p>
                        <p className="font-bold text-slate-800">{course.assignments_completed || 0}/{course.assignments_total || 0}</p>
                      </div>
                    </div>

                    <div className="flex gap-2 pt-2">
                      <Link 
                        to={`/student/courses/${course.id}`}
                        className="flex-1 py-3 bg-brand-500 text-white rounded-xl text-center font-bold text-sm shadow-lg shadow-brand-500/20 hover:bg-brand-600 transition-all hover:-translate-y-1"
                      >
                        Enter Course
                      </Link>
                      <button className="p-3 bg-slate-50 text-slate-400 rounded-xl hover:bg-slate-100 transition-all">
                        <MoreHorizontal className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              </GlassCard>
            ) : (
              <GlassCard key={course.id || i} noPadding className="p-4 group">
                <div className="flex items-center gap-6">
                  <div className="w-16 h-16 mesh-gradient rounded-2xl flex items-center justify-center text-white font-black">
                    {course.code?.substring(0, 2) || 'CS'}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-black text-lg text-slate-900 group-hover:text-brand-500 transition-colors uppercase tracking-tight">
                        {course.name}
                      </h3>
                      <ModernBadge variant="success" size="sm">{course.status || 'Active'}</ModernBadge>
                    </div>
                    <p className="text-sm text-slate-500 font-medium">{course.teacher} • {course.schedule}</p>
                  </div>
                  <div className="hidden lg:block w-48 px-6 border-x border-slate-100">
                    <div className="flex justify-between text-xs font-bold text-slate-400 mb-1">
                      <span>Progress</span>
                      <span className="text-slate-900">{course.progress}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-brand-500" style={{ width: `${course.progress}%` }}></div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 pr-2">
                    <Link 
                      to={`/student/courses/${course.id}`}
                      className="p-3 bg-brand-50 text-brand-600 rounded-xl hover:bg-brand-500 hover:text-white transition-all shadow-sm"
                    >
                      <ChevronRight className="w-5 h-5" />
                    </Link>
                  </div>
                </div>
              </GlassCard>
            )
          ))}
        </motion.div>
      )}

      {/* Course Resources Footer */}
      <motion.section variants={itemVariants} className="pt-8 border-t border-slate-200">
        <h3 className="text-xl font-black text-slate-900 mb-6 uppercase tracking-tight">Central Resources</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/student/notes" className="glass-card p-6 flex items-start gap-4 group hover:-translate-y-1 transition-all">
            <div className="p-3 bg-brand-50 rounded-2xl text-brand-500 group-hover:bg-brand-500 group-hover:text-white transition-all">
              <BookOpen className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-slate-800 mb-1">Digital Library</h4>
              <p className="text-xs text-slate-500 leading-relaxed font-medium">Access over 500+ curated study materials and lecture notes.</p>
            </div>
          </Link>
          <Link to="/student/videos" className="glass-card p-6 flex items-start gap-4 group hover:-translate-y-1 transition-all">
            <div className="p-3 bg-emerald-50 rounded-2xl text-emerald-500 group-hover:bg-emerald-500 group-hover:text-white transition-all">
              <Clock className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-slate-800 mb-1">Video Archive</h4>
              <p className="text-xs text-slate-500 leading-relaxed font-medium">Watch recorded class sessions and supplementary tutorials.</p>
            </div>
          </Link>
          <Link to="/student/forum" className="glass-card p-6 flex items-start gap-4 group hover:-translate-y-1 transition-all">
            <div className="p-3 bg-violet-50 rounded-2xl text-violet-500 group-hover:bg-violet-500 group-hover:text-white transition-all">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-slate-800 mb-1">Collaboration Forum</h4>
              <p className="text-xs text-slate-500 leading-relaxed font-medium">Discuss topics, ask questions, and share insights with peers.</p>
            </div>
          </Link>
        </div>
      </motion.section>
    </motion.div>
  );
}
