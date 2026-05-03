// =====================
// SKELETON SHIMMER COMPONENTS
// For loading states
// =====================

import { motion } from 'framer-motion';

// Base Skeleton Component
export const SkeletonShimmer = ({ className = '', variant = 'rectangular' }) => {
  const variants = {
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
    card: 'rounded-2xl',
  };
  
  return (
    <div 
      className={`bg-gradient-to-r from-white/10 via-white/20 to-white/10 bg-[length:200%_100%] animate-shimmer ${variants[variant]} ${className}`}
      style={{
        animation: 'shimmer 2s infinite linear',
      }}
    />
  );
};

// Animation keyframes are defined in CSS
// Add this to your global CSS:
// @keyframes shimmer {
//   0% { background-position: -200% 0; }
//   100% { background-position: 200% 0; }
// }

// Dashboard Stats Skeleton
export const DashboardStatsSkeleton = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6"
        >
          <SkeletonShimmer className="h-4 w-24 mb-4" />
          <SkeletonShimmer className="h-8 w-16 mb-2" />
          <SkeletonShimmer className="h-3 w-32" />
        </motion.div>
      ))}
    </div>
  );
};

// Grade Card Skeleton
export const GradeCardSkeleton = () => {
  return (
    <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <SkeletonShimmer className="h-5 w-32" />
        <SkeletonShimmer className="h-6 w-16 rounded-full" />
      </div>
      <SkeletonShimmer className="h-2 w-full rounded-full" />
    </div>
  );
};

// Attendance Row Skeleton
export const AttendanceRowSkeleton = () => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-white/10">
      <SkeletonShimmer className="h-5 w-24" />
      <SkeletonShimmer className="h-5 w-16" />
      <SkeletonShimmer className="h-5 w-20 rounded-full" />
    </div>
  );
};

// Assignment Card Skeleton
export const AssignmentCardSkeleton = () => {
  return (
    <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
      <div className="flex justify-between items-start mb-3">
        <SkeletonShimmer className="h-5 w-3/4" />
        <SkeletonShimmer className="h-6 w-16 rounded-full" />
      </div>
      <SkeletonShimmer className="h-4 w-1/2 mb-3" />
      <SkeletonShimmer className="h-3 w-1/3" />
    </div>
  );
};

// Test Card Skeleton
export const TestCardSkeleton = () => {
  return (
    <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
      <div className="flex justify-between items-start mb-3">
        <SkeletonShimmer className="h-5 w-1/2" />
        <SkeletonShimmer className="h-6 w-20 rounded-full" />
      </div>
      <div className="flex gap-4 mb-3">
        <SkeletonShimmer className="h-4 w-24" />
        <SkeletonShimmer className="h-4 w-24" />
      </div>
      <SkeletonShimmer className="h-10 w-full rounded-xl" />
    </div>
  );
};

// Course Card Skeleton
export const CourseCardSkeleton = () => {
  return (
    <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
      <SkeletonShimmer className="h-32 w-full rounded-xl mb-4" />
      <SkeletonShimmer className="h-5 w-3/4 mb-2" />
      <SkeletonShimmer className="h-4 w-1/2 mb-3" />
      <SkeletonShimmer className="h-2 w-full rounded-full" />
    </div>
  );
};

// Table Row Skeleton
export const TableRowSkeleton = () => {
  return (
    <div className="flex items-center gap-4 p-4 border-b border-white/5">
      <SkeletonShimmer className="h-10 w-10 rounded-full" />
      <SkeletonShimmer className="h-4 flex-1" />
      <SkeletonShimmer className="h-4 w-20" />
      <SkeletonShimmer className="h-4 w-16" />
    </div>
  );
};

// Notice Card Skeleton
export const NoticeCardSkeleton = () => {
  return (
    <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
      <div className="flex items-center gap-3 mb-3">
        <SkeletonShimmer className="h-8 w-8 rounded-full" />
        <div className="flex-1">
          <SkeletonShimmer className="h-4 w-32 mb-2" />
          <SkeletonShimmer className="h-3 w-24" />
        </div>
      </div>
      <SkeletonShimmer className="h-4 w-full mb-2" />
      <SkeletonShimmer className="h-4 w-3/4" />
    </div>
  );
};

// Loading Spinner (Alternative to skeleton)
export const LoadingSpinner = ({ size = 'md' }) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };
  
  return (
    <div className={`${sizes[size]} border-2 border-white/20 border-t-primary-500 rounded-full animate-spin`} />
  );
};

// Full Page Loading
export const FullPageLoading = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 flex items-center justify-center">
      <div className="text-center">
        <LoadingSpinner size="lg" />
        <p className="text-white/60 mt-4">Loading...</p>
      </div>
    </div>
  );
};

export default {
  SkeletonShimmer,
  DashboardStatsSkeleton,
  GradeCardSkeleton,
  AttendanceRowSkeleton,
  AssignmentCardSkeleton,
  TestCardSkeleton,
  CourseCardSkeleton,
  TableRowSkeleton,
  NoticeCardSkeleton,
  LoadingSpinner,
  FullPageLoading,
};
