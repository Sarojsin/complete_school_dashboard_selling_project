import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', padding = 'p-6', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
    className={`bg-gradient-to-br from-green-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl ${className}`}>
    <div className={padding}>{children}</div>
  </motion.div>
);

export const DriveCard = ({ drive, onRegister }) => (
  <GlassCard>
    <div className="flex justify-between items-start mb-2">
      <div><h4 className="text-white font-medium">{drive.company}</h4><p className="text-white/60 text-sm">{drive.date}</p></div>
      <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded">{drive.studentsApplied} applied</span>
    </div>
    <p className="text-white/60 text-sm mb-3">{drive.description}</p>
    {onRegister && !drive.registered && <button onClick={() => onRegister(drive.id)} className="w-full py-2 bg-green-500/20 text-green-400 rounded-lg">Register</button>}
    {drive.registered && <span className="block text-center py-2 text-green-400">✓ Registered</span>}
  </GlassCard>
);

export default GlassCard;
