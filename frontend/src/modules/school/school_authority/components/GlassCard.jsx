// =====================
// GLASSCARD - Authority Module
// =====================

import { motion } from 'framer-motion';

// Base GlassCard
export const GlassCard = ({ children, className = '', hover = false, onClick, gradient = 'slate', padding = 'md' }) => {
  const gradients = { 
    slate: 'from-slate-800/80 to-slate-900/80', 
    primary: 'from-primary-600/20 to-purple-600/20', 
    emerald: 'from-emerald-600/20 to-teal-600/20', 
    amber: 'from-amber-600/20 to-orange-600/20', 
    red: 'from-red-600/20 to-pink-600/20',
    authority: 'from-authority-600/20 to-sky-600/20',
    danger: 'from-red-600/20 to-rose-600/20',
  };
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

// Stat Card - Authority Dashboard
export const StatCard = ({ title, value, subtitle, icon: Icon, color = 'primary', trend, trendValue, delay = 0 }) => {
  const colorStyles = { 
    primary: 'from-primary-500/20 to-primary-600/10 border-primary-500/30', 
    authority: 'from-authority-500/20 to-sky-600/10 border-authority-500/30',
    success: 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30', 
    warning: 'from-amber-500/20 to-amber-600/10 border-amber-500/30', 
    danger: 'from-red-500/20 to-red-600/10 border-red-500/30' 
  };
  const iconColors = { 
    primary: 'text-primary-400', 
    authority: 'text-authority-400',
    success: 'text-emerald-400', 
    warning: 'text-amber-400', 
    danger: 'text-red-400' 
  };
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay }}
      className={`glass-card bg-gradient-to-br ${colorStyles[color]} border p-6`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-white/60 text-sm mb-1">{title}</p>
          <h3 className="text-3xl font-bold text-white">{value}</h3>
          {subtitle && <p className="text-white/50 text-xs mt-2">{subtitle}</p>}
          {trend && (
            <p className={`text-sm mt-2 ${trend === 'up' ? 'text-emerald-400' : 'text-red-400'}`}>
              {trend === 'up' ? '↑' : '↓'} {trendValue}% from last month
            </p>
          )}
        </div>
        {Icon && <div className="p-3 rounded-xl bg-white/10"><Icon className={`w-6 h-6 ${iconColors[color]}`} /></div>}
      </div>
    </motion.div>
  );
};

// Data Table
export const DataTable = ({ columns, data, onRowClick, loading, emptyMessage = 'No data available' }) => (
  <div className="glass-card overflow-hidden">
    <table className="w-full border-collapse">
      <thead>
        <tr className="border-b border-white/10">
          {columns.map((col) => (
            <th key={col.key} className="text-left text-white/60 text-sm font-medium px-4 py-3">{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {loading ? (
          <tr><td colSpan={columns.length} className="text-center py-8"><div className="shimmer-skeleton h-8 w-full" /></td></tr>
        ) : data?.length === 0 ? (
          <tr><td colSpan={columns.length} className="text-center py-8 text-white/40">{emptyMessage}</td></tr>
        ) : (
          data.map((row, index) => (
            <motion.tr key={row.id || index} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: index * 0.03 }}
              onClick={() => onRowClick?.(row)}
              className="border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors">
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-white">{col.render ? col.render(row[col.key], row) : row[col.key]}</td>
              ))}
            </motion.tr>
          ))
        )}
      </tbody>
    </table>
  </div>
);

// Fee Status Badge
export const FeeStatusBadge = ({ status }) => {
  const styles = { paid: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30', pending: 'bg-amber-500/20 text-amber-400 border-amber-500/30', overdue: 'bg-red-500/20 text-red-400 border-red-500/30', partial: 'bg-primary-500/20 text-primary-400 border-primary-500/30' };
  return <span className={`px-3 py-1 rounded-full text-xs font-medium border ${styles[status] || styles.pending}`}>{status?.toUpperCase()}</span>;
};

// Student Status Badge
export const StudentStatusBadge = ({ status }) => {
  const styles = { active: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30', inactive: 'bg-slate-500/20 text-slate-400 border-slate-500/30', suspended: 'bg-red-500/20 text-red-400 border-red-500/30', graduated: 'bg-primary-500/20 text-primary-400 border-primary-500/30' };
  return <span className={`px-3 py-1 rounded-full text-xs font-medium border ${styles[status] || styles.active}`}>{status?.toUpperCase()}</span>;
};

// Quick Action Button
export const QuickActionButton = ({ icon: Icon, label, color, onClick, delay = 0 }) => {
  const colorClasses = { 
    primary: 'from-primary-600 to-primary-700 hover:from-primary-500 hover:to-primary-600', 
    authority: 'from-authority-600 to-authority-700 hover:from-authority-500 hover:to-authority-600',
    success: 'from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600', 
    warning: 'from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600', 
    danger: 'from-red-600 to-red-700 hover:from-red-500 hover:to-red-600',
    purple: 'from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600' 
  };
  return (
    <motion.button initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay }} onClick={onClick}
      className={`p-4 rounded-2xl bg-gradient-to-br ${colorClasses[color]} text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 active:scale-95 flex flex-col items-center gap-2`}>
      {Icon && <Icon className="w-6 h-6" />}
      <span className="text-sm font-medium">{label}</span>
    </motion.button>
  );
};

