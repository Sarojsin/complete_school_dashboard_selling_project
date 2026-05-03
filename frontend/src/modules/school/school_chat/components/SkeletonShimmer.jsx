// =====================
// SKELETON SHIMMER - Chat Module
// =====================

import { motion } from 'framer-motion';

// Chat List Skeleton
export const ChatListSkeleton = ({ items = 8 }) => (
  <div className="space-y-2">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
        className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors">
        <div className="shimmer-skeleton h-12 w-12 rounded-full" />
        <div className="flex-1 min-w-0">
          <div className="shimmer-skeleton h-4 w-24 mb-2" />
          <div className="shimmer-skeleton h-3 w-32" />
        </div>
        <div className="text-right">
          <div className="shimmer-skeleton h-3 w-12 mb-1" />
          <div className="shimmer-skeleton h-5 w-5 rounded-full" />
        </div>
      </motion.div>
    ))}
  </div>
);

// Chat Window Skeleton
export const ChatWindowSkeleton = () => (
  <div className="flex flex-col h-full">
    <div className="p-4 border-b border-white/10">
      <div className="flex items-center gap-3">
        <div className="shimmer-skeleton h-10 w-10 rounded-full" />
        <div>
          <div className="shimmer-skeleton h-4 w-24 mb-1" />
          <div className="shimmer-skeleton h-3 w-16" />
        </div>
      </div>
    </div>
    <div className="flex-1 p-4 space-y-4 overflow-hidden">
      {[...Array(6)].map((_, i) => (
        <div key={i} className={`flex ${i % 2 === 0 ? 'justify-start' : 'justify-end'}`}>
          <div className={`shimmer-skeleton h-16 ${i % 2 === 0 ? 'w-48' : 'w-40'} rounded-2xl`} />
        </div>
      ))}
    </div>
    <div className="p-4 border-t border-white/10">
      <div className="shimmer-skeleton h-12 w-full rounded-xl" />
    </div>
  </div>
);

// Message Bubble Skeleton
export const MessageBubbleSkeleton = ({ isOwn = false }) => (
  <div className={`flex ${isOwn ? 'justify-end' : 'justify-start'} mb-4`}>
    <div className={`shimmer-skeleton h-16 ${isOwn ? 'w-48' : 'w-56'} rounded-2xl ${isOwn ? 'rounded-br-md' : 'rounded-bl-md'}`} />
  </div>
);

// Contact Skeleton
export const ContactSkeleton = () => (
  <div className="flex items-center gap-3 p-3">
    <div className="shimmer-skeleton h-12 w-12 rounded-full" />
    <div className="flex-1">
      <div className="shimmer-skeleton h-4 w-28 mb-2" />
      <div className="shimmer-skeleton h-3 w-40" />
    </div>
  </div>
);

// Group Card Skeleton
export const GroupCardSkeleton = () => (
  <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-4">
    <div className="flex items-center gap-3 mb-3">
      <div className="shimmer-skeleton h-12 w-12 rounded-xl" />
      <div className="flex-1">
        <div className="shimmer-skeleton h-4 w-32 mb-2" />
        <div className="shimmer-skeleton h-3 w-20" />
      </div>
    </div>
    <div className="shimmer-skeleton h-3 w-full mb-2" />
    <div className="flex items-center gap-2">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="shimmer-skeleton h-6 w-6 rounded-full" />
      ))}
      <div className="shimmer-skeleton h-3 w-12 ml-auto" />
    </div>
  </div>
);

// Conversation Item Skeleton
export const ConversationItemSkeleton = () => (
  <div className="flex items-center gap-3 p-3 border-b border-white/5">
    <div className="shimmer-skeleton h-12 w-12 rounded-full" />
    <div className="flex-1 min-w-0">
      <div className="flex items-center justify-between mb-1">
        <div className="shimmer-skeleton h-4 w-28" />
        <div className="shimmer-skeleton h-3 w-12" />
      </div>
      <div className="shimmer-skeleton h-3 w-40" />
    </div>
  </div>
);

// Online Users Skeleton
export const OnlineUsersSkeleton = ({ items = 5 }) => (
  <div className="flex flex-wrap gap-2">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.1 }}
        className="flex items-center gap-2 px-3 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20">
        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        <div className="shimmer-skeleton h-3 w-16" />
      </motion.div>
    ))}
  </div>
);

// Typing Indicator Skeleton
export const TypingIndicatorSkeleton = () => (
  <div className="flex items-center gap-1 p-3">
    {[...Array(3)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0.3 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.15, duration: 0.5, repeat: Infinity, repeatType: 'reverse' }}
        className="w-2 h-2 rounded-full bg-white/40" />
    ))}
  </div>
);

// Search Results Skeleton
export const SearchResultsSkeleton = ({ items = 4 }) => (
  <div className="space-y-2">
    {[...Array(items)].map((_, i) => (
      <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
        className="p-3 rounded-xl bg-white/5">
        <div className="shimmer-skeleton h-4 w-3/4 mb-2" />
        <div className="shimmer-skeleton h-3 w-1/2" />
      </motion.div>
    ))}
  </div>
);

// Settings Skeleton
export const ChatSettingsSkeleton = () => (
  <div className="space-y-4">
    {[...Array(5)].map((_, i) => (
      <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/5">
        <div className="shimmer-skeleton h-4 w-32" />
        <div className="shimmer-skeleton h-6 w-12 rounded-full" />
      </div>
    ))}
  </div>
);

export default {
  ChatListSkeleton,
  ChatWindowSkeleton,
  MessageBubbleSkeleton,
  ContactSkeleton,
  GroupCardSkeleton,
  ConversationItemSkeleton,
  OnlineUsersSkeleton,
  TypingIndicatorSkeleton,
  SearchResultsSkeleton,
  ChatSettingsSkeleton,
};
