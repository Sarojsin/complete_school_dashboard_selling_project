import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BookOpen, BookMarked, Users, AlertCircle,
  UserCircle, ChevronRight, ArrowUpRight, Clock,
  CheckCircle2, Plus, Download, Search, Filter
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getLibraryDashboardStats, getBooks, getBorrowedBooks, getOverdueBooks } from '../api/library';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const mockStats = { total_books: 12500, borrowed_today: 45, overdue: 12, new_arrivals: 28 };
const mockBooks = [
  { id: 1, title: 'Introduction to Quantum Mechanics', author: 'David Griffiths', isbn: '978-1107189638', category: 'Physics', available: 5 },
  { id: 2, title: 'Organic Chemistry', author: 'Paula Bruice', isbn: '978-0134042282', category: 'Chemistry', available: 3 },
  { id: 3, title: 'Data Structures & Algorithms', author: 'Narasimha Karumanchi', isbn: '978-1466568303', category: 'Computer Science', available: 7 },
  { id: 4, title: 'Modern India History', author: 'Bipan Chandra', isbn: '978-8125036864', category: 'History', available: 4 },
];
const mockBorrowed = [
  { id: 1, student_name: 'Amit Singh', book_title: 'Advanced Calculus', issued_on: '2024-03-15', due_on: '2024-04-15' },
  { id: 2, student_name: 'Priya Sharma', book_title: 'Linear Algebra', issued_on: '2024-03-10', due_on: '2024-04-10' },
  { id: 3, student_name: 'Raj Patel', book_title: 'Thermodynamics', issued_on: '2024-03-05', due_on: '2024-04-05' },
];
const mockOverdue = [
  { id: 1, student_name: 'Kiran Das', book_title: 'Waves & Oscillations', days_overdue: 5, fine: 100 },
  { id: 2, student_name: 'Neha Gupta', book_title: 'Number Theory', days_overdue: 3, fine: 60 },
];

