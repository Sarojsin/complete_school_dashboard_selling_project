import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', padding = 'p-6', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
    className={`bg-gradient-to-br from-purple-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl ${className}`}>
    <div className={padding}>{children}</div>
  </motion.div>
);

export const GlassCardHeader = ({ title, subtitle, action }) => (
  <div className="flex items-start justify-between mb-4">
    <div><h3 className="text-lg font-semibold text-white">{title}</h3>{subtitle && <p className="text-sm text-white/50">{subtitle}</p>}</div>
    {action}
  </div>
);

export const TeacherCard = ({ teacher, onViewPerformance }) => (
  <GlassCard>
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-purple-500/20 rounded-full flex items-center justify-center text-purple-400 font-bold">{teacher.name?.charAt(0)}</div>
        <div><p className="text-white font-medium">{teacher.name}</p><p className="text-white/60 text-sm">{teacher.courses?.length} courses</p></div>
      </div>
      <button onClick={() => onViewPerformance(teacher.id)} className="px-3 py-1 text-sm bg-white/10 text-white/60 hover:text-white rounded-lg">View</button>
    </div>
  </GlassCard>
);

// Simple skeleton
export const SkeletonCard = ({ count = 3 }) => (
  <div className="space-y-3">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="bg-gradient-to-br from-purple-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/10 rounded-full" />
          <div className="flex-1"><div className="h-4 bg-white/10 rounded w-32 mb-1" /><div className="h-3 bg-white/10 rounded w-20" /></div>
        </div>
      </div>
    ))}
  </div>
);

export default GlassCard;
