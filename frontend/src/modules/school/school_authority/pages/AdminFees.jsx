import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  IndianRupee,
  ChevronLeft,
  Download,
  Search,
  Filter,
  CheckCircle2,
  AlertCircle,
  Clock,
  TrendingUp,
  TrendingDown,
  ShieldCheck,
  MoreVertical,
  ArrowUpRight,
  Building2,
  UserCircle,
  Calendar,
  XCircle,
  BadgeIndianRupee
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getAdminFees } from '../api/authority';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

export default function AdminFees() {
  const [fees, setFees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const mockFees = [
    { id: 1, student_name: 'Amit Kumar', student_id: 'STU-001', fee_type: 'Tuition Fee - Q1', amount: 15000, paid_amount: 15000, due_date: '2024-03-10', status: 'paid', grade: '10th' },
    { id: 2, student_name: 'Sia Varma', student_id: 'STU-002', fee_type: 'Library & Lab', amount: 5000, paid_amount: 0, due_date: '2024-03-31', status: 'pending', grade: '12th' },
    { id: 3, student_name: 'Rohan Singh', student_id: 'STU-003', fee_type: 'Spring Trip', amount: 3500, paid_amount: 1500, due_date: '2024-03-15', status: 'partial', grade: '9th' },
    { id: 4, student_name: 'Priya Das', student_id: 'STU-004', fee_type: 'Tuition Fee - Q1', amount: 15000, paid_amount: 0, due_date: '2024-02-28', status: 'overdue', grade: '11th' },
    { id: 5, student_name: 'Dev Mehta', student_id: 'STU-005', fee_type: 'Tuition Fee - Q1', amount: 15000, paid_amount: 15000, due_date: '2024-03-12', status: 'paid', grade: '10th' },
  ];

  const collectionStats = {
    total_billed: 53500,
    collected: 31500,
    overdue: 15000,
    pending: 7000,
    collection_rate: 59,
  };

  useEffect(() => {
    fetchFees();
  }, []);

  const fetchFees = async () => {
    try {
      setLoading(true);
      const res = await getAdminFees();
      setFees(res.data?.length ? res.data : mockFees);
    } catch {
      setFees(mockFees);
    } finally {
      setLoading(false);
    }
  };

  const filtered = fees.filter(f =>
    (f.student_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      f.student_id.toLowerCase().includes(searchTerm.toLowerCase())) &&
    (statusFilter === 'all' || f.status === statusFilter)
  );

  const statusConfig = {
    paid:    { variant: 'success', icon: CheckCircle2 },
    pending: { variant: 'warning', icon: Clock },
    partial: { variant: 'primary', icon: TrendingUp },
    overdue: { variant: 'danger',  icon: AlertCircle },
  };

  const cvariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.08 } }
  };
  const iv = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } };

  if (loading && !fees.length) {
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
      variants={cvariants}
      className="p-6 lg:p-10 space-y-8"
    >
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={iv}>
          <Link
            to="/authority/dashboard"
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Dashboard
          </Link>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-amber-50 rounded-xl">
              <IndianRupee className="w-6 h-6 text-amber-500" />
            </div>
            <span className="text-sm font-bold text-amber-600 uppercase tracking-widest">Financial Command</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Fee Management</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Institutional oversight of all fee collection and financial ledgers."</p>
        </motion.div>

        <motion.div variants={iv} className="flex gap-3">
          <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl active:scale-95 flex items-center gap-2">
            <Download className="w-5 h-5" /> Export Ledger
          </button>
        </motion.div>
      </section>

      {/* Stats Row */}
      <motion.section variants={iv} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={BadgeIndianRupee} title="Total Billed" value={`₹${(collectionStats.total_billed / 1000).toFixed(0)}K`} trend="Current term" trendType="neutral" />
        <ModernStatCard icon={CheckCircle2} title="Collected" value={`₹${(collectionStats.collected / 1000).toFixed(0)}K`} trend={`${collectionStats.collection_rate}% rate`} trendType="positive" />
        <ModernStatCard icon={AlertCircle} title="Overdue" value={`₹${(collectionStats.overdue / 1000).toFixed(0)}K`} trend="Needs follow-up" trendType="danger" />
        <ModernStatCard icon={Clock} title="Pending" value={`₹${(collectionStats.pending / 1000).toFixed(0)}K`} trend="Upcoming dues" trendType="warning" />
      </motion.section>

      {/* Collection Rate Gauge + Quick Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <motion.div variants={iv}>
          <GlassCard title="Collection Rate" icon={TrendingUp}>
            <div className="flex flex-col items-center gap-8">
              <div className="relative flex items-center justify-center">
                <svg className="w-48 h-48 -rotate-90">
                  <circle cx="96" cy="96" r="80" stroke="currentColor" strokeWidth="20" fill="transparent" className="text-slate-100" />
                  <circle
                    cx="96" cy="96" r="80"
                    stroke="currentColor" strokeWidth="20" fill="transparent"
                    strokeDasharray={502}
                    strokeDashoffset={502 * (1 - collectionStats.collection_rate / 100)}
                    strokeLinecap="round"
                    className="text-amber-500 transition-all duration-1000"
                  />
                </svg>
                <div className="absolute text-center">
                  <span className="text-4xl font-black text-slate-900">{collectionStats.collection_rate}%</span>
                  <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1">Collected</p>
                </div>
              </div>

              <div className="w-full space-y-3">
                {[
                  { label: 'Grade 9', rate: 78, color: 'bg-blue-500' },
                  { label: 'Grade 10', rate: 92, color: 'bg-emerald-500' },
                  { label: 'Grade 11', rate: 55, color: 'bg-amber-500' },
                  { label: 'Grade 12', rate: 40, color: 'bg-rose-500' },
                ].map(g => (
                  <div key={g.label}>
                    <div className="flex justify-between mb-1">
                      <span className="text-[10px] font-black text-slate-700 uppercase tracking-wider">{g.label}</span>
                      <span className="text-[10px] font-black text-slate-400">{g.rate}%</span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${g.rate}%` }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className={`h-full ${g.color} rounded-full`}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </GlassCard>
        </motion.div>

        {/* Main Fee Table */}
        <motion.div variants={iv} className="lg:col-span-2">
          <GlassCard noPadding title="Payment Records" icon={ShieldCheck}>
            {/* Toolbar */}
            <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search student or ID..."
                  value={searchTerm}
                  onChange={e => setSearchTerm(e.target.value)}
                  className="w-full pl-12 pr-6 py-3 bg-slate-50 border border-slate-100 rounded-2xl text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all"
                />
              </div>
              <div className="flex gap-2">
                {['all', 'paid', 'pending', 'overdue'].map(s => (
                  <button
                    key={s}
                    onClick={() => setStatusFilter(s)}
                    className={`px-4 py-3 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all ${
                      statusFilter === s
                        ? 'bg-slate-900 text-white shadow-lg'
                        : 'bg-slate-50 text-slate-400 hover:bg-slate-100'
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="bg-slate-50 text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100">
                    <th className="px-8 py-4">Student</th>
                    <th className="px-8 py-4">Fee Type</th>
                    <th className="px-8 py-4 text-center">Amount</th>
                    <th className="px-8 py-4">Status</th>
                    <th className="px-8 py-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filtered.map(fee => {
                    const cfg = statusConfig[fee.status] || statusConfig.pending;
                    return (
                      <tr key={fee.id} className="group hover:bg-slate-50/50 transition-all">
                        <td className="px-8 py-5">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400">
                              <UserCircle className="w-6 h-6" />
                            </div>
                            <div>
                              <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{fee.student_name}</p>
                              <span className="text-[9px] font-bold text-slate-400 uppercase">{fee.student_id} · {fee.grade}</span>
                            </div>
                          </div>
                        </td>
                        <td className="px-8 py-5">
                          <div>
                            <p className="text-xs font-black text-slate-800 uppercase tracking-tight">{fee.fee_type}</p>
                            <div className="flex items-center gap-1 mt-0.5">
                              <Calendar className="w-3 h-3 text-slate-300" />
                              <span className="text-[9px] text-slate-400 font-bold uppercase">Due {new Date(fee.due_date).toLocaleDateString()}</span>
                            </div>
                          </div>
                        </td>
                        <td className="px-8 py-5 text-center">
                          <span className="text-sm font-black text-slate-900">₹{fee.amount.toLocaleString()}</span>
                          {fee.paid_amount > 0 && fee.paid_amount < fee.amount && (
                            <p className="text-[9px] text-amber-500 font-black uppercase mt-0.5">₹{fee.paid_amount.toLocaleString()} paid</p>
                          )}
                        </td>
                        <td className="px-8 py-5">
                          <ModernBadge variant={cfg.variant} size="sm">{fee.status}</ModernBadge>
                        </td>
                        <td className="px-8 py-5 text-right">
                          {fee.status !== 'paid' ? (
                            <button className="px-5 py-2 bg-brand-500 text-white rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-md group-hover:scale-105">
                              Collect
                            </button>
                          ) : (
                            <button className="p-2 border border-slate-100 text-slate-300 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all">
                              <ArrowUpRight className="w-4 h-4" />
                            </button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {!filtered.length && (
                <div className="flex flex-col items-center justify-center p-16 opacity-40">
                  <IndianRupee className="w-14 h-14 text-slate-200 mb-4" />
                  <h3 className="text-lg font-black text-slate-900 uppercase">No Records</h3>
                </div>
              )}
            </div>
          </GlassCard>
        </motion.div>
      </div>
    </motion.div>
  );
}
