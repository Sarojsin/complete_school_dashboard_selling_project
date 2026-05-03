// =====================
// GLASSCARD - Library Module
// =====================
import { motion } from 'framer-motion';

export const GlassCard = ({ children, className = '', padding = 'md' }) => {
  const paddings = { none: '', sm: 'p-3', md: 'p-4', lg: 'p-6' };
  return <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className={`bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl ${paddings[padding]} ${className}`}>{children}</motion.div>;
};

export const StatCard = ({ title, value, icon: Icon, color = 'emerald', delay = 0 }) => {
  const colors = { emerald: 'from-emerald-500/20 to-teal-600/10 border-emerald-500/30', amber: 'from-amber-500/20 to-amber-600/10 border-amber-500/30', red: 'from-red-500/20 to-red-600/10 border-red-500/30', primary: 'from-primary-500/20 to-primary-600/10 border-primary-500/30' };
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }} className={`glass-card bg-gradient-to-br ${colors[color]} border p-6`}>
      <div className="flex justify-between items-start">
        <div><p className="text-white/60 text-sm mb-1">{title}</p><h3 className="text-3xl font-bold text-white">{value}</h3></div>
        {Icon && <div className="p-3 rounded-xl bg-white/10"><Icon className={`w-6 h-6 text-${color}-400`} /></div>}
      </div>
    </motion.div>
  );
};

export const BookCard = ({ book, onClick, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }} onClick={onClick} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
    className="glass-card p-4 cursor-pointer hover:border-white/20 transition-all">
    <div className="h-32 bg-gradient-to-br from-primary-500/20 to-purple-500/20 rounded-lg mb-4 flex items-center justify-center"><span className="text-4xl text-white/30">📚</span></div>
    <h4 className="text-white font-medium truncate mb-1">{book?.title || 'Title'}</h4>
    <p className="text-white/50 text-sm truncate mb-2">{book?.author || 'Author'}</p>
    <div className="flex items-center justify-between">
      <span className={`px-2 py-1 rounded-full text-xs ${book?.available ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>{book?.available ? 'Available' : 'Borrowed'}</span>
    </div>
  </motion.div>
);

export const LoanStatusBadge = ({ status }) => {
  const styles = { active: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30', overdue: 'bg-red-500/20 text-red-400 border-red-500/30', returned: 'bg-primary-500/20 text-primary-400 border-primary-500/30' };
  return <span className={`px-3 py-1 rounded-full text-xs font-medium border ${styles[status] || styles.active}`}>{status?.toUpperCase()}</span>;
};

export const DataTable = ({ columns, data, onRowClick, loading }) => (
  <div className="glass-card overflow-hidden">
    <table className="w-full border-collapse">
      <thead><tr className="border-b border-white/10">{columns.map((col) => <th key={col.key} className="text-left text-white/60 text-sm font-medium px-4 py-3">{col.label}</th>)}</tr></thead>
      <tbody>
        {loading ? <tr><td colSpan={columns.length} className="text-center py-8"><div className="shimmer-skeleton h-8 w-full" /></td></tr> : data?.length === 0 ? <tr><td colSpan={columns.length} className="text-center py-8 text-white/40">No data</td></tr> :
          data.map((row, i) => <motion.tr key={row.id || i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }} onClick={() => onRowClick?.(row)} className="border-b border-white/5 hover:bg-white/5 cursor-pointer">{columns.map((col) => <td key={col.key} className="px-4 py-3 text-white">{col.render ? col.render(row[col.key], row) : row[col.key]}</td>)}</motion.tr>)}
      </tbody>
    </table>
  </div>
);

export const GlassButton = ({ children, variant = 'primary', size = 'md', disabled = false, onClick, className = '' }) => {
  const variants = { primary: 'bg-primary-600/80 hover:bg-primary-600 text-white', secondary: 'bg-white/10 hover:bg-white/20 text-white', emerald: 'bg-emerald-600/80 hover:bg-emerald-600 text-white', danger: 'bg-red-600/80 hover:bg-red-600 text-white' };
  const sizes = { sm: 'py-1.5 px-3 text-sm', md: 'py-2 px-4 text-base', lg: 'py-3 px-6 text-lg' };
  return <button onClick={onClick} disabled={disabled} className={`font-medium rounded-xl transition-all hover:scale-[1.02] disabled:opacity-50 flex items-center gap-2 ${variants[variant]} ${sizes[size]} ${className}`}>{children}</button>;
};

export const SearchInput = ({ value, onChange, placeholder = 'Search...' }) => (
  <div className="relative">
    <input type="text" value={value} onChange={onChange} placeholder={placeholder} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 pl-10 text-white placeholder-white/40 focus:outline-none focus:border-emerald-500/50" />
    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
  </div>
);

export default { GlassCard, StatCard, BookCard, LoanStatusBadge, DataTable, GlassButton, SearchInput };
