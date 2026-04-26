# Implementation Plan - Frontend Missing Services Plan 9: Timetable Module API Integration

This plan details the comprehensive API integration for the Timetable Module with weekly grid views and conflict detection.

---

## Part 1: Design System

```javascript
// Timetable Glass Components
.timetable-grid {
  @apply grid grid-cols-8 gap-2;
}

.time-slot {
  @apply p-3 rounded-xl bg-white/5 border border-white/10 text-center 
         hover:bg-white/10 transition-colors cursor-pointer;
}

.time-slot-filled {
  @apply bg-gradient-to-br from-primary-500/30 to-primary-600/20 border-primary-500/30;
}

.time-slot-current {
  @apply ring-2 ring-primary-500 shadow-glow-blue;
}

.timetable-cell {
  @apply min-h-[80px] p-2 rounded-lg border border-white/5;
}
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_timetable/hooks/useTimetable.js

export const timetableKeys = {
  all: ['timetable'] as const,
  student: () => [...timetableKeys.all, 'student'] as const,
  teacher: () => [...timetableKeys.all, 'teacher'] as const,
  entries: () => [...timetableKeys.all, 'entries'] as const,
  entriesByCourse: (courseId) => [...timetableKeys.all, 'entries', courseId] as const,
  rooms: () => [...timetableKeys.all, 'rooms'] as const,
};

export const useStudentTimetable = (params) => useQuery({
  queryKey: [...timetableKeys.student(), params],
  queryFn: () => api.getMyTimetable(params),
});

export const useTeacherTimetable = (params) => useQuery({
  queryKey: [...timetableKeys.teacher(), params],
  queryFn: () => api.getMyTeacherTimetable(params),
});

export const useTimetableEntries = (params) => useQuery({
  queryKey: [...timetableKeys.entries(), params],
  queryFn: () => api.getTimetableEntries(params),
});

export const useRooms = () => useQuery({
  queryKey: timetableKeys.rooms(),
  queryFn: api.getRooms,
});

export const useRoomAvailability = (roomId, params) => useQuery({
  queryKey: [...timetableKeys.rooms(), roomId],
  queryFn: () => api.getRoomAvailability(roomId, params),
  enabled: !!roomId,
});

// Mutations
export const useCreateTimetableEntry = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createTimetableEntry,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: timetableKeys.entries() }),
  });
};

export const useBulkCreateTimetable = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkCreateTimetable,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: timetableKeys.entries() }),
  });
};

export const useCheckRoomConflict = () => {
  return useMutation({
    mutationFn: api.checkRoomConflict,
  });
};
```

---

## Part 3: Components

```javascript
// Weekly Timetable Grid
const WeeklyTimetable = ({ schedule, onSlotClick }) => {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const hours = Array.from({ length: 9 }, (_, i) => i + 8); // 8 AM to 4 PM
  
  return (
    <div className="overflow-x-auto">
      <div className="timetable-grid">
        {/* Header Row */}
        <div className="text-white/40 text-sm font-medium p-2"></div>
        {days.map((day) => (
          <div key={day} className="text-white/60 text-sm font-medium p-2 text-center">
            {day}
          </div>
        ))}
        
        {/* Time Slots */}
        {hours.map((hour) => (
          <React.Fragment key={hour}>
            <div className="text-white/40 text-xs p-2">{hour}:00</div>
            {days.map((day) => {
              const classItem = schedule?.find(s => s.day === day && s.hour === hour);
              return (
                <motion.div
                  key={`${day}-${hour}`}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className={`timetable-cell ${classItem ? 'time-slot-filled' : 'time-slot'}`}
                  onClick={() => onSlotClick?.(day, hour)}
                >
                  {classItem && (
                    <div className="text-white text-xs font-medium">
                      {classItem.course}
                    </div>
                  )}
                </motion.div>
              );
            })}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

// Current Period Highlight
const CurrentPeriod = ({ classItem, isLive }) => (
  isLive && (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="time-slot-current p-4 bg-gradient-to-br from-primary-500/40 to-purple-500/40 rounded-xl"
    >
      <p className="text-white font-bold">{classItem.course}</p>
      <p className="text-primary-200 text-sm">{classItem.room}</p>
      <div className="flex items-center gap-2 mt-2">
        <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        <span className="text-white/60 text-xs">Live Now</span>
      </div>
    </motion.div>
  )
);
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query | 5 query hooks + 3 mutations |
| Timetable Grid | Weekly view with day/hour slots |
| Current Period | Live indicator with animation |
| Conflict Detection | Room availability checking |

---

*Last Updated: 2026-03-29*
