import { motion } from 'framer-motion';

// GlassCard Component
const GlassCard = ({ children, className = '', status, padding = 'p-6', delay = 0, onClick }) => {
  const statusColors = { present: 'border-l-4 border-l-emerald-500', absent: 'border-l-4 border-l-red-500', late: 'border-l-4 border-l-amber-500', excused: 'border-l-4 border-l-blue-500' };
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
      className={`relative overflow-hidden bg-gradient-to-br from-emerald-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl transition-all duration-300 hover:scale-[1.02] ${statusColors[status] || ''} ${className}`}
      onClick={onClick}>
      <div className={padding}>{children}</div>
    </motion.div>
  );
};

export const GlassCardHeader = ({ title, subtitle, action }) => (
  <div className="flex items-start justify-between mb-4">
    <div><h3 className="text-lg font-semibold text-white">{title}</h3>{subtitle && <p className="text-sm text-white/50">{subtitle}</p>}</div>
    {action && <div>{action}</div>}
  </div>
);

export const AttendanceStatusBadge = ({ status }) => {
  const classes = { present: 'bg-emerald-500/20 text-emerald-400', absent: 'bg-red-500/20 text-red-400', late: 'bg-amber-500/20 text-amber-400', excused: 'bg-blue-500/20 text-blue-400' };
  return <span className={`px-3 py-1 rounded-full text-xs font-medium ${classes[status] || classes.present}`}>{status?.charAt(0).toUpperCase() + status?.slice(1)}</span>;
};

export const AttendanceCard = ({ record, onClick }) => (
  <GlassCard status={record.status} onClick={onClick}>
    <div className="flex items-center justify-between">
      <div><p className="text-white font-medium">{record.studentName}</p><p className="text-white/60 text-sm">{record.date} • {record.courseName}</p></div>
      <AttendanceStatusBadge status={record.status} />
    </div>
  </GlassCard>
);

export const SessionCard = ({ session, onClose }) => (
  <GlassCard>
    <GlassCardHeader title={session.courseName} subtitle={`${session.presentCount}/${session.totalCount} present`} 
      action={session.isActive ? <button onClick={() => onClose(session.id)} className="px-3 py-1 text-sm bg-red-500/20 text-red-400 rounded-lg">Close</button> : null} />
    <div className="flex gap-4 text-white/60 text-sm"><span>📅 {session.date}</span><span>⏰ {session.startTime}</span></div>
  </GlassCard>
);

// Skeleton Components
const SkeletonShimmer = ({ className = '', variant = 'rectangular', width, height }) => {
  const base = 'relative overflow-hidden bg-gradient-to-r from-white/5 via-white/10 to-white/5 bg-[length:200%_100%]';
  const vars = { rectangular: 'rounded-lg', circular: 'rounded-full', text: 'rounded h-4', card: 'rounded-2xl' };
  return (
    <div className={`${base} ${vars[variant]} ${className}`} style={{ width, height }}>
      <motion.div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent" animate={{ x: ['-100%', '100%'] }} transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }} />
    </div>
  );
};

export const SkeletonAttendanceCard = ({ count = 3 }) => (
  <div className="space-y-3">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="bg-gradient-to-br from-emerald-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
        <div className="flex items-center justify-between">
          <div><SkeletonShimmer variant="text" width="120px" height="1rem" className="mb-1" /><SkeletonShimmer variant="text" width="180px" height="0.875rem" /></div>
          <SkeletonShimmer variant="text" width="70px" height="24px" />
        </div>
      </div>
    ))}
  </div>
);

export const SkeletonStatsGrid = ({ count = 4 }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="bg-gradient-to-br from-emerald-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
        <SkeletonShimmer variant="text" width="50%" height="0.75rem" className="mb-2" />
        <SkeletonShimmer variant="text" width="80%" height="2rem" />
      </div>
    ))}
  </div>
);

export default GlassCard;