export default function LibraryDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');

  const navigationItems = [
    { icon: BookMarked, title: 'Book Inventory', desc: 'Manage library catalog and stock', link: '/college/library/books', color: 'emerald' },
    { icon: Users, title: 'Borrowed Books', desc: 'Track current issues and returns', link: '/college/library/borrowed', color: 'blue' },
    { icon: AlertCircle, title: 'Overdue List', desc: 'Fine calculation and reminders', link: '/college/library/overdue', color: 'red' },
    { icon: Download, title: 'Reports', desc: 'Library usage analytics', link: '/college/library/reports', color: 'purple' },
  ];

  useEffect(() => {
    getLibraryDashboardStats()
      .then(res => setData(res.data))
      .catch(err => { console.error('Library Dashboard Error:', err); setData(null); })
      .finally(() => setLoading(false));
  }, []);

  const stats = {
    total_books: data?.total_books || mockStats.total_books,
    borrowed_today: data?.borrowed_today || mockStats.borrowed_today,
    overdue: data?.overdue || mockStats.overdue,
    new_arrivals: data?.new_arrivals || mockStats.new_arrivals,
  };

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
            <div className="p-2 bg-emerald-50 rounded-xl">
              <BookOpen className="w-6 h-6 text-emerald-500" />
            </div>
            <span className="text-sm font-bold text-emerald-600 uppercase tracking-widest">Central Library</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Library Hub <span className="text-xl font-medium text-slate-400">/ Knowledge Center</span>
          </h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"Gateway to information and scholarly resources."</p>
        </motion.div>

        <motion.div variants={iv} className="flex items-center gap-4 bg-white p-4 rounded-3xl border border-slate-200 shadow-sm">
          <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-500">
            <UserCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-xs font-black text-slate-900 uppercase tracking-tight">{storedUser.full_name || 'Librarian'}</p>
            <ModernBadge variant="success" size="xs" className="mt-1">Verified Staff</ModernBadge>
          </div>
        </motion.div>
      </section>

      {/* KPI Row */}
      <motion.section variants={iv} className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <ModernStatCard icon={BookOpen} title="Total Books" value={stats.total_books.toLocaleString()} trend="In catalog" trendType="neutral" />
        <ModernStatCard icon={CheckCircle2} title="Issued Today" value={stats.borrowed_today} trend="Active loans" trendType="positive" />
        <ModernStatCard icon={AlertCircle} title="Overdue" value={stats.overdue} trend="Attention needed" trendType="danger" />
        <ModernStatCard icon={Plus} title="New Arrivals" value={stats.new_arrivals} trend="This month" trendType="neutral" />
      </motion.section>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Navigation Cards */}
        <motion.div variants={iv} className="lg:col-span-2">
          <div className="mb-6 px-2">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Library Operations</h3>
          </div>
          <div className="grid grid-cols-2 gap-6">
            {navigationItems.map(item => (
              <Link
                key={item.title}
                to={item.link}
                className="group p-8 bg-white border border-slate-100 rounded-[3rem] shadow-sm hover:shadow-2xl hover:shadow-brand-500/10 hover:-translate-y-2 transition-all overflow-hidden relative"
              >
                <div className={cn(
                  "w-14 h-14 rounded-[1.5rem] mb-6 flex items-center justify-center transition-all group-hover:scale-110 group-hover:rotate-6",
                  item.color === 'emerald' ? 'bg-emerald-50 text-emerald-500' :
                  item.color === 'blue' ? 'bg-blue-50 text-blue-500' :
                  item.color === 'red' ? 'bg-rose-50 text-rose-500' : 'bg-purple-50 text-purple-500'
                )}>
                  <item.icon className="w-7 h-7" />
                </div>
                <h4 className="text-xs font-black text-slate-900 uppercase tracking-tight mb-1">{item.title}</h4>
                <p className="text-[10px] text-slate-500 font-medium leading-relaxed italic">{item.desc}</p>
                <div className="absolute top-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity">
                  <ArrowUpRight className="w-5 h-5 text-slate-300" />
                </div>
                <div className="absolute bottom-0 right-0 w-28 h-28 bg-slate-50 rounded-full translate-x-14 translate-y-14 -z-10 group-hover:bg-brand-50 transition-colors" />
              </Link>
            ))}
          </div>
        </motion.div>

        {/* Right column: Recent Activity */}
        <div className="space-y-8">
          <motion.div variants={iv}>
            <GlassCard noPadding title="Recent Borrows" icon={Clock}>
              <div className="divide-y divide-slate-100">
                {mockBorrowed.map(b => (
                  <div key={b.id} className="p-5 flex items-start gap-3 hover:bg-slate-50/50 group">
                    <div className="w-8 h-8 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-500 shrink-0">
                      <BookMarked className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-[10px] font-black text-slate-900 uppercase tracking-tight leading-tight">{b.student_name}</p>
                      <span className="text-[9px] text-slate-400 font-bold uppercase">{b.book_title} · Due: {new Date(b.due_on).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          <motion.div variants={iv}>
            <GlassCard noPadding title="Overdue Alerts" icon={AlertCircle}>
              <div className="p-6">
                {mockOverdue.length === 0 ? (
                  <p className="text-center text-slate-400 text-sm">No overdue books</p>
                ) : (
                  <div className="space-y-4">
                    {mockOverdue.map(o => (
                      <div key={o.id} className="flex items-center justify-between p-4 bg-rose-50 rounded-xl">
                        <div>
                          <p className="text-xs font-black text-slate-900">{o.student_name}</p>
                          <p className="text-[10px] text-slate-500">{o.book_title}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs font-black text-rose-600">₹{o.fine}</p>
                          <p className="text-[9px] text-slate-400">{o.days_overdue} days</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

function cn(...c) { return c.filter(Boolean).join(' '); }


