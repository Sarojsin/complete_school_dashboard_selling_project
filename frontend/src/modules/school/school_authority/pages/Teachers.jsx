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
  UserCheck,
  Calendar,
  CheckCircle2,
  XCircle,
  Briefcase,
  Award,
  ArrowUpRight
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getAdminTeachers } from '../api/authority';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';

export default function TeachersManagement() {
  const [teachers, setTeachers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDept, setSelectedDept] = useState('all');

  // Mocks for visual presentation
  const mockTeachers = [
    { id: 1, full_name: 'Dr. Sarah Wilson', email: 'sarah.w@school.edu', department: 'Physics', position: 'Senior Faculty', is_active: true, join_date: '2020-08-12' },
    { id: 2, full_name: 'Prof. James Bond', email: 'james.b@school.edu', department: 'Administration', position: 'Principal', is_active: true, join_date: '2015-01-05' },
    { id: 3, full_name: 'Ms. Emily Blunt', email: 'emily.b@school.edu', department: 'Literature', position: 'Lecturer', is_active: true, join_date: '2022-03-20' },
    { id: 4, full_name: 'Mr. Tony Stark', email: 'tony.s@school.edu', department: 'Engineering', position: 'Guest Faculty', is_active: false, join_date: '2023-11-15' },
  ];

  useEffect(() => {
    fetchTeachers();
  }, []);

  const fetchTeachers = async () => {
    try {
      setLoading(true);
      const res = await getAdminTeachers();
      setTeachers(res.data?.length ? res.data : mockTeachers);
    } catch (err) {
      console.error('Error fetching teachers:', err);
      setTeachers(mockTeachers);
    } finally {
      setLoading(false);
    }
  };

  const filteredTeachers = teachers.filter(t => 
    (t.full_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
     t.department.toLowerCase().includes(searchTerm.toLowerCase())) &&
    (selectedDept === 'all' || t.department === selectedDept)
  );

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !teachers.length) {
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
              <UserCheck className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Faculty Management</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Teaching Staff</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Governance of academic human resources and departmental structures."</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex gap-3">
           <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl active:scale-95 flex items-center gap-2">
              <Plus className="w-5 h-5" /> Recruit Faculty
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
               <p className="text-[10px] font-black text-slate-400 uppercase">Total Faculty</p>
               <span className="text-xl font-black text-slate-900">{teachers.length}</span>
            </div>
         </div>
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-emerald-50 text-emerald-500 rounded-2xl"><Award className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Senior Staff</p>
               <span className="text-xl font-black text-slate-900">12</span>
            </div>
         </div>
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-amber-50 text-amber-500 rounded-2xl"><Briefcase className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Active Tenure</p>
               <span className="text-xl font-black text-slate-900">22</span>
            </div>
         </div>
         <div className="p-6 bg-white border border-slate-100 rounded-[2rem] shadow-sm flex items-center gap-4">
            <div className="p-3 bg-purple-50 text-purple-500 rounded-2xl"><BookOpen className="w-5 h-5" /></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase">Departments</p>
               <span className="text-xl font-black text-slate-900">8</span>
            </div>
         </div>
      </motion.section>

      {/* Main Table Interface */}
      <motion.div variants={itemVariants}>
         <GlassCard noPadding title="Faculty Directory" icon={ShieldCheck}>
            <div className="p-8 border-b border-slate-100 flex flex-col lg:flex-row justify-between gap-6">
               <div className="flex-1 relative max-w-xl">
                  <Search className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input 
                     type="text" 
                     placeholder="Search faculty name or ID..." 
                     value={searchTerm}
                     onChange={(e) => setSearchTerm(e.target.value)}
                     className="w-full pl-16 pr-8 py-4 bg-slate-50 border border-slate-100 rounded-3xl text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                  />
               </div>
               
               <div className="flex items-center gap-4">
                  <select 
                    value={selectedDept}
                    onChange={(e) => setSelectedDept(e.target.value)}
                    className="pl-6 pr-12 py-4 bg-slate-50 border border-slate-100 rounded-2xl text-[10px] font-black uppercase tracking-widest text-slate-600 outline-none hover:border-brand-500 transition-all appearance-none cursor-pointer"
                  >
                     <option value="all">All Departments</option>
                     <option value="Physics">Physics</option>
                     <option value="Administration">Administration</option>
                     <option value="Literature">Literature</option>
                     <option value="Engineering">Engineering</option>
                  </select>
                  <button className="flex items-center gap-3 px-8 py-4 border border-slate-200 rounded-2xl hover:border-brand-200 hover:bg-brand-50 transition-all text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-brand-500">
                     <Filter className="w-4 h-4" /> Filter Staff
                  </button>
               </div>
            </div>

            <div className="overflow-x-auto min-h-[400px]">
               <table className="w-full text-left">
                  <thead>
                     <tr className="bg-slate-50 font-black text-[10px] uppercase tracking-[0.2em] text-slate-400 border-b border-slate-100">
                        <th className="px-10 py-5">Staff Identity</th>
                        <th className="px-10 py-5">Designation</th>
                        <th className="px-10 py-5 text-center">Department</th>
                        <th className="px-10 py-5">Tenure Status</th>
                        <th className="px-10 py-5 text-right">Administrative</th>
                     </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                     {filteredTeachers.map((t) => (
                       <tr key={t.id} className="group hover:bg-slate-50/50 transition-all cursor-pointer">
                          <td className="px-10 py-6">
                             <div className="flex items-center gap-4">
                                <div className="w-12 h-12 bg-slate-100 rounded-[1.25rem] group-hover:bg-white flex items-center justify-center text-slate-400 transition-colors">
                                   <UserCircle className="w-8 h-8" />
                                </div>
                                <div>
                                   <h4 className="text-sm font-black text-slate-900 leading-tight uppercase tracking-tight">{t.full_name}</h4>
                                   <div className="flex items-center gap-2 mt-1">
                                      <Mail className="w-3.5 h-3.5 text-slate-300" />
                                      <span className="text-[10px] font-bold text-slate-400 lowercase">{t.email}</span>
                                   </div>
                                </div>
                             </div>
                          </td>
                          <td className="px-10 py-6">
                             <div className="flex flex-col gap-1">
                                <span className="text-xs font-black text-slate-700 uppercase tracking-tight">{t.position}</span>
                                <span className="text-[10px] font-bold text-slate-400 uppercase italic">Joined: {new Date(t.join_date).toLocaleDateString()}</span>
                             </div>
                          </td>
                          <td className="px-10 py-6 text-center">
                             <ModernBadge variant="primary" size="xs" className="px-3">
                                {t.department}
                             </ModernBadge>
                          </td>
                          <td className="px-10 py-6">
                             <ModernBadge variant={t.is_active ? 'success' : 'danger'} size="sm">
                                {t.is_active ? 'Active Tenure' : 'Suspended'}
                             </ModernBadge>
                          </td>
                          <td className="px-10 py-6 text-right">
                             <div className="flex items-center justify-end gap-2">
                                <Link to={`/authority/teachers/${t.id}`} className="px-6 py-2 border border-slate-200 rounded-xl text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-brand-500 hover:border-brand-500 transition-all">
                                   Manage
                                </Link>
                                <button className="p-2.5 text-slate-300 hover:text-slate-900 transition-colors"><MoreVertical className="w-5 h-5" /></button>
                             </div>
                          </td>
                       </tr>
                     ))}
                  </tbody>
               </table>
               
               {!filteredTeachers.length && (
                  <div className="flex flex-col items-center justify-center p-20 text-center opacity-50">
                     <Users className="w-16 h-16 text-slate-200 mb-4" />
                     <h3 className="text-xl font-black text-slate-900 uppercase">Staff Not Found</h3>
                     <p className="text-xs text-slate-400 font-bold uppercase mt-2 tracking-widest">Adjust departmental filters or search terms.</p>
                  </div>
               )}
            </div>

            <div className="px-10 py-6 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
               <div className="flex items-center gap-4">
                  <button className="flex items-center gap-2 text-[10px] font-black text-brand-500 uppercase tracking-widest hover:underline decoration-2 underline-offset-4">
                     Generate Staff Report <ArrowUpRight className="w-3.5 h-3.5" />
                  </button>
               </div>
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
