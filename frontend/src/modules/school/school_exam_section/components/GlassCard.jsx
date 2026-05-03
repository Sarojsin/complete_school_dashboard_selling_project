import { motion } from 'framer-motion';

/**
 * GlassCard - A glassmorphism card component for Exam Section module
 * Features:
 * - Gradient backgrounds with backdrop blur
 * - Smooth animations using Framer Motion
 * - Exam-specific status badges and styling
 */
const GlassCard = ({
  children,
  className = '',
  hover = true,
  onClick,
  status,
  padding = 'p-6',
  delay = 0,
}) => {
  const baseClasses = `
    relative overflow-hidden
    bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl
    border border-white/10 rounded-2xl
    transition-all duration-300
  `;

  const hoverClasses = hover ? `
    hover:border-white/20 hover:shadow-xl
    hover:scale-[1.02]
    hover:from-blue-800/30 hover:to-slate-800/30
  ` : '';

  const clickClasses = onClick ? 'cursor-pointer' : '';

  const statusColors = {
    published: 'border-l-4 border-l-emerald-500',
    scheduled: 'border-l-4 border-l-amber-500',
    draft: 'border-l-4 border-l-slate-500',
    active: 'border-l-4 border-l-emerald-500',
    completed: 'border-l-4 border-l-blue-500',
    upcoming: 'border-l-4 border-l-purple-500',
  };

  const statusClass = status ? statusColors[status] || '' : '';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
      whileHover={hover ? { scale: 1.02 } : {}}
      className={`${baseClasses} ${hoverClasses} ${clickClasses} ${statusClass} ${className}`}
      onClick={onClick}
    >
      {/* Glow effect on hover */}
      {hover && (
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-blue-500/5 via-purple-500/5 to-emerald-500/5 opacity-0 hover:opacity-100 transition-opacity duration-300 rounded-2xl" />
      )}
      
      {/* Content */}
      <div className={padding}>
        {children}
      </div>
    </motion.div>
  );
};

/**
 * GlassCardHeader - Header section for GlassCard
 */
export const GlassCardHeader = ({ title, subtitle, action, icon: Icon }) => {
  return (
    <div className="flex items-start justify-between mb-4">
      <div className="flex items-center gap-3">
        {Icon && (
          <div className="p-2 bg-white/5 rounded-xl">
            <Icon className="w-5 h-5 text-blue-400" />
          </div>
        )}
        <div>
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          {subtitle && (
            <p className="text-sm text-white/50">{subtitle}</p>
          )}
        </div>
      </div>
      {action && <div>{action}</div>}
    </div>
  );
};

/**
 * GlassCardContent - Content section for GlassCard
 */
export const GlassCardContent = ({ children, className = '' }) => {
  return <div className={className}>{children}</div>;
};

/**
 * GlassCardFooter - Footer section for GlassCard
 */
export const GlassCardFooter = ({ children, className = '' }) => {
  return (
    <div className={`mt-4 pt-4 border-t border-white/10 ${className}`}>
      {children}
    </div>
  );
};

/**
 * ExamStatusBadge - Status badge for exams
 */
