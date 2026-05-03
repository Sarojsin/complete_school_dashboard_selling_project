import { motion } from 'framer-motion';

/**
 * GlassCard - A glassmorphism card component for Super Admin module
 * Features:
 * - Gradient backgrounds with backdrop blur
 * - Smooth animations using Framer Motion
 * - Hover effects with scale and glow
 * - Status indicator support
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
    bg-gradient-to-br from-slate-900/90 to-slate-950/90
    backdrop-blur-2xl
    border border-white/5
    shadow-2xl rounded-2xl
    transition-all duration-300
  `;

  const hoverClasses = hover ? `
    hover:border-white/10 hover:shadow-3xl
    hover:scale-[1.02]
    hover:from-slate-800/90 hover:to-slate-900/90
  ` : '';

  const clickClasses = onClick ? 'cursor-pointer' : '';

  const statusColors = {
    success: 'border-l-4 border-l-emerald-500',
    warning: 'border-l-4 border-l-amber-500',
    error: 'border-l-4 border-l-red-500',
    info: 'border-l-4 border-l-blue-500',
    inactive: 'border-l-4 border-l-slate-500',
    active: 'border-l-4 border-l-emerald-500',
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
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-emerald-500/5 via-blue-500/5 to-purple-500/5 opacity-0 hover:opacity-100 transition-opacity duration-300 rounded-2xl" />
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
            <Icon className="w-5 h-5 text-emerald-400" />
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
    <div className={`mt-4 pt-4 border-t border-white/5 ${className}`}>
      {children}
    </div>
  );
};

/**
 * StatCard - Specialized card for displaying statistics
 */
export const StatCard = ({
  label,
  value,
  change,
  changeType,
  icon: Icon,
  delay = 0,
}) => {
  const changeColors = {
    positive: 'text-emerald-400',
    negative: 'text-red-400',
    neutral: 'text-white/50',
  };

  return (
    <GlassCard delay={delay}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-white/50 mb-1">{label}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
          {change !== undefined && (
            <p className={`text-sm mt-2 ${changeColors[changeType]}`}>
              {changeType === 'positive' && '↑'}
              {changeType === 'negative' && '↓'}
              {Math.abs(change)}%
            </p>
          )}
        </div>
        {Icon && (
          <div className="p-3 bg-white/5 rounded-xl">
            <Icon className="w-6 h-6 text-emerald-400" />
          </div>
        )}
      </div>
    </GlassCard>
  );
};

/**
 * SystemHealthCard - Card showing system health status
 */
export const SystemHealthCard = ({ health, services = [] }) => {
  const statusColors = {
    good: 'bg-emerald-500',
    warning: 'bg-amber-500',
    critical: 'bg-red-500 animate-pulse',
  };

  return (
    <GlassCard status={health?.status === 'good' ? 'success' : health?.status === 'warning' ? 'warning' : 'error'}>
      <GlassCardHeader
        title="System Health"
        icon={() => (
          <div className={`w-3 h-3 rounded-full ${statusColors[health?.status] || 'bg-slate-500'}`} />
        )}
      />
      <div className="grid grid-cols-2 gap-3 mt-4">
        {services.map((service) => (
          <div
            key={service.name}
            className="flex items-center justify-between p-3 bg-white/5 rounded-xl"
          >
            <span className="text-white/60 text-sm">{service.name}</span>
            <span className={`text-xs ${
              service.status === 'up' ? 'text-emerald-400' : 'text-red-400'
            }`}>
              {service.status === 'up' ? '● Online' : '● Offline'}
            </span>
          </div>
        ))}
      </div>
    </GlassCard>
  );
};

/**
 * SchoolCard - Card for displaying school information
 */
export const SchoolCard = ({ school, onActivate, onDeactivate, onView }) => {
  return (
    <GlassCard status={school.active ? 'active' : 'inactive'}>
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-emerald-500/20 to-blue-500/20 rounded-xl flex items-center justify-center">
            <span className="text-xl font-bold text-emerald-400">
              {school.name?.charAt(0) || 'S'}
            </span>
          </div>
          <div>
            <h4 className="text-white font-semibold">{school.name}</h4>
            <p className="text-sm text-white/50">{school.userCount} users</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs ${
          school.active
            ? 'bg-emerald-500/20 text-emerald-400'
            : 'bg-red-500/20 text-red-400'
        }`}>
          {school.active ? 'Active' : 'Inactive'}
        </span>
      </div>
      
      <GlassCardFooter>
        <div className="flex gap-2">
          {school.active ? (
            <button
              onClick={() => onDeactivate?.(school.id)}
              className="px-3 py-1.5 text-sm text-white/60 hover:text-white bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
            >
              Deactivate
            </button>
          ) : (
            <button
              onClick={() => onActivate?.(school.id)}
              className="px-3 py-1.5 text-sm text-emerald-400 hover:text-emerald-300 bg-emerald-500/10 hover:bg-emerald-500/20 rounded-lg transition-colors"
            >
              Activate
            </button>
          )}
          <button
            onClick={() => onView?.(school.id)}
            className="px-3 py-1.5 text-sm text-white/60 hover:text-white bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
          >
            View Details
          </button>
        </div>
      </GlassCardFooter>
    </GlassCard>
  );
};

/**
 * FeatureToggleCard - Card for feature flag management
 */
export const FeatureToggleCard = ({ feature, onToggle }) => {
  return (
    <GlassCard>
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-white font-medium">{feature.name}</h4>
          <p className="text-sm text-white/50">{feature.description}</p>
        </div>
        <button
          onClick={() => onToggle?.(feature.name, !feature.enabled)}
          className={`relative w-12 h-6 rounded-full transition-colors ${
            feature.enabled ? 'bg-emerald-500' : 'bg-white/10'
          }`}
        >
          <div
            className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
              feature.enabled ? 'translate-x-7' : 'translate-x-1'
            }`}
          />
        </button>
      </div>
    </GlassCard>
  );
};

export default GlassCard;
