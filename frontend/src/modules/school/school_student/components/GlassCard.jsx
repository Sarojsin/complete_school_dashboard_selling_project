// =====================
// GLASSCARD COMPONENT
// Premium glassmorphic card with backdrop blur
// =====================

import { motion } from 'framer-motion';
import { SkeletonShimmer } from './SkeletonShimmer';

// Base GlassCard Component
export const GlassCard = ({ 
  children, 
  className = '', 
  hover = false,
  onClick,
  gradient = 'slate',
  padding = 'md',
}) => {
  const gradients = {
    slate: 'from-slate-800/80 to-slate-900/80',
    primary: 'from-primary-600/20 to-purple-600/20',
    emerald: 'from-emerald-600/20 to-teal-600/20',
    amber: 'from-amber-600/20 to-orange-600/20',
    red: 'from-red-600/20 to-pink-600/20',
  };
  
  const paddings = {
    none: '',
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8',
  };
  
  const Component = onClick ? motion.button : motion.div;
  
  return (
    <Component
      onClick={onClick}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={hover ? { scale: 1.02 } : undefined}
      whileTap={onClick ? { scale: 0.98 } : undefined}
      className={`
        bg-gradient-to-br ${gradients[gradient]}
        backdrop-blur-xl 
        border border-white/10 
        shadow-xl 
        rounded-2xl
        ${paddings[padding]}
        ${hover ? 'cursor-pointer transition-all duration-200 hover:border-white/30 hover:shadow-2xl' : ''}
        ${className}
      `}
    >
      {children}
    </Component>
  );
};

// Stat Card with Icon
export const StatCard = ({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  color = 'primary',
  delay = 0,
}) => {
  const colorStyles = {
    primary: 'from-primary-500/20 to-primary-600/10 border-primary-500/30',
    success: 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30',
    warning: 'from-amber-500/20 to-amber-600/10 border-amber-500/30',
    danger: 'from-red-500/20 to-red-600/10 border-red-500/30',
  };
  
  const iconColors = {
    primary: 'text-primary-400',
    success: 'text-emerald-400',
    warning: 'text-amber-400',
    danger: 'text-red-400',
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className={`glass-card bg-gradient-to-br ${colorStyles[color]} border p-6`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-white/60 text-sm mb-1">{title}</p>
          <h3 className="text-3xl font-bold text-white">{value}</h3>
          {subtitle && <p className="text-white/50 text-xs mt-2">{subtitle}</p>}
        </div>
        {Icon && (
          <div className="p-3 rounded-xl bg-white/10">
            <Icon className={`w-6 h-6 ${iconColors[color]}`} />
          </div>
        )}
      </div>
    </motion.div>
  );
};

// Animated Progress Bar
export const AnimatedProgressBar = ({ 
  value, 
  max = 100, 
  label, 
  color = 'primary',
  showPercentage = true,
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  
  const colorClasses = {
    primary: 'bg-gradient-to-r from-primary-500 to-primary-600',
    success: 'bg-gradient-to-r from-emerald-500 to-emerald-600',
    warning: 'bg-gradient-to-r from-amber-500 to-amber-600',
    danger: 'bg-gradient-to-r from-red-500 to-red-600',
  };
  
  return (
    <div className="mb-4">
      {(label || showPercentage) && (
        <div className="flex justify-between mb-2">
          {label && <span className="text-white/70 text-sm">{label}</span>}
          {showPercentage && <span className="text-white font-medium">{Math.round(percentage)}%</span>}
        </div>
      )}
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ 
            duration: 0.8, 
            ease: [0.34, 1.56, 0.64, 1],
            delay: 0.2 
          }}
          className={`h-full ${colorClasses[color]} rounded-full`}
        />
      </div>
    </div>
  );
};

// Empty State Component
export const EmptyState = ({ 
  icon: Icon, 
  title, 
  description, 
  action,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-12 text-center"
    >
      {Icon && (
        <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center">
          <Icon className="w-12 h-12 text-white/60" />
        </div>
      )}
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      {description && (
        <p className="text-white/50 max-w-sm mx-auto mb-6">{description}</p>
      )}
      {action && (
        <button className="bg-primary-600 hover:bg-primary-500 text-white font-medium py-2 px-6 rounded-xl transition-colors">
          {action}
        </button>
      )}
    </motion.div>
  );
};

// Badge Component
export const Badge = ({ 
  children, 
  variant = 'default',
  size = 'md',
}) => {
  const variants = {
    default: 'bg-white/10 text-white/60',
    primary: 'bg-primary-500/20 text-primary-400',
    success: 'bg-emerald-500/20 text-emerald-400',
    warning: 'bg-amber-500/20 text-amber-400',
    danger: 'bg-red-500/20 text-red-400',
  };
  
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base',
  };
  
  return (
    <span className={`inline-flex items-center rounded-full font-medium ${variants[variant]} ${sizes[size]}`}>
      {children}
    </span>
  );
};

// Glass Button
export const GlassButton = ({ 
  children, 
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  className = '',
  icon: Icon,
}) => {
  const variants = {
    primary: 'bg-primary-600/80 hover:bg-primary-600 text-white',
    secondary: 'bg-white/10 hover:bg-white/20 text-white',
    success: 'bg-emerald-600/80 hover:bg-emerald-600 text-white',
    danger: 'bg-red-600/80 hover:bg-red-600 text-white',
    ghost: 'bg-transparent hover:bg-white/10 text-white',
  };
  
  const sizes = {
    sm: 'py-1.5 px-3 text-sm',
    md: 'py-2 px-4 text-base',
    lg: 'py-3 px-6 text-lg',
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        font-medium rounded-xl transition-all duration-200 
        hover:scale-[1.02] active:scale-[0.98]
        disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
        flex items-center justify-center gap-2
        ${variants[variant]} ${sizes[size]} ${className}
      `}
    >
      {loading ? (
        <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
      ) : Icon ? (
        <Icon className="w-5 h-5" />
      ) : null}
      {children}
    </button>
  );
};

// Glass Input
export const GlassInput = ({
  type = 'text',
  placeholder,
  value,
  onChange,
  name,
  label,
  error,
  icon: Icon,
  className = '',
  ...props
}) => {
  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="text-white/70 text-sm font-medium">{label}</label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40">
            <Icon className="w-5 h-5" />
          </div>
        )}
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          name={name}
          className={`
            w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 
            text-white placeholder:text-white/40 
            focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 
            transition-all duration-200
            ${Icon ? 'pl-10' : ''}
            ${error ? 'border-red-500' : ''}
          `}
          {...props}
        />
      </div>
      {error && (
        <p className="text-red-400 text-sm">{error}</p>
      )}
    </div>
  );
};

export default {
  GlassCard,
  StatCard,
  AnimatedProgressBar,
  EmptyState,
  Badge,
  GlassButton,
  GlassInput,
};