export const ExamStatusBadge = ({ status }) => {
  const statusClasses = {
    published: 'bg-emerald-500/20 text-emerald-400',
    scheduled: 'bg-amber-500/20 text-amber-400',
    draft: 'bg-white/10 text-white/60',
    active: 'bg-emerald-500/20 text-emerald-400',
    completed: 'bg-blue-500/20 text-blue-400',
    upcoming: 'bg-purple-500/20 text-purple-400',
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusClasses[status] || statusClasses.draft}`}>
      {status?.charAt(0).toUpperCase() + status?.slice(1)}
    </span>
  );
};

/**
 * GradeBadge - Grade badge with color coding
 */
export const GradeBadge = ({ grade }) => {
  const gradeClasses = {
    A: 'bg-emerald-500/20 text-emerald-400',
    B: 'bg-blue-500/20 text-blue-400',
    C: 'bg-amber-500/20 text-amber-400',
    D: 'bg-orange-500/20 text-orange-400',
    F: 'bg-red-500/20 text-red-400',
  };

  return (
    <span className={`px-2 py-1 rounded-lg text-sm font-bold ${gradeClasses[grade] || 'bg-white/10 text-white/60'}`}>
      {grade}
    </span>
  );
};

/**
 * ExamCard - Card for displaying exam information
 */
export const ExamCard = ({ exam, onClick, onPublish, onSchedule }) => {
  return (
    <GlassCard status={exam.status} onClick={onClick}>
      <div className="flex justify-between items-start mb-3">
        <h4 className="text-white font-semibold">{exam.title}</h4>
        <ExamStatusBadge status={exam.status} />
      </div>
      
      <div className="flex gap-4 text-white/60 text-sm mb-4">
        <span>📅 {exam.date || exam.examDate}</span>
        <span>⏰ {exam.duration || exam.durationMinutes} min</span>
        <span>📝 {exam.questionsCount || exam.questionCount || 0} questions</span>
      </div>
      
      <GlassCardFooter>
        <div className="flex gap-2">
          {exam.status === 'draft' && onPublish && (
            <button
              onClick={(e) => { e.stopPropagation(); onPublish(exam.id); }}
              className="px-3 py-1.5 text-sm text-emerald-400 hover:text-emerald-300 bg-emerald-500/10 hover:bg-emerald-500/20 rounded-lg transition-colors"
            >
              Publish
            </button>
          )}
          {exam.status === 'draft' && onSchedule && (
            <button
              onClick={(e) => { e.stopPropagation(); onSchedule(exam.id); }}
              className="px-3 py-1.5 text-sm text-blue-400 hover:text-blue-300 bg-blue-500/10 hover:bg-blue-500/20 rounded-lg transition-colors"
            >
              Schedule
            </button>
          )}
        </div>
      </GlassCardFooter>
    </GlassCard>
  );
};

/**
 * ResultCard - Card for displaying exam results
 */
export const ResultCard = ({ result, showStudent = true, showExam = true }) => {
  return (
    <GlassCard status={result.published ? 'published' : 'draft'}>
      <div className="flex items-center justify-between">
        <div>
          {showStudent && (
            <p className="text-white font-medium">{result.studentName}</p>
          )}
          {showExam && (
            <p className="text-white/60 text-sm">{result.examTitle}</p>
          )}
          <div className="flex gap-4 mt-2 text-white/60 text-sm">
            <span>Score: {result.score}/{result.maxScore}</span>
            <span>Percentage: {result.percentage}%</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <GradeBadge grade={result.grade} />
          <span className={`text-xs ${result.published ? 'text-emerald-400' : 'text-amber-400'}`}>
            {result.published ? '● Published' : '● Draft'}
          </span>
        </div>
      </div>
    </GlassCard>
  );
};

/**
 * GradeDistributionChart - Chart showing grade distribution
 */
export const GradeDistributionChart = ({ analytics }) => {
  const grades = ['A', 'B', 'C', 'D', 'F'];
  const maxCount = Math.max(...Object.values(analytics?.distribution || {}), 1);
  
  const gradeColors = {
    A: 'bg-emerald-500',
    B: 'bg-blue-500',
    C: 'bg-amber-500',
    D: 'bg-orange-500',
    F: 'bg-red-500',
  };

  return (
    <GlassCard>
      <GlassCardHeader title="Grade Distribution" />
      <div className="flex items-end gap-3 h-40 mt-4">
        {grades.map((grade) => {
          const count = analytics?.distribution?.[grade] || 0;
          const height = (count / maxCount) * 100;
          
          return (
            <div key={grade} className="flex-1 flex flex-col items-center">
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: `${height}%` }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className={`w-full rounded-t-lg ${gradeColors[grade]}`}
              />
              <span className="text-white/60 text-sm mt-2">{grade}</span>
              <span className="text-white/40 text-xs">{count}</span>
            </div>
          );
        })}
      </div>
    </GlassCard>
  );
};

/**
 * StatsCard - Card for displaying exam statistics
 */
export const StatsCard = ({ label, value, icon: Icon, trend, color = 'blue' }) => {
  const colorClasses = {
    blue: 'text-blue-400',
    emerald: 'text-emerald-400',
    amber: 'text-amber-400',
    purple: 'text-purple-400',
  };

  return (
    <GlassCard>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-white/50 mb-1">{label}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
          {trend && (
            <p className={`text-sm mt-2 ${trend > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
            </p>
          )}
        </div>
        {Icon && (
          <div className="p-3 bg-white/5 rounded-xl">
            <Icon className={`w-6 h-6 ${colorClasses[color]}`} />
          </div>
        )}
      </div>
    </GlassCard>
  );
};

export default GlassCard;
