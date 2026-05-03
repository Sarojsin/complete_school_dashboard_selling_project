// =====================
// SKELETON SHIMMER - Library Module
// =====================
import { motion } from 'framer-motion';

export const LibraryDashboardSkeleton = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[...Array(4)].map((_, i) => <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.1 }} className="bg-gradient-to-br from-emerald-800/90 to-teal-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6"><div className="shimmer-skeleton h-4 w-24 mb-4" /><div className="shimmer-skeleton h-8 w-16" /></motion.div>)}
    </div>
  </div>
);

export const BookCardSkeleton = () => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
    <div className="shimmer-skeleton h-32 w-full mb-4 rounded-lg" />
    <div className="shimmer-skeleton h-5 w-3/4 mb-2" />
    <div className="shimmer-skeleton h-4 w-1/2 mb-4" />
    <div className="shimmer-skeleton h-8 w-full rounded-lg" />
  </motion.div>
);

export const LoanTableSkeleton = ({ rows = 5 }) => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl overflow-hidden">
    <div className="shimmer-skeleton h-12 w-full border-b border-white/10" />
    {[...Array(rows)].map((_, i) => <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }} className="shimmer-skeleton h-16 w-full border-b border-white/5" />)}
  </div>
);

export default { LibraryDashboardSkeleton, BookCardSkeleton, LoanTableSkeleton };
