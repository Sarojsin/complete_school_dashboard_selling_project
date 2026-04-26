# Implementation Plan - Frontend Missing Services Plan 7: Groups Module API Integration

This plan details the comprehensive API integration for the Groups/Forum Module with social learning features, posts, and comments.

---

## Part 1: Design System

```javascript
// Groups Glass Components
.group-card {
  @apply bg-gradient-to-br from-emerald-900/30 to-slate-900/30 backdrop-blur-xl 
         border border-white/10 rounded-2xl overflow-hidden;
}

.post-card {
  @apply glass-card p-4 mb-4;
}

.post-content {
  @apply text-white/90 leading-relaxed;
}

.like-button {
  @apply flex items-center gap-2 text-white/60 hover:text-red-400 transition-colors;
}

.like-button-liked {
  @apply text-red-400;
}
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_groups/hooks/useGroups.js

export const groupKeys = {
  all: ['groups'] as const,
  list: () => [...groupKeys.all, 'list'] as const,
  byId: (id) => [...groupKeys.all, 'list', id] as const,
  members: (id) => [...groupKeys.all, 'members', id] as const,
  posts: (groupId) => [...groupKeys.all, 'posts', groupId] as const,
  postById: (postId) => [...groupKeys.all, 'posts', 'single', postId] as const,
  comments: (postId) => [...groupKeys.all, 'comments', postId] as const,
};

export const useAllGroups = (params) => useQuery({
  queryKey: [...groupKeys.list(), params],
  queryFn: () => api.getAllGroups(params),
});

export const useGroupById = (groupId) => useQuery({
  queryKey: groupKeys.byId(groupId),
  queryFn: () => api.getGroupById(groupId),
  enabled: !!groupId,
});

export const useGroupMembers = (groupId) => useQuery({
  queryKey: groupKeys.members(groupId),
  queryFn: () => api.getGroupMembers(groupId),
  enabled: !!groupId,
});

export const useGroupPosts = (groupId) => useQuery({
  queryKey: groupKeys.posts(groupId),
  queryFn: () => api.getGroupPosts(groupId),
  enabled: !!groupId,
});

export const usePostComments = (postId) => useQuery({
  queryKey: groupKeys.comments(postId),
  queryFn: () => api.getPostComments(postId),
  enabled: !!postId,
});

// Mutations
export const useCreateGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createGroup,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: groupKeys.list() }),
  });
};

export const useJoinGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.joinGroup,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: groupKeys.list() }),
  });
};

export const useCreatePost = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, data }) => api.createPost(groupId, data),
    onSuccess: (_, { groupId }) => queryClient.invalidateQueries({ queryKey: groupKeys.posts(groupId) }),
  });
};

export const useLikePost = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.likePost,
    onMutate: async (postId) => {
      await queryClient.cancelQueries({ queryKey: groupKeys.posts });
      const previous = queryClient.getQueryData(groupKeys.posts);
      
      queryClient.setQueryData(groupKeys.posts, (old = []) => 
        old.map(p => p.id === postId ? { ...p, liked: !p.liked, likes: p.liked ? p.likes - 1 : p.likes + 1 } : p)
      );
      
      return { previous };
    },
    onError: (err, postId, context) => {
      queryClient.setQueryData(groupKeys.posts, context?.previous);
    },
  });
};

export const useAddComment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ postId, data }) => api.addComment(postId, data),
    onSuccess: (_, { postId }) => queryClient.invalidateQueries({ queryKey: groupKeys.comments(postId) }),
  });
};
```

---

## Part 3: Components

```javascript
// Group Post with Like Animation
const GroupPost = ({ post }) => {
  const { mutate: likePost } = useLikePost();
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="post-card"
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500" />
        <div>
          <p className="text-white font-medium">{post.author}</p>
          <p className="text-white/40 text-xs">{post.created_at}</p>
        </div>
      </div>
      
      <p className="post-content mb-4">{post.content}</p>
      
      {post.attachments?.length > 0 && (
        <div className="mb-4 rounded-xl overflow-hidden">
          <img src={post.attachments[0]} alt="attachment" className="w-full" />
        </div>
      )}
      
      <div className="flex items-center gap-4 pt-3 border-t border-white/10">
        <button 
          onClick={() => likePost(post.id)}
          className={`like-button ${post.liked ? 'like-button-liked' : ''}`}
        >
          <Heart className={`w-5 h-5 ${post.liked ? 'fill-current' : ''}`} />
          <span>{post.likes || 0}</span>
        </button>
        <button className="like-button">
          <MessageCircle className="w-5 h-5" />
          <span>{post.comments || 0}</span>
        </button>
      </div>
    </motion.div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query | 5 query hooks + 5 mutations |
| Optimistic Updates | Like button with instant feedback |
| Components | Group cards, posts, comments |

---

*Last Updated: 2026-03-29*
