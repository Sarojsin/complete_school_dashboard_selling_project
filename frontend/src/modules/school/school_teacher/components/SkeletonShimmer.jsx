// =====================
// SKELETON SHIMMER - Teacher Module
// =====================

import { motion } from 'framer-motion';

export const SkeletonShimmer = ({ className = '', variant = 'rectangular' }) => {
  const variants = {
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
    card: 'rounded-2xl',
  };
  return (
    <div className={`bg-gradient-to-r from-white/10 via-white/20 to-white/10 bg-[length:200%_100%] animate-shimmer ${variants[variant]} ${className}`} />
  );
};

// Teacher Dashboard Skeleton
export const TeacherDashboardSkeleton = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[...Array(4)].map((_, i) => (
        <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
          className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
          <SkeletonShimmer className="h-4 w-24 mb-4" />
          <SkeletonShimmer className="h-8 w-16" />
        </motion.div>
      ))}
    </div>
  </div>
);

// Grade Table Skeleton
export const GradeTableSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    {[...Array(5)].map((_, i) => (
      <div key={i} className="flex items-center gap-4 mb-4">
        <SkeletonShimmer className="h-10 w-10 rounded-full" />
        <SkeletonShimmer className="h-5 flex-1" />
        <SkeletonShimmer className="h-5 w-20" />
      </div>
    ))}
  </div>
);

// Attendance Grid Skeleton
export const AttendanceGridSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="grid grid-cols-4 gap-2">
      {[...Array(20)].map((_, i) => (
        <SkeletonShimmer key={i} className="h-12 rounded-lg" />
      ))}
    </div>
  </div>
);

// Course Card Skeleton
export const CourseCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
    <SkeletonShimmer className="h-5 w-3/4 mb-2" />
    <SkeletonShimmer className="h-4 w-1/2 mb-3" />
    <SkeletonShimmer className="h-2 w-full rounded-full" />
  </div>
);

// Assignment Card Skeleton
export const AssignmentCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
    <div className="flex justify-between mb-3">
      <SkeletonShimmer className="h-5 w-1/2" />
      <SkeletonShimmer className="h-6 w-16 rounded-full" />
    </div>
    <SkeletonShimmer className="h-4 w-3/4 mb-2" />
    <SkeletonShimmer className="h-3 w-1/4" />
  </div>
);

export default { SkeletonShimmer, TeacherDashboardSkeleton, GradeTableSkeleton, AttendanceGridSkeleton, CourseCardSkeleton, AssignmentCardSkeleton };
