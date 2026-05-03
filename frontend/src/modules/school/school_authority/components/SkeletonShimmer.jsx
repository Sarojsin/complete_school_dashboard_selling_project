// =====================
// SKELETON SHIMMER - Authority Module
// =====================

import { motion } from 'framer-motion';

// Shimmer effect base
const shimmerBase = "relative overflow-hidden bg-white/5";
const shimmerOverlay = "absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/10 to-transparent";

// Dashboard Skeleton
export const AuthorityDashboardSkeleton = () => (
  <div className="space-y-6">
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl p-8">
      <div className="shimmer-skeleton h-10 w-64 mb-2" />
      <div className="shimmer-skeleton h-5 w-48" />
    </motion.div>
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[...Array(4)].map((_, i) => (
        <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
          className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
          <div className="shimmer-skeleton h-4 w-24 mb-4" />
          <div className="shimmer-skeleton h-8 w-16" />
        </motion.div>
      ))}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {[...Array(2)].map((_, i) => (
        <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 + i * 0.1 }}
          className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
          <div className="shimmer-skeleton h-6 w-32 mb-4" />
          <div className="space-y-3">
            {[...Array(5)].map((_, j) => (
              <div key={j} className="shimmer-skeleton h-12 w-full rounded-lg" />
            ))}
          </div>
        </motion.div>
      ))}
    </div>
  </div>
);

// Data Table Skeleton
export const DataTableSkeleton = ({ rows = 5, cols = 5 }) => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl overflow-hidden">
    <div className="shimmer-skeleton h-12 w-full border-b border-white/10" />
    {[...Array(rows)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
        className="shimmer-skeleton h-16 w-full border-b border-white/5" />
    ))}
  </div>
);

// Form Skeleton
export const FormSkeleton = ({ fields = 4 }) => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6 space-y-4">
    {[...Array(fields)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.1 }}>
        <div className="shimmer-skeleton h-4 w-24 mb-2" />
        <div className="shimmer-skeleton h-10 w-full rounded-lg" />
      </motion.div>
    ))}
    <div className="shimmer-skeleton h-10 w-32 rounded-lg mt-4" />
  </div>
);

// Stats Card Skeleton
export const StatCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="flex justify-between items-start">
      <div>
        <div className="shimmer-skeleton h-4 w-20 mb-2" />
        <div className="shimmer-skeleton h-8 w-12" />
      </div>
      <div className="shimmer-skeleton h-12 w-12 rounded-xl" />
    </div>
  </div>
);

// List Skeleton
export const ListSkeleton = ({ items = 5 }) => (
  <div className="space-y-3">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
        className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 rounded-xl p-4 flex items-center gap-4">
        <div className="shimmer-skeleton h-10 w-10 rounded-full" />
        <div className="flex-1">
          <div className="shimmer-skeleton h-4 w-32 mb-2" />
          <div className="shimmer-skeleton h-3 w-48" />
        </div>
        <div className="shimmer-skeleton h-8 w-20 rounded-lg" />
      </motion.div>
    ))}
  </div>
);

// Chart Skeleton
export const ChartSkeleton = ({ bars = 6 }) => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="shimmer-skeleton h-6 w-32 mb-6" />
    <div className="flex items-end justify-between gap-2 h-48">
      {[...Array(bars)].map((_, i) => (
        <motion.div key={i} initial={{ height: 0 }} animate={{ height: '60%' }} transition={{ delay: i * 0.1, duration: 0.5 }}
          className="flex-1 shimmer-skeleton rounded-t-lg" />
      ))}
    </div>
  </div>
);

// Detail Skeleton
export const DetailSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6 space-y-6">
    <div className="flex items-center gap-6">
      <div className="shimmer-skeleton h-20 w-20 rounded-full" />
      <div className="space-y-2">
        <div className="shimmer-skeleton h-6 w-48" />
        <div className="shimmer-skeleton h-4 w-32" />
      </div>
    </div>
    <div className="grid grid-cols-2 gap-4">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="space-y-2">
          <div className="shimmer-skeleton h-3 w-20" />
          <div className="shimmer-skeleton h-5 w-32" />
        </div>
      ))}
    </div>
  </div>
);

// Modal Skeleton
export const ModalSkeleton = () => (
  <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
    <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
      className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl p-6 w-full max-w-lg">
      <div className="shimmer-skeleton h-6 w-48 mb-6" />
      <div className="space-y-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="space-y-2">
            <div className="shimmer-skeleton h-4 w-24" />
            <div className="shimmer-skeleton h-10 w-full rounded-lg" />
          </div>
        ))}
      </div>
      <div className="flex justify-end gap-3 mt-6">
        <div className="shimmer-skeleton h-10 w-24 rounded-xl" />
        <div className="shimmer-skeleton h-10 w-32 rounded-xl" />
      </div>
    </motion.div>
  </div>
);

// Student Table Skeleton
export const StudentTableSkeleton = ({ rows = 8 }) => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl overflow-hidden">
    <div className="p-4 border-b border-white/10 flex justify-between items-center">
      <div className="shimmer-skeleton h-8 w-64 rounded-lg" />
      <div className="shimmer-skeleton h-8 w-32 rounded-lg" />
    </div>
    <div className="shimmer-skeleton h-12 w-full border-b border-white/10" />
    {[...Array(rows)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }}
        className="shimmer-skeleton h-16 w-full border-b border-white/5" />
    ))}
  </div>
);

// Fee Card Skeleton
export const FeeCardSkeleton = ({ items = 4 }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
        className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
        <div className="flex justify-between items-start mb-4">
          <div className="shimmer-skeleton h-5 w-32" />
          <div className="shimmer-skeleton h-6 w-20 rounded-full" />
        </div>
        <div className="shimmer-skeleton h-8 w-24 mb-2" />
        <div className="shimmer-skeleton h-4 w-40" />
      </motion.div>
    ))}
  </div>
);

// Notice Card Skeleton
export const NoticeCardSkeleton = ({ items = 3 }) => (
  <div className="space-y-4">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
        className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
        <div className="flex justify-between items-start mb-3">
          <div className="shimmer-skeleton h-5 w-3/4" />
          <div className="shimmer-skeleton h-5 w-16 rounded-full" />
        </div>
        <div className="shimmer-skeleton h-4 w-full mb-2" />
        <div className="shimmer-skeleton h-4 w-2/3" />
        <div className="flex items-center gap-4 mt-4">
          <div className="shimmer-skeleton h-3 w-24" />
          <div className="shimmer-skeleton h-3 w-32" />
        </div>
      </motion.div>
    ))}
  </div>
);

export default {
  AuthorityDashboardSkeleton,
  DataTableSkeleton,
  FormSkeleton,
  StatCardSkeleton,
  ListSkeleton,
  ChartSkeleton,
  DetailSkeleton,
  ModalSkeleton,
  StudentTableSkeleton,
  FeeCardSkeleton,
  NoticeCardSkeleton,
};
