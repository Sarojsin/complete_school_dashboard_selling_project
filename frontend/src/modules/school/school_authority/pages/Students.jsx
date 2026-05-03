import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  Search, 
  Filter, 
  Plus, 
  Download, 
  MoreVertical, 
  ChevronLeft, 
  UserCircle, 
  Mail, 
  BookOpen, 
  ShieldCheck, 
  GraduationCap,
  Calendar,
  CheckCircle2,
  XCircle,
  FileText,
  UserPlus
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getAdminStudents } from '../api/authority';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function StudentsManagement() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedGrade, setSelectedGrade] = useState('all');

  // Mocks for visual presentation
  const mockStudents = [
    { id: 1, student_id: 'STU-2024-001', full_name: 'Amit Kumar', email: 'amit.k@example.com', grade_level: '10th', is_active: true, admission_date: '2023-06-15' },
    { id: 2, student_id: 'STU-2024-002', full_name: 'Sia Varma', email: 'sia.v@example.com', grade_level: '12th', is_active: true, admission_date: '2022-06-10' },
    { id: 3, student_id: 'STU-2024-003', full_name: 'Rohan Singh', email: 'rohan.s@example.com', grade_level: '9th', is_active: false, admission_date: '2024-01-05' },
    { id: 4, student_id: 'STU-2024-004', full_name: 'Priya Das', email: 'priya.d@example.com', grade_level: '11th', is_active: true, admission_date: '2023-07-20' },
  ];

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const res = await getAdminStudents();
      setStudents(res.data?.length ? res.data : mockStudents);
    } catch (err) {
      console.error('Error fetching students:', err);
      setStudents(mockStudents);
    } finally {
      setLoading(false);
    }
  };

  const filteredStudents = students.filter(s => 
    (s.full_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
     s.student_id.toLowerCase().includes(searchTerm.toLowerCase())) &&
    (selectedGrade === 'all' || s.grade_level === selectedGrade)
  );

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !students.length) {
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
            to="/authority/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Dashboard
          </Link>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <Users className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Enrollment Registry</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Student Management</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Institutional oversight of administrative student data and lifecycle."</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex gap-3">
           <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl active:scale-95 flex items-center gap-2">
              <UserPlus className="w-5 h-5" /> Enroll Student
           </button>
           <button className="p-4 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all shadow-sm">
              <Download className="w-5 h-5" />
           </button>
        </motion.div>
      </section>

      {/* Analytics Mini-Row */}
      <motion.section variants={itemVariants} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 text-blue-500 rounded-2xl"><Users className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Total Students</p>
               <span className="text-xl font-black text-slate-900">{students.length}</span>
            </div>
         </div>
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-emerald-50 text-emerald-500 rounded-2xl"><CheckCircle2 className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Active Now</p>
               <span className="text-xl font-black text-slate-900">1,212</span>
            </div>
         </div>
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-amber-50 text-amber-500 rounded-2xl"><GraduationCap className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Graduating</p>
               <span className="text-xl font-black text-slate-900">86</span>
            </div>
         </div>
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-rose-50 text-rose-500 rounded-2xl"><XCircle className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Withdrawn</p>
               <span className="text-xl font-black text-slate-900">14</span>
            </div>
         </div>
      </motion.section>

      {/* Main Table Interface */}
      <motion.div variants={itemVariants}>
         <GlassCard noPadding title="Comprehensive Directory" icon={ShieldCheck}>
            <div className="p-8 border-b border-slate-100 flex flex-col lg:flex-row justify-between gap-6">
               <div className="flex-1 relative max-w-xl">
                  <Search className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input 
                     type="text" 
                     placeholder="Search name, ID, or email..." 
                     value={searchTerm}
                     onChange={(e) => setSearchTerm(e.target.value)}
                     className="w-full pl-16 pr-8 py-4 bg-slate-50 border border-slate-100 rounded-3xl text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                  />
               </div>
               
               <div className="flex items-center gap-4">
                  <select 
                    value={selectedGrade}
                    onChange={(e) => setSelectedGrade(e.target.value)}
                    className="pl-6 pr-12 py-4 bg-slate-50 border border-slate-100 rounded-2xl text-[10px] font-black uppercase tracking-widest text-slate-600 outline-none hover:border-brand-500 transition-all appearance-none cursor-pointer"
                  >
                     <option value="all">Every Class</option>
                     <option value="9th">Grade 9</option>
                     <option value="10th">Grade 10</option>
                     <option value="11th">Grade 11</option>
                     <option value="12th">Grade 12</option>
                  </select>
                  <button className="flex items-center gap-3 px-8 py-4 border border-slate-200 rounded-2xl hover:border-brand-200 hover:bg-brand-50 transition-all text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-brand-500">
                     <Filter className="w-4 h-4" /> Comprehensive Filters
                  </button>
               </div>
            </div>

            <div className="overflow-x-auto min-h-[400px]">
               <table className="w-full text-left">
                  <thead>
                     <tr className="bg-slate-50 font-black text-[10px] uppercase tracking-[0.2em] text-slate-400 border-b border-slate-100">
                        <th className="px-10 py-5">Profile & ID</th>
                        <th className="px-10 py-5">Contact Vector</th>
                        <th className="px-10 py-5 text-center">Class Level</th>
                        <th className="px-10 py-5">Lifecycle Status</th>
                        <th className="px-10 py-5 text-right">Administrative</th>
                     </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                     {filteredStudents.map((s) => (
                       <tr key={s.id} className="group hover:bg-slate-50/50 transition-all cursor-pointer">
                          <td className="px-10 py-6">
                             <div className="flex items-center gap-4">
                                <div className="w-12 h-12 bg-slate-100 rounded-[1.25rem] group-hover:bg-white flex items-center justify-center text-slate-400 transition-colors">
                                   <UserCircle className="w-8 h-8" />
                                </div>
                                <div>
                                   <h4 className="text-sm font-black text-slate-900 leading-tight uppercase tracking-tight">{s.full_name}</h4>
                                   <span className="text-[10px] font-bold text-slate-400 uppercase tracking-[0.1em]">{s.student_id}</span>
                                </div>
                             </div>
                          </td>
                          <td className="px-10 py-6">
                             <div className="flex flex-col gap-1">
                                <div className="flex items-center gap-2 text-xs font-bold text-slate-600">
                                   <Mail className="w-3.5 h-3.5 text-slate-300" /> {s.email}
                                </div>
                                <div className="flex items-center gap-2 text-[10px] font-bold text-slate-400 uppercase">
                                   <Calendar className="w-3.5 h-3.5" /> Enrolled: {new Date(s.admission_date).toLocaleDateString()}
                                </div>
                             </div>
                          </td>
                          <td className="px-10 py-6 text-center">
                             <span className="px-4 py-2 bg-slate-100 rounded-xl text-[10px] font-black text-slate-700 uppercase tracking-widest">{s.grade_level}</span>
                          </td>
                          <td className="px-10 py-6">
                             <ModernBadge variant={s.is_active ? 'success' : 'danger'} size="sm">
                                {s.is_active ? 'Active' : 'Inactive'}
                             </ModernBadge>
                          </td>
                          <td className="px-10 py-6 text-right">
                             <div className="flex items-center justify-end gap-2">
                                <Link to={`/authority/students/${s.id}`} className="px-6 py-2 border border-slate-200 rounded-xl text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-brand-500 hover:border-brand-500 transition-all">
                                   Edit Profile
                                </Link>
                                <button className="p-2.5 text-slate-300 hover:text-slate-900 transition-colors"><MoreVertical className="w-5 h-5" /></button>
                             </div>
                          </td>
                       </tr>
                     ))}
                  </tbody>
               </table>
               
               {!filteredStudents.length && (
                  <div className="flex flex-col items-center justify-center p-20 text-center opacity-50">
                     <Users className="w-16 h-16 text-slate-200 mb-4" />
                     <h3 className="text-xl font-black text-slate-900 uppercase">No Matches Found</h3>
                     <p className="text-xs text-slate-400 font-bold uppercase mt-2 tracking-widest">Adjust search criteria for results.</p>
                  </div>
               )}
            </div>

            <div className="px-10 py-6 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
               <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Displaying 1-{filteredStudents.length} of {students.length} Entries</span>
               <div className="flex gap-2">
                  <button className="px-6 py-2 bg-white border border-slate-200 rounded-xl text-[10px] font-black uppercase text-slate-400 disabled:opacity-30" disabled>Previous</button>
                  <button className="px-6 py-2 bg-white border border-slate-200 rounded-xl text-[10px] font-black uppercase text-slate-400">Next Page</button>
               </div>
            </div>
         </GlassCard>
      </motion.div>
    </motion.div>
  );
}

// Utility
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}
