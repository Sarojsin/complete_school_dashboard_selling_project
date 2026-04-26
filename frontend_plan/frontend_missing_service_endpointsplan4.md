# Implementation Plan - Frontend Missing Services Plan 4: Parent Module API Integration

This plan details the comprehensive API integration for the Parent Portal with premium glassmorphic design, featuring multi-child monitoring and real-time alerts.

---

## Part 1: Design System (Parent)

```javascript
// Parent Module Tailwind Extension
module.exports = {
  theme: {
    extend: {
      colors: {
        parent: {
          primary: '#8b5cf6',  // Violet
          success: '#10b981',
          warning: '#f59e0b',
        }
      }
    }
  }
}

// Parent Glass Components
.parent-glass-card {
  @apply bg-gradient-to-br from-violet-900/40 to-slate-900/40 backdrop-blur-xl 
         border border-white/10 shadow-2xl rounded-2xl;
}

.child-avatar {
  @apply w-16 h-16 rounded-full bg-gradient-to-br from-parent-primary to-purple-400 
         flex items-center justify-center text-white text-xl font-bold ring-4 ring-white/10;
}
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_parent/hooks/useParent.js

export const parentKeys = {
  all: ['parent'] as const,
  children: () => [...parentKeys.all, 'children'] as const,
  childById: (id) => [...parentKeys.all, 'children', id] as const,
  childProfile: (id) => [...parentKeys.all, 'children', id, 'profile'] as const,
  childCourses: (id) => [...parentKeys.all, 'children', id, 'courses'] as const,
  childGrades: (id) => [...parentKeys.all, 'children', id, 'grades'] as const,
  childAttendance: (id) => [...parentKeys.all, 'children', id, 'attendance'] as const,
  childAssignments: (id) => [...parentKeys.all, 'children', id, 'assignments'] as const,
  childFees: (id) => [...parentKeys.all, 'children', id, 'fees'] as const,
  notices: () => [...parentKeys.all, 'notices'] as const,
  messages: () => [...parentKeys.all, 'messages'] as const,
};

// Query Hooks
export const useLinkedChildren = () => useQuery({
  queryKey: parentKeys.children(),
  queryFn: api.getLinkedChildren,
  staleTime: 5 * 60 * 1000,
});

export const useChildById = (childId) => useQuery({
  queryKey: parentKeys.childById(childId),
  queryFn: () => api.getChildById(childId),
  enabled: !!childId,
});

export const useChildGrades = (childId) => useQuery({
  queryKey: parentKeys.childGrades(childId),
  queryFn: () => api.getChildGrades(childId),
  enabled: !!childId,
});

export const useChildAttendance = (childId) => useQuery({
  queryKey: parentKeys.childAttendance(childId),
  queryFn: () => api.getChildAttendance(childId),
  enabled: !!childId,
});

export const useChildFees = (childId) => useQuery({
  queryKey: parentKeys.childFees(childId),
  queryFn: () => api.getChildFees(childId),
  enabled: !!childId,
});

export const useParentNotices = () => useQuery({
  queryKey: parentKeys.notices(),
  queryFn: api.getNotices,
  staleTime: 5 * 60 * 1000,
});

export const useParentMessages = () => useQuery({
  queryKey: parentKeys.messages(),
  queryFn: api.getMessages,
  staleTime: 1 * 60 * 1000, // More frequent for chat
});

// Mutations
export const useSendMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.sendMessage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: parentKeys.messages() });
    },
  });
};
```

---

## Part 3: Components

### 3.1 Child Selector

```javascript
// Child Selector Component
export const ChildSelector = ({ children, selectedChild, onSelect }) => (
  <div className="flex gap-4 overflow-x-auto pb-4">
    {children.map((child) => (
      <motion.button
        key={child.id}
        onClick={() => onSelect(child.id)}
        className={`flex-shrink-0 p-4 rounded-2xl transition-all ${
          selectedChild === child.id
            ? 'bg-parent-primary/30 border-2 border-parent-primary'
            : 'bg-white/5 border-2 border-white/10 hover:border-white/20'
        }`}
      >
        <div className="child-avatar mb-2">{child.name.charAt(0)}</div>
        <p className="text-white text-sm font-medium">{child.name}</p>
        <p className="text-white/40 text-xs">{child.grade}</p>
      </motion.button>
    ))}
  </div>
);
```

### 3.2 Parent Dashboard with Child Stats

```javascript
export const ParentDashboard = () => {
  const { data: children } = useLinkedChildren();
  const [selectedChild, setSelectedChild] = useState(children?.[0]?.id);
  const { data: grades } = useChildGrades(selectedChild);
  const { data: attendance } = useChildAttendance(selectedChild);
  
  return (
    <div className="space-y-6 p-6">
      {/* Child Selector */}
      <ChildSelector 
        children={children || []} 
        selectedChild={selectedChild}
        onSelect={setSelectedChild}
      />
      
      {/* Quick Stats */}
      <div className="grid grid-cols-3 gap-4">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="parent-glass-card p-6 text-center"
        >
          <p className="text-white/60 text-sm">GPA</p>
          <p className="text-3xl font-bold text-white">{grades?.gpa || '-'}</p>
        </motion.div>
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="parent-glass-card p-6 text-center"
        >
          <p className="text-white/60 text-sm">Attendance</p>
          <p className="text-3xl font-bold text-white">{attendance?.percentage || 0}%</p>
        </motion.div>
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="parent-glass-card p-6 text-center"
        >
          <p className="text-white/60 text-sm">Pending Fees</p>
          <p className="text-3xl font-bold text-white">${children?.[0]?.pendingFees || 0}</p>
        </motion.div>
      </div>
      
      {/* Recent Activity */}
      <div className="parent-glass-card p-6">
        <h3 className="text-white font-semibold mb-4">Recent Activity</h3>
        {/* Activity timeline */}
      </div>
    </div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query Hooks | 8 query hooks + 1 mutation |
| Child Selector | Multi-child switching with animations |
| Parent Dashboard | Quick stats, activity timeline |

---

*Last Updated: 2026-03-29*
