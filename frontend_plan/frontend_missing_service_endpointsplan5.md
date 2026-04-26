# Implementation Plan - Frontend Missing Services Plan 5: Chat Module API Integration

This plan details the comprehensive API integration for the Chat/Messaging Module with real-time messaging, typing indicators, and glassmorphic chat bubbles.

---

## Part 1: Design System

```javascript
// Chat Module Tailwind
.chat-bubble {
  @apply max-w-[70%] p-4 rounded-2xl backdrop-blur-md;
}

.chat-bubble-sent {
  @apply bg-gradient-to-br from-primary-600 to-primary-700 text-white ml-auto rounded-br-md;
}

.chat-bubble-received {
  @apply bg-gradient-to-br from-white/20 to-white/10 text-white mr-auto rounded-bl-md border border-white/10;
}

.chat-input-glass {
  @apply flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white 
         placeholder:text-white/40 focus:outline-none focus:border-primary-500 
         focus:ring-2 focus:ring-primary-500/20;
}
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_chat/hooks/useChat.js

export const chatKeys = {
  all: ['chat'] as const,
  conversations: () => [...chatKeys.all, 'conversations'] as const,
  conversationById: (id) => [...chatKeys.all, 'conversations', id] as const,
  messages: (convId) => [...chatKeys.all, 'messages', convId] as const,
  unreadCount: () => [...chatKeys.all, 'unread'] as const,
  groups: () => [...chatKeys.all, 'groups'] as const,
};

// Query Hooks
export const useConversations = () => useQuery({
  queryKey: chatKeys.conversations(),
  queryFn: api.getConversations,
  staleTime: 30 * 1000, // Short for chat
});

export const useMessages = (conversationId) => useQuery({
  queryKey: chatKeys.messages(conversationId),
  queryFn: () => api.getMessages(conversationId),
  enabled: !!conversationId,
  refetchInterval: 5000, // Poll every 5 seconds
});

export const useUnreadCount = () => useQuery({
  queryKey: chatKeys.unreadCount(),
  queryFn: api.getUnreadCount,
  refetchInterval: 10000,
});

// Mutations
export const useSendMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ conversationId, data }) => api.sendMessage(conversationId, data),
    onMutate: async ({ conversationId, data }) => {
      await queryClient.cancelQueries({ queryKey: chatKeys.messages(conversationId) });
      const previous = queryClient.getQueryData(chatKeys.messages(conversationId));
      
      // Optimistic update
      queryClient.setQueryData(chatKeys.messages(conversationId), (old = []) => [
        ...old,
        { ...data, id: `temp-${Date.now()}`, status: 'sending', created_at: new Date().toISOString() }
      ]);
      
      return { previous };
    },
    onError: (err, { conversationId }, context) => {
      queryClient.setQueryData(chatKeys.messages(conversationId), context?.previous);
    },
    onSettled: (data, error, { conversationId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(conversationId) });
      queryClient.invalidateQueries({ queryKey: chatKeys.unreadCount() });
    },
  });
};

export const useMarkAsRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.unreadCount() });
    },
  });
};

export const useCreateConversation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
    },
  });
};
```

---

## Part 3: Chat Components

### 3.1 Message Bubble with Animation

```javascript
const MessageBubble = ({ message, isOwn }) => (
  <motion.div
    initial={{ opacity: 0, y: 10, scale: 0.95 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    className={`chat-bubble ${isOwn ? 'chat-bubble-sent' : 'chat-bubble-received'}`}
  >
    <p>{message.content}</p>
    <div className={`flex items-center gap-2 mt-1 text-xs ${isOwn ? 'text-primary-200' : 'text-white/40'}`}>
      <span>{formatTime(message.created_at)}</span>
      {isOwn && (
        <span>{message.status === 'read' ? '✓✓' : message.status === 'delivered' ? '✓✓' : '✓'}</span>
      )}
    </div>
  </motion.div>
);
```

### 3.2 Typing Indicator

```javascript
const TypingIndicator = () => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="chat-bubble chat-bubble-received flex gap-1 p-3"
  >
    {[0, 1, 2].map((i) => (
      <motion.div
        key={i}
        animate={{ y: [0, -5, 0] }}
        transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.1 }}
        className="w-2 h-2 rounded-full bg-white/40"
      />
    ))}
  </motion.div>
);
```

### 3.3 Chat Window

```javascript
export const ChatWindow = ({ conversationId }) => {
  const { data: messages, isLoading } = useMessages(conversationId);
  const { mutate: sendMessage } = useSendMessage();
  const [input, setInput] = useState('');
  
  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage({ conversationId, data: { content: input } });
    setInput('');
  };
  
  return (
    <div className="flex flex-col h-[600px] glass-card">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages?.map((msg) => (
          <MessageBubble key={msg.id} message={msg} isOwn={msg.is_own} />
        ))}
      </div>
      
      {/* Input */}
      <div className="p-4 border-t border-white/10">
        <div className="flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type a message..."
            className="chat-input-glass"
          />
          <button onClick={handleSend} className="glass-button">
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query | 3 query hooks + 3 mutations with optimistic updates |
| Real-time | Polling + refetchInterval |
| Components | Message bubbles, typing indicator, chat window |
| Status | Read receipts, sending states |

---

*Last Updated: 2026-03-29*
