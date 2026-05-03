import { motion } from 'framer-motion';

/**
 * SkeletonShimmer - Loading skeleton component with shimmer animation
 * Used for Exam Section module to show loading states
 */
const SkeletonShimmer = ({
  className = '',
  variant = 'rectangular',
  width,
  height,
  count = 1,
}) => {
  const baseClasses = `
    relative overflow-hidden
    bg-gradient-to-r from-white/5 via-white/10 to-white/5
    bg-[length:200%_100%]
  `;

  const variantClasses = {
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
    text: 'rounded h-4',
    card: 'rounded-2xl',
  };

  const variantStyle = variant === 'text' ? { height: height || '1rem', width: width || '100%' } : {};
  const customStyle = { width, height, ...variantStyle };

  return (
    <div className={`${baseClasses} ${variantClasses[variant]} ${className}`} style={customStyle}>
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
        animate={{
          x: ['-100%', '100%'],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
    </div>
  );
};

/**
 * SkeletonTable - Loading skeleton for tables
 */
export const SkeletonTable = ({ rows = 5, cols = 5, showHeader = true }) => {
  return (
    <div className="w-full overflow-hidden rounded-2xl border border-white/10">
      {/* Header */}
      {showHeader && (
        <div className="grid gap-4 p-4 bg-white/5" style={{ gridTemplateColumns: `repeat(${cols}, 1fr)` }}>
          {Array.from({ length: cols }).map((_, i) => (
            <SkeletonShimmer key={`header-${i}`} variant="text" height="1rem" />
          ))}
        </div>
      )}
      
      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div
          key={`row-${rowIndex}`}
          className="grid gap-4 p-4 border-t border-white/5"
          style={{ gridTemplateColumns: `repeat(${cols}, 1fr)` }}
        >
          {Array.from({ length: cols }).map((_, colIndex) => (
            <SkeletonShimmer key={`cell-${rowIndex}-${colIndex}`} variant="text" height="0.875rem" />
          ))}
        </div>
      ))}
    </div>
  );
};

/**
 * SkeletonCard - Loading skeleton for cards
 */
export const SkeletonCard = ({ showFooter = true }) => {
  return (
    <div className="bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex-1">
          <SkeletonShimmer variant="text" width="60%" height="1.25rem" className="mb-2" />
          <div className="flex gap-3">
            <SkeletonShimmer variant="text" width="80px" height="0.875rem" />
            <SkeletonShimmer variant="text" width="80px" height="0.875rem" />
            <SkeletonShimmer variant="text" width="80px" height="0.875rem" />
          </div>
        </div>
        <SkeletonShimmer variant="text" width="70px" height="24px" />
      </div>
      
      {/* Content */}
      <div className="space-y-3 mt-4">
        <SkeletonShimmer variant="text" width="100%" height="0.875rem" />
        <SkeletonShimmer variant="text" width="80%" height="0.875rem" />
        <SkeletonShimmer variant="text" width="90%" height="0.875rem" />
      </div>
      
      {/* Footer */}
      {showFooter && (
        <div className="mt-4 pt-4 border-t border-white/10 flex gap-2">
          <SkeletonShimmer variant="text" width="80px" height="32px" />
          <SkeletonShimmer variant="text" width="80px" height="32px" />
        </div>
      )}
    </div>
  );
};

/**
 * SkeletonStatsGrid - Loading skeleton for stats cards
 */
export const SkeletonStatsGrid = ({ count = 4 }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <SkeletonShimmer variant="text" width="50%" height="0.75rem" className="mb-2" />
              <SkeletonShimmer variant="text" width="80%" height="2rem" className="font-bold" />
              <SkeletonShimmer variant="text" width="40%" height="0.75rem" className="mt-2" />
            </div>
            <SkeletonShimmer variant="circular" width="48px" height="48px" />
          </div>
        </div>
      ))}
    </div>
  );
};

/**
 * SkeletonList - Loading skeleton for lists
 */
export const SkeletonList = ({ count = 5, showAvatar = true }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="flex items-center gap-3 p-4 bg-white/5 rounded-xl"
        >
          {showAvatar && (
            <SkeletonShimmer variant="circular" width="40px" height="40px" />
          )}
          <div className="flex-1">
            <SkeletonShimmer variant="text" width="30%" height="0.875rem" className="mb-1" />
            <SkeletonShimmer variant="text" width="50%" height="0.75rem" />
          </div>
          <SkeletonShimmer variant="text" width="40px" height="24px" />
        </div>
      ))}
    </div>
  );
};

/**
 * SkeletonExamCard - Loading skeleton for exam cards
 */
export const SkeletonExamCard = ({ count = 3 }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6"
        >
          <div className="flex justify-between items-start mb-3">
            <SkeletonShimmer variant="text" width="60%" height="1.25rem" />
            <SkeletonShimmer variant="text" width="70px" height="24px" />
          </div>
          <div className="flex gap-3 mb-4">
            <SkeletonShimmer variant="text" width="60px" height="0.875rem" />
            <SkeletonShimmer variant="text" width="60px" height="0.875rem" />
            <SkeletonShimmer variant="text" width="60px" height="0.875rem" />
          </div>
          <div className="flex gap-2">
            <SkeletonShimmer variant="text" width="70px" height="32px" />
            <SkeletonShimmer variant="text" width="70px" height="32px" />
          </div>
        </div>
      ))}
    </div>
  );
};

/**
 * SkeletonGradeChart - Loading skeleton for grade distribution chart
 */
export const SkeletonGradeChart = () => {
  const grades = ['A', 'B', 'C', 'D', 'F'];
  
  return (
    <div className="bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
      <SkeletonShimmer variant="text" width="40%" height="1.25rem" className="mb-4" />
      <div className="flex items-end gap-3 h-40">
        {grades.map((grade) => (
          <div key={grade} className="flex-1 flex flex-col items-center">
            <SkeletonShimmer variant="rectangular" width="100%" height="60%" className="rounded-t-lg" />
            <SkeletonShimmer variant="text" width="50%" height="0.75rem" className="mt-2" />
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * SkeletonResultCard - Loading skeleton for result cards
 */
export const SkeletonResultCard = ({ count = 3 }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-4"
        >
          <div className="flex items-center justify-between">
            <div>
              <SkeletonShimmer variant="text" width="120px" height="1rem" className="mb-1" />
              <SkeletonShimmer variant="text" width="180px" height="0.875rem" />
              <SkeletonShimmer variant="text" width="100px" height="0.75rem" className="mt-1" />
            </div>
            <div className="flex items-center gap-3">
              <SkeletonShimmer variant="text" width="40px" height="28px" />
              <SkeletonShimmer variant="text" width="60px" height="20px" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

/**
 * SkeletonDashboard - Full dashboard loading skeleton
 */
export const SkeletonDashboard = () => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <SkeletonStatsGrid count={4} />
      
      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SkeletonExamCard count={3} />
        <SkeletonGradeChart />
      </div>
    </div>
  );
};

/**
 * SkeletonNoticeCard - Loading skeleton for notice cards
 */
export const SkeletonNoticeCard = ({ count = 3 }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-4"
        >
          <div className="flex justify-between items-start mb-2">
            <SkeletonShimmer variant="text" width="60%" height="1rem" />
            <SkeletonShimmer variant="text" width="80px" height="20px" />
          </div>
          <SkeletonShimmer variant="text" width="100%" height="0.875rem" className="mb-1" />
          <SkeletonShimmer variant="text" width="80%" height="0.875rem" />
        </div>
      ))}
    </div>
  );
};

export default SkeletonShimmer;
