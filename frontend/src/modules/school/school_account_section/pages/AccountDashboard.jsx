import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Wallet, LayoutDashboard, IndianRupee, Receipt,
  AlertCircle, CheckCircle2, Clock, Search, Filter,
  Download, Plus, UserCircle, ChevronRight, ArrowUpRight,
  Send, Pencil, Trash2, TrendingUp
} from 'lucide-react';
import { getProfile, getDashboardStats, getFees, getPayments, getPendingStudents } from '../api/account';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

// ─── Mock data ────────────────────────────────────────────────────────────────
const mockStats = { total_revenue: 4580000, pending_amount: 820000, collected: 3760000, total_students: 1248 };
const mockPayments = [
  { id: 1, student_name: 'Amit Kumar',  fee_type: 'Tuition Q1', amount: 15000, payment_date: '2024-03-28', payment_method: 'UPI' },
  { id: 2, student_name: 'Priya Das',   fee_type: 'Lab Charges', amount: 5000,  payment_date: '2024-03-26', payment_method: 'Bank Transfer' },
  { id: 3, student_name: 'Dev Mehta',   fee_type: 'Tuition Q1', amount: 15000, payment_date: '2024-03-25', payment_method: 'Cash' },
];
const mockPending = [
  { id: 1, name: 'Rohan Singh', class_name: 'Grade 9',  roll_number: 'R-023', pending_amount: 15000, due_date: '2024-03-15' },
  { id: 2, name: 'Sia Varma',   class_name: 'Grade 12', roll_number: 'R-041', pending_amount: 5500,  due_date: '2024-03-31' },
];
const mockFees = [
  { id: 1, name: 'Tuition Fee Q1',     class_name: 'All Grades', amount: 15000, due_date: '2024-03-10', status: 'paid' },
  { id: 2, name: 'Library & Lab',      class_name: 'All Grades', amount: 5000,  due_date: '2024-03-31', status: 'pending' },
  { id: 3, name: 'Annual Maintenance', class_name: 'All Grades', amount: 3000,  due_date: '2024-04-10', status: 'pending' },
];

const statusVariant = { paid: 'success', pending: 'warning', overdue: 'danger', partial: 'primary' };

function cn(...c) { return c.filter(Boolean).join(' '); }
function fmt(n) { return `₹${Number(n).toLocaleString('en-IN')}`; }

const tabs = [
  { id: 'dashboard', label: 'Overview',   icon: LayoutDashboard },
  { id: 'fees',      label: 'Fee Ledger', icon: IndianRupee },
  { id: 'payments',  label: 'Payments',   icon: Receipt },
  { id: 'pending',   label: 'Defaulters', icon: AlertCircle },
];

