import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', padding = 'p-6', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
    className={`bg-gradient-to-br from-cyan-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl ${className}`}>
    <div className={padding}>{children}</div>
  </motion.div>
);

export const PaymentStatusBadge = ({ status }) => {
  const c = { paid: 'bg-emerald-500/20 text-emerald-400', pending: 'bg-amber-500/20 text-amber-400', overdue: 'bg-red-500/20 text-red-400' };
  return <span className={`px-3 py-1 rounded-full text-xs ${c[status] || c.pending}`}>{status}</span>;
};

export const FeeCard = ({ fee, onPay }) => (
  <GlassCard>
    <div className="flex justify-between items-start">
      <div><h4 className="text-white font-medium">{fee.title}</h4><p className="text-white/60 text-sm">{fee.dueDate}</p></div>
      <div className="text-right"><p className="text-white font-bold">${fee.amount}</p><PaymentStatusBadge status={fee.status} /></div>
    </div>
    {fee.status !== 'paid' && onPay && <button onClick={() => onPay(fee.id)} className="mt-3 w-full py-2 bg-cyan-500/20 text-cyan-400 rounded-lg">Pay Now</button>}
  </GlassCard>
);

export const StatsCard = ({ label, value, icon: Icon, color = 'cyan' }) => {
  const colors = { cyan: 'text-cyan-400', emerald: 'text-emerald-400', amber: 'text-amber-400' };
  return (
    <GlassCard>
      <div className="flex items-center justify-between">
        <div><p className="text-white/60 text-sm">{label}</p><p className="text-2xl font-bold text-white">{value}</p></div>
        {Icon && <Icon className={`w-8 h-8 ${colors[color]}`} />}
      </div>
    </GlassCard>
  );
};

export default GlassCard;
