// =====================
// SKELETON SHIMMER - Parent Module
// =====================

import { motion } from 'framer-motion';

// Dashboard Skeleton
export const ParentDashboardSkeleton = () => (
  <div className="space-y-6">
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-gradient-to-br from-amber-800/90 to-orange-900/90 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl p-8">
      <div className="shimmer-skeleton h-10 w-64 mb-2" />
      <div className="shimmer-skeleton h-5 w-48" />
    </motion.div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {[...Array(3)].map((_, i) => (
        <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
          className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
          <div className="flex items-center gap-4">
            <div className="shimmer-skeleton h-14 w-14 rounded-full" />
            <div>
              <div className="shimmer-skeleton h-4 w-24 mb-2" />
              <div className="shimmer-skeleton h-6 w-16" />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {[...Array(2)].map((_, i) => (
        <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 + i * 0.1 }}
          className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
          <div className="shimmer-skeleton h-6 w-32 mb-4" />
          <div className="space-y-3">
            {[...Array(4)].map((_, j) => (
              <div key={j} className="shimmer-skeleton h-12 w-full rounded-lg" />
            ))}
          </div>
        </motion.div>
      ))}
    </div>
  </div>
);

// Child Card Skeleton
export const ChildCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="flex items-center gap-4 mb-4">
      <div className="shimmer-skeleton h-16 w-16 rounded-full" />
      <div>
        <div className="shimmer-skeleton h-5 w-32 mb-2" />
        <div className="shimmer-skeleton h-4 w-24" />
      </div>
    </div>
    <div className="grid grid-cols-3 gap-3">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="shimmer-skeleton h-16 rounded-lg" />
      ))}
    </div>
  </div>
);

// Grade Table Skeleton
export const GradeTableSkeleton = ({ rows = 5 }) => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl overflow-hidden">
    <div className="shimmer-skeleton h-12 w-full border-b border-white/10" />
    {[...Array(rows)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
        className="shimmer-skeleton h-16 w-full border-b border-white/5" />
    ))}
  </div>
);

// Attendance Calendar Skeleton
export const AttendanceCalendarSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="shimmer-skeleton h-6 w-32 mb-4" />
    <div className="grid grid-cols-7 gap-2">
      {[...Array(7)].map((_, i) => (
        <div key={i} className="shimmer-skeleton h-8 w-full rounded" />
      ))}
      {[...Array(28)].map((_, i) => (
        <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.02 }}
          className="shimmer-skeleton h-10 w-full rounded-lg" />
      ))}
    </div>
  </div>
);

// Fee Card Skeleton
export const FeeCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="flex justify-between items-start mb-4">
      <div className="shimmer-skeleton h-5 w-32" />
      <div className="shimmer-skeleton h-6 w-20 rounded-full" />
    </div>
    <div className="shimmer-skeleton h-8 w-24 mb-2" />
    <div className="shimmer-skeleton h-4 w-40" />
    <div className="shimmer-skeleton h-10 w-full mt-4 rounded-lg" />
  </div>
);

// Homework Card Skeleton
export const HomeworkCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="shimmer-skeleton h-5 w-3/4 mb-3" />
    <div className="shimmer-skeleton h-4 w-full mb-2" />
    <div className="shimmer-skeleton h-4 w-2/3 mb-4" />
    <div className="flex items-center gap-4">
      <div className="shimmer-skeleton h-3 w-24" />
      <div className="shimmer-skeleton h-3 w-20" />
    </div>
  </div>
);

// Notice Card Skeleton
export const NoticeCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
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
  </div>
);

// Chat Skeleton
export const ChatSkeleton = () => (
  <div className="flex h-full gap-4">
    <div className="w-1/3 bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
      <div className="shimmer-skeleton h-8 w-full mb-4 rounded-lg" />
      {[...Array(5)].map((_, i) => (
        <div key={i} className="flex items-center gap-3 mb-3">
          <div className="shimmer-skeleton h-10 w-10 rounded-full" />
          <div className="flex-1">
            <div className="shimmer-skeleton h-4 w-20 mb-1" />
            <div className="shimmer-skeleton h-3 w-28" />
          </div>
        </div>
      ))}
    </div>
    <div className="flex-1 bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
      <div className="shimmer-skeleton h-6 w-32 mb-4" />
      <div className="space-y-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className={`flex ${i % 2 === 0 ? 'justify-start' : 'justify-end'}`}>
            <div className={`shimmer-skeleton h-16 w-48 rounded-2xl ${i % 2 === 0 ? 'mr-auto' : 'ml-auto'}`} />
          </div>
        ))}
      </div>
    </div>
  </div>
);

// Performance Chart Skeleton
export const PerformanceChartSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="shimmer-skeleton h-6 w-40 mb-6" />
    <div className="flex items-end justify-between gap-2 h-48">
      {[...Array(6)].map((_, i) => (
        <motion.div key={i} initial={{ height: 0 }} animate={{ height: '60%' }} transition={{ delay: i * 0.1, duration: 0.5 }}
          className="flex-1 shimmer-skeleton rounded-t-lg" />
      ))}
    </div>
  </div>
);

// List Skeleton
export const ParentListSkeleton = ({ items = 5 }) => (
  <div className="space-y-3">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
        className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 rounded-xl p-4 flex items-center gap-4">
        <div className="shimmer-skeleton h-12 w-12 rounded-full" />
        <div className="flex-1">
          <div className="shimmer-skeleton h-4 w-32 mb-2" />
          <div className="shimmer-skeleton h-3 w-48" />
        </div>
        <div className="shimmer-skeleton h-8 w-24 rounded-lg" />
      </motion.div>
    ))}
  </div>
);

export default {
  ParentDashboardSkeleton,
  ChildCardSkeleton,
  GradeTableSkeleton,
  AttendanceCalendarSkeleton,
  FeeCardSkeleton,
  HomeworkCardSkeleton,
  NoticeCardSkeleton,
  ChatSkeleton,
  PerformanceChartSkeleton,
  ParentListSkeleton,
};
