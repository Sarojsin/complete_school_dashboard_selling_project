import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', padding = 'p-6', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
    className={`bg-gradient-to-br from-pink-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl ${className}`}>
    <div className={padding}>{children}</div>
  </motion.div>
);

export const VideoCard = ({ video, onPlay }) => (
  <GlassCard className="overflow-hidden" padding="p-0">
    <div className="relative aspect-video bg-black/50" onClick={() => onPlay(video.id)}>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">▶</div>
      </div>
      <span className="absolute bottom-2 right-2 bg-black/70 px-2 py-1 text-xs text-white rounded">{video.duration}</span>
    </div>
    <div className="p-4">
      <h4 className="text-white font-medium mb-1 line-clamp-1">{video.title}</h4>
      <p className="text-white/60 text-sm mb-2 line-clamp-1">{video.description}</p>
      <div className="flex items-center justify-between text-white/50 text-xs">
        <span>👁 {video.views} • ❤️ {video.likes}</span>
        <span>{video.courseName}</span>
      </div>
    </div>
  </GlassCard>
);

export const PlaylistCard = ({ playlist, onPlay }) => (
  <GlassCard>
    <div className="flex items-center gap-4">
      <div className="w-16 h-16 bg-pink-500/20 rounded-lg flex items-center justify-center text-pink-400">▶</div>
      <div className="flex-1">
        <h4 className="text-white font-medium">{playlist.name}</h4>
        <p className="text-white/60 text-sm">{playlist.videoCount} videos</p>
      </div>
      <button onClick={() => onPlay(playlist.id)} className="px-3 py-1 bg-white/10 text-white/60 hover:text-white rounded-lg text-sm">Play</button>
    </div>
  </GlassCard>
);

export const SkeletonVideoCard = ({ count = 3 }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="bg-gradient-to-br from-pink-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden">
        <div className="aspect-video bg-white/5" />
        <div className="p-4"><div className="h-4 bg-white/10 rounded w-3/4 mb-2" /><div className="h-3 bg-white/10 rounded w-1/2" /></div>
      </div>
    ))}
  </div>
);

export default GlassCard;