// ─── Component ────────────────────────────────────────────────────────────────
export default function AccountDashboard() {
  const [activeTab,       setActiveTab]       = useState('dashboard');
  const [stats,           setStats]           = useState(mockStats);
  const [fees,            setFees]            = useState([]);
  const [payments,        setPayments]        = useState([]);
  const [pendingStudents, setPendingStudents] = useState([]);
  const [loading,         setLoading]         = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [sr, fr, pr, dr] = await Promise.allSettled([getDashboardStats(), getFees(), getPayments(), getPendingStudents()]);
        setStats(sr.value?.data || mockStats);
        setFees(fr.value?.data?.length    ? fr.value.data : mockFees);
        setPayments(pr.value?.data?.length ? pr.value.data : mockPayments);
        setPendingStudents(dr.value?.data?.length ? dr.value.data : mockPending);
      } catch { setFees(mockFees); setPayments(mockPayments); setPendingStudents(mockPending); }
      finally  { setLoading(false); }
    }
    load();
  }, []);

  const cv = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.08 } } };
  const iv = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <motion.div initial="hidden" animate="visible" variants={cv} className="p-6 lg:p-10 space-y-8">
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={iv}>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-amber-50 rounded-xl"><Wallet className="w-6 h-6 text-amber-500" /></div>
            <span className="text-sm font-bold text-amber-600 uppercase tracking-widest">Financial Office</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Accounts Section</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Custodians of institutional financial health and fee collection."</p>
        </motion.div>
        <motion.div variants={iv} className="flex gap-2">
          <button className="px-6 py-4 bg-slate-900 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl flex items-center gap-2">
            <Plus className="w-4 h-4" /> Create Fee
          </button>
          <button className="p-4 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl transition-all shadow-sm">
            <Download className="w-5 h-5" />
          </button>
        </motion.div>
      </section>

      {/* Tabs */}
      <motion.div variants={iv} className="flex flex-wrap gap-2 bg-slate-100/60 p-2 rounded-[2rem] w-fit">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={cn(
              "flex items-center gap-2 px-6 py-3 rounded-[1.5rem] text-[10px] font-black uppercase tracking-widest transition-all",
              activeTab === t.id ? "bg-white text-slate-900 shadow-lg" : "text-slate-400 hover:text-slate-700"
            )}
          >
            <t.icon className="w-4 h-4" /> {t.label}
          </button>
        ))}
      </motion.div>

      <AnimatePresence mode="wait">
        {/* ── OVERVIEW ── */}
        {activeTab === 'dashboard' && (
          <motion.div key="dash" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <ModernStatCard icon={IndianRupee} title="Total Revenue"  value={fmt(stats.total_revenue)}  trend="Annual"       trendType="positive" />
              <ModernStatCard icon={CheckCircle2} title="Collected"     value={fmt(stats.collected)}       trend="Fee receipts" trendType="positive" />
              <ModernStatCard icon={Clock}        title="Outstanding"   value={fmt(stats.pending_amount)}  trend="Follow-up"    trendType="danger" />
              <ModernStatCard icon={TrendingUp}   title="Total Students" value={stats.total_students}      trend="Enrolled"     trendType="neutral" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <GlassCard noPadding title="Recent Transactions" icon={Receipt}>
                <div className="divide-y divide-slate-100">
                  {payments.slice(0, 4).map(p => (
                    <div key={p.id} className="p-6 flex items-center justify-between hover:bg-slate-50/50 group cursor-pointer">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-500">
                          <UserCircle className="w-5 h-5" />
                        </div>
                        <div>
                          <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{p.student_name}</p>
                          <p className="text-[10px] text-slate-400 font-bold uppercase">{p.fee_type} · {p.payment_method}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-xs font-black text-emerald-500">{fmt(p.amount)}</p>
                        <p className="text-[9px] text-slate-400 font-bold uppercase">{new Date(p.payment_date).toLocaleDateString()}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </GlassCard>

              <GlassCard noPadding title="Defaulter Alert" icon={AlertCircle}>
                {pendingStudents.length === 0
                  ? <div className="p-16 flex flex-col items-center text-center opacity-40">
                      <CheckCircle2 className="w-14 h-14 text-emerald-300 mb-4" />
                      <h3 className="text-lg font-black text-slate-900 uppercase">All Clear!</h3>
                      <p className="text-[10px] text-slate-400 font-bold uppercase mt-2">No pending dues remaining.</p>
                    </div>
                  : <div className="divide-y divide-slate-100">
                      {pendingStudents.map(s => (
                        <div key={s.id} className="p-6 flex items-center justify-between hover:bg-slate-50/50 group">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-rose-50 rounded-xl flex items-center justify-center text-rose-500">
                              <UserCircle className="w-5 h-5" />
                            </div>
                            <div>
                              <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{s.name}</p>
                              <p className="text-[10px] text-slate-400 font-bold uppercase">{s.class_name} · Roll {s.roll_number}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-xs font-black text-rose-500">{fmt(s.pending_amount)}</p>
                            <p className="text-[9px] text-slate-400 font-bold uppercase">Due {new Date(s.due_date).toLocaleDateString()}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                }
              </GlassCard>
            </div>
          </motion.div>
        )}

        {/* ── FEES ── */}
        {activeTab === 'fees' && (
          <motion.div key="fees" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
            <GlassCard noPadding title="Fee Structures" icon={IndianRupee}>
              <div className="p-6 border-b border-slate-100 flex gap-4">
                <div className="relative flex-1 max-w-sm">
                  <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input type="text" placeholder="Search fees..." className="w-full pl-12 pr-6 py-3 bg-slate-50 border border-slate-100 rounded-2xl text-xs font-bold outline-none focus:ring-2 focus:ring-brand-500 transition-all" />
                </div>
                <button className="p-3 border border-slate-200 text-slate-400 hover:text-brand-500 rounded-2xl"><Filter className="w-5 h-5" /></button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50 text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100">
                      <th className="px-8 py-4">Fee Name</th>
                      <th className="px-8 py-4">Class</th>
                      <th className="px-8 py-4 text-center">Amount</th>
                      <th className="px-8 py-4">Due Date</th>
                      <th className="px-8 py-4">Status</th>
                      <th className="px-8 py-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {fees.map(f => (
                      <tr key={f.id} className="group hover:bg-slate-50/50">
                        <td className="px-8 py-5">
                          <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{f.name}</p>
                        </td>
                        <td className="px-8 py-5">
                          <span className="text-[10px] font-black text-slate-500 uppercase">{f.class_name}</span>
                        </td>
                        <td className="px-8 py-5 text-center">
                          <span className="text-sm font-black text-slate-900">{fmt(f.amount)}</span>
                        </td>
                        <td className="px-8 py-5">
                          <span className="text-[10px] font-black text-slate-600 uppercase">{new Date(f.due_date).toLocaleDateString()}</span>
                        </td>
                        <td className="px-8 py-5">
                          <ModernBadge variant={statusVariant[f.status] || 'neutral'} size="sm">{f.status}</ModernBadge>
                        </td>
                        <td className="px-8 py-5 text-right">
                          <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl"><Pencil className="w-4 h-4" /></button>
                            <button className="p-2 border border-slate-200 text-slate-400 hover:text-rose-500 hover:border-rose-500 rounded-xl"><Trash2 className="w-4 h-4" /></button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* ── PAYMENTS ── */}
        {activeTab === 'payments' && (
          <motion.div key="payments" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
            <GlassCard noPadding title="Payment Ledger" icon={Receipt}>
              <div className="p-6 border-b border-slate-100 flex justify-between gap-4">
                <div className="relative flex-1 max-w-sm">
                  <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input type="text" placeholder="Search student..." className="w-full pl-12 pr-6 py-3 bg-slate-50 border border-slate-100 rounded-2xl text-xs font-bold outline-none focus:ring-2 focus:ring-brand-500 transition-all" />
                </div>
                <button className="px-6 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center gap-2">
                  <Plus className="w-4 h-4" /> Record
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50 text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100">
                      <th className="px-8 py-4">Student</th>
                      <th className="px-8 py-4">Fee Type</th>
                      <th className="px-8 py-4 text-center">Amount</th>
                      <th className="px-8 py-4">Date</th>
                      <th className="px-8 py-4">Method</th>
                      <th className="px-8 py-4 text-right">Receipt</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {payments.map(p => (
                      <tr key={p.id} className="group hover:bg-slate-50/50">
                        <td className="px-8 py-5">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400">
                              <UserCircle className="w-5 h-5" />
                            </div>
                            <p className="text-xs font-black text-slate-900 uppercase">{p.student_name}</p>
                          </div>
                        </td>
                        <td className="px-8 py-5"><span className="text-xs font-bold text-slate-600 uppercase">{p.fee_type}</span></td>
                        <td className="px-8 py-5 text-center"><span className="text-sm font-black text-emerald-500">{fmt(p.amount)}</span></td>
                        <td className="px-8 py-5"><span className="text-[10px] font-bold text-slate-500 uppercase">{new Date(p.payment_date).toLocaleDateString()}</span></td>
                        <td className="px-8 py-5">
                          <ModernBadge variant="primary" size="xs">{p.payment_method}</ModernBadge>
                        </td>
                        <td className="px-8 py-5 text-right">
                          <button className="p-2 border border-slate-200 text-slate-400 hover:text-brand-500 hover:border-brand-500 rounded-xl transition-all opacity-0 group-hover:opacity-100">
                            <ArrowUpRight className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* ── DEFAULTERS ── */}
        {activeTab === 'pending' && (
          <motion.div key="pending" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest">{pendingStudents.length} Students with Outstanding Dues</h3>
              <button className="px-6 py-4 bg-amber-500 text-white rounded-[1.75rem] text-[10px] font-black uppercase tracking-widest hover:bg-amber-600 transition-all shadow-xl flex items-center gap-2">
                <Send className="w-4 h-4" /> Send Bulk Reminder
              </button>
            </div>
            {pendingStudents.length === 0
              ? <div className="p-20 flex flex-col items-center text-center bg-white rounded-[3rem] border border-slate-100 opacity-40">
                  <CheckCircle2 className="w-16 h-16 text-emerald-300 mb-4" />
                  <h3 className="text-xl font-black text-slate-900 uppercase">Zero Defaulters</h3>
                </div>
              : <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {pendingStudents.map(s => (
                    <div key={s.id} className="p-8 bg-white border-2 border-rose-100 rounded-[3rem] shadow-sm hover:shadow-xl transition-all">
                      <div className="flex items-center gap-4 mb-6">
                        <div className="w-12 h-12 bg-rose-50 rounded-2xl flex items-center justify-center text-rose-500">
                          <UserCircle className="w-7 h-7" />
                        </div>
                        <div>
                          <h4 className="text-sm font-black text-slate-900 uppercase tracking-tight">{s.name}</h4>
                          <p className="text-[10px] text-slate-400 font-bold uppercase">{s.class_name} · Roll {s.roll_number}</p>
                        </div>
                      </div>
                      <div className="space-y-3 mb-6 p-4 bg-rose-50 rounded-2xl">
                        <div className="flex justify-between">
                          <span className="text-[10px] font-black text-slate-500 uppercase">Outstanding</span>
                          <span className="text-sm font-black text-rose-600">{fmt(s.pending_amount)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[10px] font-black text-slate-500 uppercase">Due Date</span>
                          <span className="text-[10px] font-black text-rose-500 uppercase">{new Date(s.due_date).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <button className="flex-1 py-3 bg-white border border-slate-200 text-slate-600 rounded-2xl text-[9px] font-black uppercase tracking-widest hover:border-brand-500 hover:text-brand-500 transition-all">Remind</button>
                        <button className="flex-1 py-3 bg-slate-900 text-white rounded-2xl text-[9px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all">Collect</button>
                      </div>
                    </div>
                  ))}
                </div>
            }
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
