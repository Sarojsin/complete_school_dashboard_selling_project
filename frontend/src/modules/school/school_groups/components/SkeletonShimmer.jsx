// SKELETON SHIMMER - Groups Module
import { motion } from 'framer-motion';

export const GroupCardSkeleton = () => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">
    <div className="shimmer-skeleton h-6 w-32 mb-3" />
    <div className="shimmer-skeleton h-4 w-full mb-2" />
    <div className="shimmer-skeleton h-4 w-2/3 mb-4" />
    <div className="flex items-center gap-2"><div className="shimmer-skeleton h-6 w-6 rounded-full" /><div className="shimmer-skeleton h-4 w-16" /></div>
  </motion.div>
);

export const PostSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-4">
    <div className="flex items-center gap-3 mb-4"><div className="shimmer-skeleton h-10 w-10 rounded-full" /><div className="shimmer-skeleton h-4 w-24" /></div>
    <div className="shimmer-skeleton h-4 w-full mb-2" /><div className="shimmer-skeleton h-4 w-3/4" />
  </div>
);

export default { GroupCardSkeleton, PostSkeleton };