// Animated Progress Bar
export const AnimatedProgressBar = ({ value, max = 100, label, color = 'primary', showPercentage = true }) => {
  const percentage = Math.min((value / max) * 100, 100);
  const colorClasses = { 
    primary: 'bg-gradient-to-r from-primary-500 to-primary-600', 
    authority: 'bg-gradient-to-r from-authority-500 to-sky-600',
    success: 'bg-gradient-to-r from-emerald-500 to-emerald-600', 
    warning: 'bg-gradient-to-r from-amber-500 to-amber-600', 
    danger: 'bg-gradient-to-r from-red-500 to-red-600' 
  };
  return (
    <div className="mb-4">
      {(label || showPercentage) && <div className="flex justify-between mb-2">
        {label && <span className="text-white/70 text-sm">{label}</span>}
        {showPercentage && <span className="text-white font-medium">{Math.round(percentage)}%</span>}
      </div>}
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <motion.div initial={{ width: 0 }} animate={{ width: `${percentage}%` }} transition={{ duration: 0.8, ease: [0.34, 1.56, 0.64, 1], delay: 0.2 }} 
          className={`h-full ${colorClasses[color]} rounded-full`} />
      </div>
    </div>
  );
};

// Glass Button
export const GlassButton = ({ children, variant = 'primary', size = 'md', disabled = false, loading = false, onClick, className = '', icon: Icon }) => {
  const variants = { 
    primary: 'bg-primary-600/80 hover:bg-primary-600 text-white', 
    authority: 'bg-authority-600/80 hover:bg-authority-600 text-white',
    secondary: 'bg-white/10 hover:bg-white/20 text-white', 
    success: 'bg-emerald-600/80 hover:bg-emerald-600 text-white', 
    danger: 'bg-red-600/80 hover:bg-red-600 text-white' 
  };
  const sizes = { sm: 'py-1.5 px-3 text-sm', md: 'py-2 px-4 text-base', lg: 'py-3 px-6 text-lg' };
  return (
    <button onClick={onClick} disabled={disabled || loading}
      className={`font-medium rounded-xl transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${variants[variant]} ${sizes[size]} ${className}`}>
      {loading ? <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" /> : Icon ? <Icon className="w-5 h-5" /> : null}
      {children}
    </button>
  );
};

// Empty State
export const EmptyState = ({ icon: Icon, title, description, action }) => (
  <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass-card p-12 text-center">
    {Icon && <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-authority-500/30 to-sky-500/30 flex items-center justify-center"><Icon className="w-12 h-12 text-white/60" /></div>}
    <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
    {description && <p className="text-white/50 max-w-sm mx-auto mb-6">{description}</p>}
    {action && <button className="bg-authority-600 hover:bg-authority-500 text-white font-medium py-2 px-6 rounded-xl transition-colors">{action}</button>}
  </motion.div>
);

// Search Input
export const SearchInput = ({ value, onChange, placeholder = 'Search...', className = '' }) => (
  <div className={`relative ${className}`}>
    <input type="text" value={value} onChange={onChange} placeholder={placeholder}
      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 pl-10 text-white placeholder-white/40 focus:outline-none focus:border-authority-500/50 transition-colors" />
    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  </div>
);

// Modal
export const Modal = ({ isOpen, onClose, title, children, size = 'md' }) => {
  if (!isOpen) return null;
  const sizes = { sm: 'max-w-md', md: 'max-w-lg', lg: 'max-w-2xl', xl: 'max-w-4xl' };
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
      <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }}
        onClick={(e) => e.stopPropagation()} className={`bg-gradient-to-br from-slate-800/95 to-slate-900/95 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl w-full ${sizes[size]} max-h-[90vh] overflow-auto`}>
        {title && <div className="p-6 border-b border-white/10"><h2 className="text-xl font-semibold text-white">{title}</h2></div>}
        <div className="p-6">{children}</div>
      </motion.div>
    </motion.div>
  );
};

// Badge
export const Badge = ({ children, variant = 'default' }) => {
  const variants = { default: 'bg-white/10 text-white/60', primary: 'bg-primary-500/20 text-primary-400', authority: 'bg-authority-500/20 text-authority-400', success: 'bg-emerald-500/20 text-emerald-400', warning: 'bg-amber-500/20 text-amber-400', danger: 'bg-red-500/20 text-red-400' };
  return <span className={`inline-flex items-center rounded-full font-medium ${variants[variant]} px-3 py-1 text-sm`}>{children}</span>;
};

export default { GlassCard, StatCard, DataTable, FeeStatusBadge, StudentStatusBadge, QuickActionButton, AnimatedProgressBar, GlassButton, EmptyState, SearchInput, Modal, Badge };
