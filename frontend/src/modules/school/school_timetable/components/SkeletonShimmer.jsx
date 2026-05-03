// SKELETON SHIMMER - Timetable Module
import { motion } from 'framer-motion';

export const TimetableSkeleton = () => (
  <div className="space-y-4">
    {[...Array(6)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.1 }} className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
        <div className="shimmer-skeleton h-8 w-full rounded-lg" />
      </motion.div>
    ))}
  </div>
);

export const TimetableGridSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden">
    <div className="grid grid-cols-8 gap-2 p-4">
      {[...Array(40)].map((_, i) => <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.02 }} className="shimmer-skeleton h-16 rounded-lg" />)}
    </div>
  </div>
);

export default { TimetableSkeleton, TimetableGridSkeleton };
