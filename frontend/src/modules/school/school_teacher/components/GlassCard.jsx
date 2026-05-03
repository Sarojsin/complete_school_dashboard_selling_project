// =====================
// GLASSCARD - Teacher Module
// =====================

import { motion } from 'framer-motion';

// Base GlassCard
export const GlassCard = ({ children, className = '', hover = false, onClick, gradient = 'slate', padding = 'md' }) => {
  const gradients = { slate: 'from-slate-800/80 to-slate-900/80', primary: 'from-primary-600/20 to-purple-600/20', emerald: 'from-emerald-600/20 to-teal-600/20', amber: 'from-amber-600/20 to-orange-600/20', red: 'from-red-600/20 to-pink-600/20' };
  const paddings = { none: '', sm: 'p-3', md: 'p-6', lg: 'p-8' };
  const Component = onClick ? motion.button : motion.div;
  return (
    <Component onClick={onClick} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      whileHover={hover ? { scale: 1.02 } : undefined} whileTap={onClick ? { scale: 0.98 } : undefined}
      className={`bg-gradient-to-br ${gradients[gradient]} backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl ${paddings[padding]} ${hover ? 'cursor-pointer transition-all duration-200 hover:border-white/30 hover:shadow-2xl' : ''} ${className}`}>
      {children}
    </Component>
  );
};

// Stat Card
export const StatCard = ({ title, value, subtitle, icon: Icon, color = 'primary', delay = 0 }) => {
  const colorStyles = { primary: 'from-primary-500/20 to-primary-600/10 border-primary-500/30', success: 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30', warning: 'from-amber-500/20 to-amber-600/10 border-amber-500/30', danger: 'from-red-500/20 to-red-600/10 border-red-500/30' };
  const iconColors = { primary: 'text-primary-400', success: 'text-emerald-400', warning: 'text-amber-400', danger: 'text-red-400' };
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay }}
      className={`glass-card bg-gradient-to-br ${colorStyles[color]} border p-6`}>
      <div className="flex items-start justify-between">
        <div><p className="text-white/60 text-sm mb-1">{title}</p><h3 className="text-3xl font-bold text-white">{value}</h3>{subtitle && <p className="text-white/50 text-xs mt-2">{subtitle}</p>}</div>
        {Icon && <div className="p-3 rounded-xl bg-white/10"><Icon className={`w-6 h-6 ${iconColors[color]}`} /></div>}
      </div>
    </motion.div>
  );
};

// Animated Progress Bar
export const AnimatedProgressBar = ({ value, max = 100, label, color = 'primary', showPercentage = true }) => {
  const percentage = Math.min((value / max) * 100, 100);
  const colorClasses = { primary: 'bg-gradient-to-r from-primary-500 to-primary-600', success: 'bg-gradient-to-r from-emerald-500 to-emerald-600', warning: 'bg-gradient-to-r from-amber-500 to-amber-600', danger: 'bg-gradient-to-r from-red-500 to-red-600' };
  return (
    <div className="mb-4">
      {(label || showPercentage) && <div className="flex justify-between mb-2">{label && <span className="text-white/70 text-sm">{label}</span>}{showPercentage && <span className="text-white font-medium">{Math.round(percentage)}%</span>}</div>}
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <motion.div initial={{ width: 0 }} animate={{ width: `${percentage}%` }} transition={{ duration: 0.8, ease: [0.34, 1.56, 0.64, 1], delay: 0.2 }} className={`h-full ${colorClasses[color]} rounded-full`} />
      </div>
    </div>
  );
};

// Quick Action Button
export const QuickActionButton = ({ icon: Icon, label, color, onClick, delay = 0 }) => {
  const colorClasses = { primary: 'from-primary-600 to-primary-700 hover:from-primary-500 hover:to-primary-600', success: 'from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600', warning: 'from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600', purple: 'from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600' };
  return (
    <motion.button initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay }} onClick={onClick}
      className={`p-4 rounded-2xl bg-gradient-to-br ${colorClasses[color]} text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 active:scale-95 flex flex-col items-center gap-2`}>
      <Icon className="w-6 h-6" /><span className="text-sm font-medium">{label}</span>
    </motion.button>
  );
};

// Attendance Toggle Button
export const AttendanceToggle = ({ status, onClick }) => {
  const statusStyles = { present: 'bg-emerald-500/30 border-2 border-emerald-500/50', absent: 'bg-red-500/30 border-2 border-red-500/50', default: 'bg-white/5 border-2 border-white/10 hover:border-white/30' };
  const statusColors = { present: 'text-emerald-400', absent: 'text-red-400', default: 'text-white/40' };
  return (
    <motion.button whileTap={{ scale: 0.95 }} onClick={onClick}
      className={`p-3 rounded-xl text-center transition-all duration-200 ${statusStyles[status] || statusStyles.default}`}>
      <p className="text-white text-xs font-medium truncate">{status}</p>
      <p className={`text-lg font-bold ${statusColors[status] || statusColors.default}`}>{status === 'present' ? 'P' : status === 'absent' ? 'A' : '-'}</p>
    </motion.button>
  );
};

// Badge
export const Badge = ({ children, variant = 'default' }) => {
  const variants = { default: 'bg-white/10 text-white/60', primary: 'bg-primary-500/20 text-primary-400', success: 'bg-emerald-500/20 text-emerald-400', warning: 'bg-amber-500/20 text-amber-400', danger: 'bg-red-500/20 text-red-400' };
  return <span className={`inline-flex items-center rounded-full font-medium ${variants[variant]} px-3 py-1 text-sm`}>{children}</span>;
};

// Glass Button
export const GlassButton = ({ children, variant = 'primary', size = 'md', disabled = false, loading = false, onClick, className = '', icon: Icon }) => {
  const variants = { primary: 'bg-primary-600/80 hover:bg-primary-600 text-white', secondary: 'bg-white/10 hover:bg-white/20 text-white', success: 'bg-emerald-600/80 hover:bg-emerald-600 text-white', danger: 'bg-red-600/80 hover:bg-red-600 text-white' };
  const sizes = { sm: 'py-1.5 px-3 text-sm', md: 'py-2 px-4 text-base', lg: 'py-3 px-6 text-lg' };
  return (
    <button onClick={onClick} disabled={disabled || loading}
      className={`font-medium rounded-xl transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${variants[variant]} ${sizes[size]} ${className}`}>
      {loading ? <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" /> : Icon ? <Icon className="w-5 h-5" /> : null}{children}
    </button>
  );
};

// Empty State
export const EmptyState = ({ icon: Icon, title, description, action }) => (
  <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass-card p-12 text-center">
    {Icon && <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center"><Icon className="w-12 h-12 text-white/60" /></div>}
    <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
    {description && <p className="text-white/50 max-w-sm mx-auto mb-6">{description}</p>}
    {action && <button className="bg-primary-600 hover:bg-primary-500 text-white font-medium py-2 px-6 rounded-xl transition-colors">{action}</button>}
  </motion.div>
);

export default { GlassCard, StatCard, AnimatedProgressBar, QuickActionButton, AttendanceToggle, Badge, GlassButton, EmptyState };
