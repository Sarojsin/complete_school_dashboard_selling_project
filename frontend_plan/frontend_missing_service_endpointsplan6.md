# Implementation Plan - Frontend Missing Services Plan 6: Library Module API Integration

This plan details the comprehensive API integration for the Library Module with book management, issue/return tracking, and overdue notifications.

---

## Part 1: Design System

```javascript
// Library Glass Components
.book-card {
  @apply bg-gradient-to-br from-amber-900/30 to-slate-900/30 backdrop-blur-xl 
         border border-white/10 rounded-2xl p-4 hover:border-amber-500/30 transition-all;
}

.due-counter {
  @apply px-3 py-1 rounded-full text-sm font-medium;
}

.due-safe { @apply bg-emerald-500/20 text-emerald-400; }
.due-warning { @apply bg-amber-500/20 text-amber-400; }
.due-danger { @apply bg-red-500/20 text-red-400; }
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_library/hooks/useLibrary.js

export const libraryKeys = {
  all: ['library'] as const,
  books: () => [...libraryKeys.all, 'books'] as const,
  bookById: (id) => [...libraryKeys.all, 'books', id] as const,
  issued: () => [...libraryKeys.all, 'issued'] as const,
  myIssued: () => [...libraryKeys.all, 'issued', 'mine'] as const,
  overdue: () => [...libraryKeys.all, 'overdue'] as const,
  stats: () => [...libraryKeys.all, 'stats'] as const,
};

export const useAllBooks = (params) => useQuery({
  queryKey: [...libraryKeys.books(), params],
  queryFn: () => api.getAllBooks(params),
});

export const useIssuedBooks = (params) => useQuery({
  queryKey: [...libraryKeys.issued(), params],
  queryFn: () => api.getIssuedBooks(params),
});

export const useMyIssuedBooks = () => useQuery({
  queryKey: libraryKeys.myIssued(),
  queryFn: api.getMyIssuedBooks,
});

export const useOverdueBooks = () => useQuery({
  queryKey: libraryKeys.overdue(),
  queryFn: api.getOverdueBooks,
});

export const useLibraryStats = () => useQuery({
  queryKey: libraryKeys.stats(),
  queryFn: api.getLibraryStats,
});

// Mutations
export const useIssueBook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.issueBook,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: libraryKeys.books() });
      queryClient.invalidateQueries({ queryKey: libraryKeys.issued() });
    },
  });
};

export const useReturnBook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.returnBook,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: libraryKeys.issued() });
      queryClient.invalidateQueries({ queryKey: libraryKeys.myIssued() });
    },
  });
};

export const useRenewBook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.renewBook,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: libraryKeys.myIssued() });
    },
  });
};
```

---

## Part 3: Library Components

```javascript
// Book Card with Due Counter
const BookCard = ({ book }) => {
  const daysLeft = book.dueDate ? Math.ceil((new Date(book.dueDate) - new Date()) / (1000*60*60*24)) : null;
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="book-card"
    >
      <div className="h-32 bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-xl mb-3 flex items-center justify-center">
        <BookOpen className="w-12 h-12 text-amber-400" />
      </div>
      <h4 className="text-white font-medium truncate">{book.title}</h4>
      <p className="text-white/50 text-sm">{book.author}</p>
      {book.status === 'issued' && (
        <span className={`due-counter mt-2 inline-block ${
          daysLeft > 7 ? 'due-safe' : daysLeft > 3 ? 'due-warning' : 'due-danger'
        }`}>
          {daysLeft} days left
        </span>
      )}
    </motion.div>
  );
};

// Issue/Return Form
const IssueBookForm = () => {
  const { mutate: issueBook } = useIssueBook();
  
  return (
    <div className="glass-card p-6">
      <h3 className="text-white font-semibold mb-4">Issue Book</h3>
      {/* Form fields */}
    </div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query | 5 query hooks + 3 mutations |
| Book Cards | Due date counters with color coding |
| Issue/Return | Optimistic updates |

---

*Last Updated: 2026-03-29*
