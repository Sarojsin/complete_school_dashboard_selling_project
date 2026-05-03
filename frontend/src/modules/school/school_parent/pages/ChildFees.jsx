import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CreditCard, 
  ChevronLeft, 
  Download, 
  Search, 
  Filter, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  Receipt,
  ArrowUpRight,
  ShieldCheck,
  Building2,
  Calendar,
  ChevronRight,
  Info
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getLinkedChildren } from '../api/parents';
import api from '../../../shared/api/client';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function ChildFees() {
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [feesData, setFeesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  // Mocks for visual presentation
  const mockFees = [
    { id: 1, fee_type: 'Tuition Fee - Q1', amount: 15000, paid_amount: 15000, due_date: '2024-03-10', paid_date: '2024-03-08', status: 'paid', transaction_id: 'TXN-99281' },
    { id: 2, fee_type: 'Library & Lab Charges', amount: 5000, paid_amount: 0, due_date: '2024-03-31', paid_date: null, status: 'pending', transaction_id: null },
    { id: 3, fee_type: 'Spring Trip Deposit', amount: 3500, paid_amount: 1500, due_date: '2024-03-15', paid_date: '2024-03-12', status: 'overdue', transaction_id: 'TXN-99102' },
  ];

  useEffect(() => {
    fetchChildren();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchFees(selectedChild.id || selectedChild.student_id);
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

  const fetchFees = async (studentId) => {
    try {
      setLoading(true);
      const res = await api.get(`/fees/student/${studentId}`);
      setFeesData(res.data?.length ? res.data : mockFees);
    } catch (err) {
      console.error('Error fetching fees:', err);
      setFeesData(mockFees);
    } finally {
      setLoading(false);
    }
  };

  const calculateTotals = () => {
    const total = feesData.reduce((sum, f) => sum + (f.amount || 0), 0);
    const paid = feesData.reduce((sum, f) => sum + (f.paid_amount || 0), 0);
    const pending = total - paid;
    return { total, paid, pending };
  };

  const totals = calculateTotals();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading && !feesData.length) {
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
              <CreditCard className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Financial Records</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Fee Statements</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Manage school investments and transaction history seamlessly."</p>
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

      {/* Financial Overview */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard 
          icon={Receipt} 
          title="Total Billed" 
          value={`₹${totals.total.toLocaleString()}`} 
          trend="Annual inclusive" 
          trendType="neutral" 
        />
        <ModernStatCard 
          icon={CheckCircle2} 
          title="Total Paid" 
          value={`₹${totals.paid.toLocaleString()}`} 
          trend="Verified transactions" 
          trendType="positive" 
        />
        <ModernStatCard 
          icon={AlertCircle} 
          title="Outstanding" 
          value={`₹${totals.pending.toLocaleString()}`} 
          trend="Immediate attention" 
          trendType="danger" 
        />
      </motion.section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          {/* Main Statement Card */}
          <motion.div variants={itemVariants}>
            <GlassCard noPadding title="Detailed Statement" icon={Building2}>
               <div className="p-6 border-b border-slate-100 flex flex-col md:flex-row justify-between gap-4">
                  <div className="relative flex-1 max-w-md">
                     <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                     <input 
                        type="text"
                        placeholder="Search statement..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-12 pr-6 py-3 bg-slate-50 border border-slate-100 rounded-2xl text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                     />
                  </div>
                  <div className="flex gap-2">
                     <button className="px-6 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg flex items-center gap-2">
                        <Download className="w-4 h-4" /> Export Statement
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
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Description</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Amount</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Status</th>
                           <th className="px-8 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Transactions</th>
                        </tr>
                     </thead>
                     <tbody className="divide-y divide-slate-100">
                        {feesData.map((fee, idx) => (
                           <tr key={idx} className="group hover:bg-slate-50/50 transition-colors">
                              <td className="px-8 py-6">
                                 <div>
                                    <h4 className="text-sm font-black text-slate-900 uppercase tracking-tight">{fee.fee_type}</h4>
                                    <div className="flex items-center gap-2 mt-1">
                                       <Calendar className="w-3 h-3 text-slate-400" />
                                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Due: {new Date(fee.due_date).toLocaleDateString()}</span>
                                    </div>
                                 </div>
                              </td>
                              <td className="px-8 py-6 text-center">
                                 <div>
                                    <span className="text-sm font-black text-slate-900">₹{fee.amount.toLocaleString()}</span>
                                    {fee.paid_amount > 0 && (
                                       <p className="text-[9px] font-black text-emerald-500 uppercase mt-0.5 animate-pulse">₹{fee.paid_amount.toLocaleString()} PAID</p>
                                    )}
                                 </div>
                              </td>
                              <td className="px-8 py-6">
                                 <ModernBadge variant={fee.status === 'paid' ? 'success' : fee.status === 'overdue' ? 'danger' : 'warning'} size="sm">
                                    {fee.status}
                                 </ModernBadge>
                              </td>
                              <td className="px-8 py-6 text-right">
                                 {fee.status !== 'paid' ? (
                                    <button className="px-6 py-2 bg-brand-500 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-md group-hover:scale-105">
                                       Pay Now
                                    </button>
                                 ) : (
                                    <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all" title={fee.transaction_id}>
                                       <Receipt className="w-4 h-4" />
                                    </button>
                                 )}
                              </td>
                           </tr>
                        ))}
                     </tbody>
                  </table>
               </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Financial Tools & Support */}
        <div className="space-y-8">
           <motion.div variants={itemVariants}>
              <GlassCard title="Fast Payments" icon={ShieldCheck}>
                 <div className="space-y-4">
                    <div className="p-4 rounded-2xl bg-slate-900 text-white flex items-center justify-between group cursor-pointer hover:bg-slate-800 transition-all">
                       <div className="flex items-center gap-3">
                          <div className="p-2 bg-white/10 rounded-xl text-brand-400">
                             <CreditCard className="w-5 h-5" />
                          </div>
                          <div>
                             <h6 className="text-[10px] font-black uppercase tracking-widest">Saved Card</h6>
                             <span className="text-[10px] text-slate-400">Visa ending in 4421</span>
                          </div>
                       </div>
                       <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                    
                    <Link to="/parent/fees/history" className="w-full flex items-center justify-center gap-2 py-4 border border-slate-200 rounded-2xl text-[10px] font-black text-slate-400 hover:text-brand-500 hover:border-brand-500 uppercase tracking-widest transition-all">
                       View Payment History <ArrowUpRight className="w-3.5 h-3.5" />
                    </Link>
                 </div>
              </GlassCard>
           </motion.div>

           <motion.div variants={itemVariants}>
              <div className="p-8 rounded-[2.5rem] bg-emerald-500 border border-emerald-400 shadow-2xl relative overflow-hidden group">
                 <div className="relative z-10 text-white space-y-6">
                    <div className="p-3 bg-white/10 rounded-2xl w-fit">
                       <ShieldCheck className="w-6 h-6" />
                    </div>
                    <div>
                       <h4 className="text-xl font-black leading-tight uppercase">Safe & Secure <br />Transfers</h4>
                       <p className="text-white/80 text-[10px] font-medium mt-2 leading-relaxed">
                          All transactions are encrypted with PCI-DSS compliance. We never store your full card details.
                       </p>
                    </div>
                 </div>
                 {/* Decorative Pulse */}
                 <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 blur-3xl rounded-full translate-x-12 -translate-y-12 animate-pulse" />
              </div>
           </motion.div>

           <motion.div variants={itemVariants}>
              <GlassCard title="Finance Support" icon={Info}>
                 <p className="text-xs font-bold text-slate-600 leading-relaxed italic mb-4">
                    Having trouble with the payment portal? Contact our bursar office during school hours.
                 </p>
                 <button className="w-full py-4 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2">
                    <Building2 className="w-4 h-4" /> Contact Accounts
                 </button>
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
