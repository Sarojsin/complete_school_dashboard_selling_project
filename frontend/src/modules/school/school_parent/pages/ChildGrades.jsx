import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  GraduationCap, 
  ChevronLeft, 
  TrendingUp, 
  Award, 
  BookOpen, 
  Download,
  Filter,
  BarChart3,
  LineChart,
  Target,
  ChevronRight,
  Search
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getLinkedChildren, getChildGrades } from '../api/parents';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function ChildGrades() {
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [gradesData, setGradesData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  // Mocks for visual presentation
  const mockGrades = {
    gpa: '3.8',
    percentage: 92,
    rank: '5th',
    semester: 'Spring 2024',
    grades: [
      { subject: 'Advanced Physics', score: 94, total_score: 100, grade: 'A+', semester: '1st', exam_type: 'Final' },
      { subject: 'Pure Mathematics', score: 88, total_score: 100, grade: 'A', semester: '1st', exam_type: 'Final' },
      { subject: 'English Literature', score: 91, total_score: 100, grade: 'A+', semester: '1st', exam_type: 'Final' },
      { subject: 'World History', score: 85, total_score: 100, grade: 'B+', semester: '1st', exam_type: 'Final' },
      { subject: 'Computer Science', score: 98, total_score: 100, grade: 'A+', semester: '1st', exam_type: 'Final' },
    ]
  };

  useEffect(() => {
    fetchChildren();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchGrades(selectedChild.id || selectedChild.student_id);
    }
  }, [selectedChild]);

  const fetchChildren = async () => {
    try {
      const res = await getLinkedChildren();
      const childrenList = res.data?.children || [];
      setChildren(childrenList);
      if (childrenList.length > 0) setSelectedChild(childrenList[0]);
    } catch (err) {
      console.error('Error fetching children:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchGrades = async (studentId) => {
    try {
      setLoading(true);
      const res = await getChildGrades(studentId);
      setGradesData(res.data || mockGrades);
    } catch (err) {
      console.error('Error fetching grades:', err);
      setGradesData(mockGrades);
    } finally {
      setLoading(false);
    }
  };

  const getGradeVariant = (grade) => {
    const g = grade?.toUpperCase();
    if (g?.includes('A')) return 'success';
    if (g?.includes('B')) return 'primary';
    if (g?.includes('C')) return 'warning';
    return 'danger';
  };

  const filteredGrades = gradesData?.grades?.filter(g => 
    g.subject.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !gradesData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
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
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <Link 
            to="/parent/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Back to Dashboard
          </Link>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <GraduationCap className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Academic Records</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Performance metrics</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Excellence is not a skill, it is an attitude."</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex flex-col gap-2 min-w-[240px]">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Viewing Records For</label>
          <select 
            value={selectedChild?.id || ''} 
            onChange={(e) => {
              const child = children.find(c => (c.id || c.student_id) == e.target.value);
              setSelectedChild(child);
            }}
            className="px-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all shadow-sm"
          >
            {children.map((child) => (
              <option key={child.id || child.student_id} value={child.id || child.student_id}>
                {child.full_name || child.student_name}
              </option>
            ))}
          </select>
        </motion.div>
      </section>

      {/* Summary Stats */}
      {gradesData && (
        <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <ModernStatCard icon={Target} title="Current GPA" value={gradesData.gpa || 'N/A'} trend="Top 5% of class" trendType="positive" />
          <ModernStatCard icon={TrendingUp} title="Overall %" value={`${gradesData.percentage || 0}%`} trend="+2% from last term" trendType="positive" />
          <ModernStatCard icon={Award} title="Class Rank" value={gradesData.rank || 'N/A'} trend="Consistent progress" trendType="neutral" />
          <ModernStatCard icon={BookOpen} title="Subjects Credits" value={gradesData.grades?.length || 0} trend="All credits active" trendType="positive" />
        </motion.section>
      )}

      {/* Main Content & Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          {/* Detailed Grades Table */}
          <motion.div variants={itemVariants}>
            <GlassCard noPadding title="Subject wise breakdown" icon={BarChart3}>
               <div className="p-6 border-b border-slate-100 flex flex-col md:flex-row justify-between gap-4">
                  <div className="relative flex-1 max-w-md">
                     <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                     <input 
                        type="text"
                        placeholder="Filter by subject..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-12 pr-6 py-3 bg-slate-50 border border-slate-100 rounded-2xl text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                     />
                  </div>
                  <div className="flex gap-2">
                     <button className="px-6 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg flex items-center gap-2">
                        <Download className="w-4 h-4" /> Export Result
                     </button>
                     <button className="p-3 border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all">
                        <Filter className="w-5 h-5" />
                     </button>
                  </div>
               </div>

               <div className="overflow-x-auto">
                  <table className="w-full text-left">
                     <thead>
                        <tr className="bg-slate-50/50 border-b border-slate-100">
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Subject</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Performance</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Score</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Grade</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Progress</th>
                        </tr>
                     </thead>
                     <tbody className="divide-y divide-slate-100">
                        {filteredGrades?.map((g, idx) => (
                           <tr key={idx} className="group hover:bg-slate-50/50 transition-colors">
                              <td className="px-8 py-6">
                                 <div>
                                    <h4 className="text-sm font-black text-slate-900 uppercase tracking-tight">{g.subject}</h4>
                                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{g.semester} Semester • {g.exam_type}</span>
                                 </div>
                              </td>
                              <td className="px-8 py-6">
                                 <div className="w-32 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                    <div 
                                       className={cn(
                                          "h-full transition-all duration-1000",
                                          g.score >= 90 ? "bg-emerald-500" : g.score >= 80 ? "bg-brand-500" : "bg-amber-500"
                                       )} 
                                       style={{ width: `${g.score}%` }} 
                                    />
                                 </div>
                              </td>
                              <td className="px-8 py-6">
                                 <span className="text-sm font-black text-slate-900">{g.score}<span className="text-slate-400 text-[10px]">/{g.total_score}</span></span>
                              </td>
                              <td className="px-8 py-6">
                                 <ModernBadge variant={getGradeVariant(g.grade)} size="sm">{g.grade}</ModernBadge>
                              </td>
                              <td className="px-8 py-6 text-right">
                                 <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all">
                                    <ChevronRight className="w-4 h-4" />
                                 </button>
                              </td>
                           </tr>
                        ))}
                     </tbody>
                  </table>
               </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Behavioral & Trend Insights */}
        <div className="space-y-8">
           <motion.div variants={itemVariants}>
              <GlassCard title="Learning Curve" icon={LineChart}>
                 <div className="p-4 rounded-3xl bg-slate-900 text-white space-y-6 relative overflow-hidden group">
                    <div className="relative z-10">
                       <div className="flex justify-between items-start mb-4">
                          <h5 className="text-[10px] font-black uppercase tracking-widest text-brand-400">Quarterly Trend</h5>
                          <ModernBadge variant="success" size="xs">+4.2%</ModernBadge>
                       </div>
                       <div className="space-y-4">
                          <div className="flex items-end gap-1 h-24">
                             {[40, 65, 55, 80, 75, 95].map((val, i) => (
                                <div 
                                   key={i} 
                                   className="flex-1 bg-white/10 rounded-t-lg transition-all hover:bg-brand-500/50 cursor-pointer" 
                                   style={{ height: `${val}%` }} 
                                />
                             ))}
                          </div>
                          <p className="text-[10px] text-slate-400 font-medium italic">Performance in STEM subjects has peaked this month. Suggest maintaining focus on literature.</p>
                       </div>
                    </div>
                    {/* Background Detail */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/10 blur-3xl rounded-full translate-x-12 -translate-y-12" />
                 </div>
              </GlassCard>
           </motion.div>

           <motion.div variants={itemVariants}>
              <GlassCard title="Upcoming Benchmarks" icon={Target}>
                 <div className="space-y-4">
                    {[
                       { title: 'Mid-Term Exams', date: 'April 15, 2024', status: 'Upcoming' },
                       { title: 'Project Submission', date: 'April 20, 2024', status: 'Pending' }
                    ].map((item, i) => (
                       <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 hover:border-brand-200 transition-all group">
                          <h6 className="text-xs font-black text-slate-900 tracking-tight uppercase group-hover:text-brand-500 transition-colors">{item.title}</h6>
                          <div className="flex justify-between items-center mt-1">
                             <span className="text-[10px] font-bold text-slate-400 tracking-tight">{item.date}</span>
                             <ModernBadge variant="primary" size="xs">{item.status}</ModernBadge>
                          </div>
                       </div>
                    ))}
                    <button className="w-full py-4 bg-slate-900 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg active:scale-95">
                       Download Schedule
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
