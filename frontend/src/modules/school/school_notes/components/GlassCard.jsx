import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', padding = 'p-6', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
    className={`bg-gradient-to-br from-orange-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl ${className}`}>
    <div className={padding}>{children}</div>
  </motion.div>
);

export const NoteCard = ({ note, onDownload, onShare }) => (
  <GlassCard>
    <div className="flex justify-between items-start mb-2">
      <h4 className="text-white font-medium">{note.title}</h4>
      <span className="text-xs text-white/50">{note.subject}</span>
    </div>
    <p className="text-white/60 text-sm mb-3 line-clamp-2">{note.description}</p>
    <div className="flex items-center justify-between">
      <div className="flex gap-3 text-white/50 text-sm">
        <span>👁 {note.views}</span>
        <span>❤️ {note.likes}</span>
        <span>📚 {note.subject}</span>
      </div>
      <div className="flex gap-2">
        <button onClick={() => onDownload(note.id)} className="px-2 py-1 text-xs bg-white/10 rounded">Download</button>
      </div>
    </div>
  </GlassCard>
);

export const SkeletonNoteCard = ({ count = 3 }) => (
  <div className="space-y-3">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="bg-gradient-to-br from-orange-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
        <div className="h-4 bg-white/10 rounded w-3/4 mb-2" />
        <div className="h-3 bg-white/10 rounded w-full mb-3" />
        <div className="flex gap-3"><div className="h-3 bg-white/10 rounded w-12" /><div className="h-3 bg-white/10 rounded w-12" /></div>
      </div>
    ))}
  </div>
);

export default GlassCard;
