import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Award, 
  BookOpen, 
  Trophy, 
  ChevronRight, 
  PieChart, 
  History,
  CheckCircle2,
  Clock,
  ArrowUpRight
} from 'lucide-react';
import { getStudentGrades } from '../api/students';
import GlassCard from '../../../shared/components/GlassCard';
import ModernStatCard from '../../../shared/components/ModernStatCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function GradesPage() {
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStudentGrades()
      .then(data => {
        setGrades(Array.isArray(data) ? data : (data.grades || []));
      })
      .catch(err => console.error("Grades Fetch Error:", err))
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

  const gradeDistribution = [
    { grade: 'A', count: 3, percentage: 50, color: 'bg-emerald-500' },
    { grade: 'B', count: 2, percentage: 33, color: 'bg-brand-500' },
    { grade: 'C', count: 1, percentage: 17, color: 'bg-amber-500' },
  ];

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-emerald-600';
    if (score >= 80) return 'text-brand-600';
    if (score >= 70) return 'text-amber-600';
    return 'text-rose-600';
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
              <TrendingUp className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Performance Insights</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Grade Analytics</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Detailed breakdown of your academic results and historical progress.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <button className="px-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold hover:bg-slate-50 transition-all shadow-sm flex items-center gap-2">
            <History className="w-4 h-4" />
            Previous Semesters
          </button>
          <button className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-sm font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 flex items-center gap-2">
            <Award className="w-4 h-4" />
            Download Transcript
          </button>
        </motion.div>
      </section>

      {/* Stats Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={TrendingUp} title="Current GPA" value="3.75" trend="Top 10%" trendType="positive" />
        <ModernStatCard icon={CheckCircle2} title="Completion" value="85%" trend="Credits: 18/24" trendType="positive" />
        <ModernStatCard icon={History} title="Last Term" value="3.60" trend="+0.15 improvement" trendType="positive" />
        <ModernStatCard icon={Trophy} title="World Rank" value="#124" trend="Global percentile" trendType="neutral" />
      </motion.section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Course Grades Table */}
        <div className="lg:col-span-2 space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard title="Course Performance" icon={BookOpen} noPadding>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50/50 border-b border-slate-100">
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Course</th>
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Internal</th>
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Exam</th>
                      <th className="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Result</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {(grades.length > 0 ? grades : [
                      { name: 'Advanced Mathematics', code: 'MATH401', int: 92, ext: 88, total: 90, grade: 'A' },
                      { name: 'Computer Architecture', code: 'CS302', int: 85, ext: 82, total: 84, grade: 'A-' },
                      { name: 'Database Systems', code: 'CS301', int: 78, ext: 75, total: 76, grade: 'B+' },
                      { name: 'English Literature', code: 'ENG102', int: 95, ext: 91, total: 93, grade: 'A' },
                      { name: 'Physics Laboratory', code: 'PHY201', int: 88, ext: 92, total: 90, grade: 'A' },
                    ]).map((row, i) => (
                      <tr key={i} className="group hover:bg-slate-50/50 transition-colors">
                        <td className="px-6 py-4">
                          <h4 className="font-bold text-slate-900 group-hover:text-brand-500 transition-colors">{row.name}</h4>
                          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{row.code}</p>
                        </td>
                        <td className="px-6 py-4 text-center">
                          <span className="text-sm font-bold text-slate-600">{row.int}%</span>
                        </td>
                        <td className="px-6 py-4 text-center">
                          <span className="text-sm font-bold text-slate-600">{row.ext}%</span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex flex-col items-end">
                            <span className={cn("text-lg font-black", getScoreColor(row.total))}>{row.grade}</span>
                            <span className="text-[10px] font-bold text-slate-400 uppercase">{row.total}% OVERALL</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </GlassCard>
            <div className="mt-4 p-4 rounded-2xl bg-brand-50 border border-brand-100 flex items-center gap-3">
              <div className="p-2 bg-white rounded-xl shadow-sm">
                <ArrowUpRight className="w-5 h-5 text-brand-500" />
              </div>
              <p className="text-xs font-bold text-brand-700">
                Performance Note: Your average in STEM subjects has increased by 12% compared to the previous semester.
              </p>
            </div>
          </motion.div>
        </div>

        {/* Distribution & Insights */}
        <div className="space-y-8">
          <motion.div variants={itemVariants}>
            <GlassCard title="Grade Distribution" icon={PieChart}>
              <div className="space-y-6">
                <div className="flex justify-center py-4">
                  <div className="relative w-32 h-32 rounded-full border-8 border-slate-100 flex items-center justify-center">
                    <div className="text-center">
                      <span className="text-2xl font-black text-slate-900 leading-none">A</span>
                      <p className="text-[8px] font-bold text-slate-400 uppercase">Majority</p>
                    </div>
                    {/* Simplified SVG Chart ring logic would go here */}
                  </div>
                </div>
                <div className="space-y-3">
                  {gradeDistribution.map((item, i) => (
                    <div key={i} className="space-y-1">
                      <div className="flex justify-between text-xs font-bold uppercase tracking-wider">
                        <span className="text-slate-500">Grade {item.grade}</span>
                        <span className="text-slate-900">{item.count} Courses</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div className={cn("h-full rounded-full transition-all duration-1000", item.color)} style={{ width: `${item.percentage}%` }}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={itemVariants}>
            <GlassCard title="Academic Goals" icon={Trophy}>
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-100 group hover:shadow-md transition-all">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest">GPA Target</span>
                    <span className="text-xs font-black text-emerald-700">3.85 / 4.0</span>
                  </div>
                  <div className="h-1.5 w-full bg-white/50 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500" style={{ width: '92%' }}></div>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-center gap-3">
                  <div className="w-10 h-10 shrink-0 rounded-xl bg-white shadow-sm flex items-center justify-center">
                    <Award className="w-5 h-5 text-brand-500" />
                  </div>
                  <div>
                    <h5 className="text-xs font-black text-slate-900 uppercase">Honor Roll Eligibility</h5>
                    <p className="text-[10px] text-slate-500 font-medium">Earn 3 more 'A' grades to qualify.</p>
                  </div>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

// Reuse the cn helper
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}
