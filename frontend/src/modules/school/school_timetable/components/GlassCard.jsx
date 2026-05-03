// GLASSCARD - Timetable Module
import { motion } from 'framer-motion';

export const GlassCard = ({ children, className = '' }) => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className={`bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl ${className}`}>{children}</motion.div>
);

export const TimetableSlot = ({ entry, onClick, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay }} onClick={onClick} whileHover={{ scale: 1.02 }}
    className="glass-card p-3 cursor-pointer hover:border-primary-500/30 transition-all border">
    <h5 className="text-white font-medium text-sm truncate">{entry?.subject || 'Subject'}</h5>
    <p className="text-white/50 text-xs truncate">{entry?.teacher || 'Teacher'}</p>
    <p className="text-white/40 text-xs">{entry?.room || 'Room'}</p>
  </motion.div>
);

export const PeriodCard = ({ period, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay }} className="glass-card p-3 flex items-center justify-between">
    <div><h5 className="text-white font-medium">{period?.name || 'Period'}</h5><p className="text-white/50 text-sm">{period?.time || 'Time'}</p></div>
  </motion.div>
);

export default { GlassCard, TimetableSlot, PeriodCard };
