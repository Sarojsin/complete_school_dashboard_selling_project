// GLASSCARD - Groups Module
import { motion } from 'framer-motion';

export const GlassCard = ({ children, className = '', padding = 'md' }) => {
  const paddings = { none: '', sm: 'p-3', md: 'p-4', lg: 'p-6' };
  return <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className={`bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl ${paddings[padding]} ${className}`}>{children}</motion.div>;
};

export const GroupCard = ({ group, onClick, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }} onClick={onClick} whileHover={{ scale: 1.02 }} className="glass-card p-6 cursor-pointer hover:border-white/20">
    <h4 className="text-white font-semibold text-lg mb-2">{group?.name || 'Group Name'}</h4>
    <p className="text-white/60 text-sm mb-4">{group?.description || 'No description'}</p>
    <div className="flex items-center gap-2"><span className="px-2 py-1 rounded-full bg-primary-500/20 text-primary-400 text-xs">{group?.member_count || 0} members</span></div>
  </motion.div>
);

export const PostCard = ({ post, onLike, onComment, delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }} className="glass-card p-4">
    <div className="flex items-center gap-3 mb-3">
      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500/30 to-purple-500/30 flex items-center justify-center text-white font-medium">{post?.author?.charAt(0) || 'U'}</div>
      <div><h5 className="text-white font-medium">{post?.author || 'User'}</h5><p className="text-white/40 text-xs">{post?.time || 'Just now'}</p></div>
    </div>
    <p className="text-white/80 mb-4">{post?.content || ''}</p>
    <div className="flex items-center gap-4">
      <button onClick={onLike} className="flex items-center gap-1 text-white/60 hover:text-primary-400 transition-colors"><span>👍</span><span>{post?.likes || 0}</span></button>
      <button onClick={onComment} className="flex items-center gap-1 text-white/60 hover:text-primary-400 transition-colors"><span>💬</span><span>{post?.comments || 0}</span></button>
    </div>
  </motion.div>
);

export default { GlassCard, GroupCard, PostCard };
