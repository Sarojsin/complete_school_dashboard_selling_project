import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpen, 
  Plus, 
  Users, 
  Calendar, 
  Search, 
  Filter, 
  ChevronRight, 
  MoreVertical,
  Layers,
  GraduationCap,
  X
} from 'lucide-react';
import { getTeacherCourses, createAssignment } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [formData, setFormData] = useState({ 
    title: '', 
    description: '', 
    due_date: '', 
    course_id: '',
    points: 100
  });

  useEffect(() => {
    getTeacherCourses()
      .then(data => setCourses(data))
      .catch(err => console.error("Courses Fetch Error:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createAssignment(formData);
      setShowForm(false);
      // Reset form
      setFormData({ title: '', description: '', due_date: '', course_id: '', points: 100 });
      // In a real app, we might refresh or show a success toast
    } catch (err) {
      console.error("Assignment Creation Error:", err);
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

  const filteredCourses = courses.filter(c => 
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.description?.toLowerCase().includes(searchQuery.toLowerCase())
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
              <Layers className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Academic Catalog</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Class Management</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Coordinate your curriculum, students, and active assignments.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <button 
            onClick={() => setShowForm(true)}
            className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-sm font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 flex items-center gap-2 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            New Assignment
          </button>
        </motion.div>
      </section>

      {/* Search & Filter Bar */}
      <motion.section variants={itemVariants} className="flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search classes by name or ID..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-4 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500/20 transition-all font-medium text-slate-700"
          />
        </div>
        <button className="px-6 py-4 bg-white border border-slate-200 rounded-2xl text-slate-600 font-bold flex items-center gap-2 hover:bg-slate-50 transition-all">
          <Filter className="w-4 h-4" /> Filters
        </button>
      </motion.section>

      {/* Courses Grid */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {loading ? (
          [1,2,3].map(i => <div key={i} className="h-64 bg-slate-100 rounded-3xl animate-pulse" />)
        ) : filteredCourses.length === 0 ? (
          <div className="col-span-full py-20 text-center">
            <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <BookOpen className="w-10 h-10 text-slate-300" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">No classes found</h3>
            <p className="text-slate-500 mt-2">Try adjusting your search or filters.</p>
          </div>
        ) : (
          filteredCourses.map((course) => (
            <motion.div key={course.id} whileHover={{ y: -5 }} transition={{ type: 'spring', stiffness: 300 }}>
              <GlassCard noPadding className="h-full flex flex-col group overflow-hidden border-transparent hover:border-brand-200">
                {/* Visual Accent */}
                <div className="h-3 bg-brand-500 w-full" />
                
                <div className="p-6 flex-1 space-y-4">
                  <div className="flex justify-between items-start">
                    <div className="p-2.5 bg-brand-50 rounded-xl">
                      <GraduationCap className="w-5 h-5 text-brand-500" />
                    </div>
                    <button className="text-slate-400 hover:text-slate-600 transition-colors">
                      <MoreVertical className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <div>
                    <h3 className="text-xl font-bold text-slate-900 group-hover:text-brand-500 transition-colors">{course.name}</h3>
                    <p className="text-sm text-slate-500 font-medium line-clamp-2 mt-2">{course.description || "No description available for this course module."}</p>
                  </div>

                  <div className="flex items-center gap-4 pt-2">
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-slate-400" />
                      <span className="text-xs font-bold text-slate-700 uppercase tracking-widest">{course.student_count || 0} Students</span>
                    </div>
                  </div>
                </div>

                <div className="p-6 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between">
                  <ModernBadge variant="primary" size="sm">Active Quarter</ModernBadge>
                  <button className="text-xs font-black text-brand-500 uppercase tracking-widest flex items-center gap-1 hover:translate-x-1 transition-transform">
                    Enter Class <ChevronRight className="w-3 h-3" />
                  </button>
                </div>
              </GlassCard>
            </motion.div>
          ))
        )}
      </motion.section>

      {/* Create Assignment Modal */}
      <AnimatePresence>
        {showForm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowForm(false)}
              className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl overflow-hidden"
            >
              <div className="p-6 border-b border-slate-100 flex justify-between items-center">
                <h3 className="text-xl font-black text-slate-900 uppercase tracking-tight">Create Assignment</h3>
                <button onClick={() => setShowForm(false)} className="p-2 hover:bg-slate-100 rounded-xl transition-all">
                  <X className="w-5 h-5 text-slate-400" />
                </button>
              </div>
              
              <form onSubmit={handleSubmit} className="p-8 space-y-6">
                <div className="space-y-2">
                  <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Select Target Course</label>
                  <select 
                    className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-bold text-slate-700"
                    value={formData.course_id} 
                    onChange={e => setFormData({...formData, course_id: e.target.value})}
                    required
                  >
                    <option value="">Choose a module...</option>
                    {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Assignment Title</label>
                  <input
                    type="text"
                    placeholder="e.g. Unit 4 Research Paper"
                    className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium"
                    value={formData.title}
                    onChange={e => setFormData({...formData, title: e.target.value})}
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Due Date</label>
                    <input
                      type="date"
                      className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium"
                      value={formData.due_date}
                      onChange={e => setFormData({...formData, due_date: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total Points</label>
                    <input
                      type="number"
                      className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium"
                      value={formData.points}
                      onChange={e => setFormData({...formData, points: e.target.value})}
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Description & Requirements</label>
                  <textarea
                    placeholder="Describe the task and submission format..."
                    className="w-full min-h-[120px] p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium"
                    value={formData.description}
                    onChange={e => setFormData({...formData, description: e.target.value})}
                  />
                </div>

                <button 
                  type="submit" 
                  className="w-full py-4 bg-brand-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 active:scale-95"
                >
                  Publish to Students
                </button>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
