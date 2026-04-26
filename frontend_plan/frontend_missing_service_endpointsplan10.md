# Implementation Plan - Frontend Missing Services Plan 10: Exam Section Module API Integration

This plan details the comprehensive API integration for the Exam Section Module with exam management, results, and grade sheets.

---

## Part 1: Design System

```javascript
// Exam Glass Components
.exam-card {
  @apply bg-gradient-to-br from-blue-900/30 to-slate-900/30 backdrop-blur-xl 
         border border-white/10 rounded-2xl overflow-hidden;
}

.exam-status {
  @apply px-3 py-1 rounded-full text-xs font-medium;
}

.status-draft { @apply bg-white/10 text-white/60; }
.status-published { @apply bg-emerald-500/20 text-emerald-400; }
.status-scheduled { @apply bg-amber-500/20 text-amber-400; }

.grade-badge {
  @apply px-2 py-1 rounded-lg text-sm font-bold;
}

.grade-a { @apply bg-emerald-500/20 text-emerald-400; }
.grade-b { @apply bg-blue-500/20 text-blue-400; }
.grade-c { @apply bg-amber-500/20 text-amber-400; }
.grade-d { @apply bg-red-500/20 text-red-400; }
```

---

## Part 2: TanStack Query Hooks

```javascript
// frontend/src/modules/school/school_exam_section/hooks/useExam.js

export const examKeys = {
  all: ['exam'] as const,
  list: () => [...examKeys.all, 'list'] as const,
  byId: (id) => [...examKeys.all, 'list', id] as const,
  results: () => [...examKeys.all, 'results'] as const,
  resultsByExam: (examId) => [...examKeys.all, 'results', examId] as const,
  gradeSheets: () => [...examKeys.all, 'gradeSheets'] as const,
  gradeAnalytics: (examId) => [...examKeys.all, 'analytics', examId] as const,
};

export const useAllExams = (params) => useQuery({
  queryKey: [...examKeys.list(), params],
  queryFn: () => api.getAllExams(params),
});

export const useExamById = (id) => useQuery({
  queryKey: examKeys.byId(id),
  queryFn: () => api.getExamById(id),
  enabled: !!id,
});

export const useAllResults = (params) => useQuery({
  queryKey: [...examKeys.results(), params],
  queryFn: () => api.getAllResults(params),
});

export const useExamResults = (examId) => useQuery({
  queryKey: examKeys.resultsByExam(examId),
  queryFn: () => api.getExamResults(examId),
  enabled: !!examId,
});

export const useStudentResults = (studentId) => useQuery({
  queryKey: [...examKeys.results(), 'student', studentId],
  queryFn: () => api.getStudentResults(studentId),
  enabled: !!studentId,
});

export const useGradeSheets = (params) => useQuery({
  queryKey: [...examKeys.gradeSheets(), params],
  queryFn: () => api.getGradeSheets(params),
});

export const useGradeAnalytics = (examId) => useQuery({
  queryKey: examKeys.gradeAnalytics(examId),
  queryFn: () => api.getGradeAnalytics(examId),
  enabled: !!examId,
});

// Mutations
export const useCreateExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createExam,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: examKeys.list() }),
  });
};

export const usePublishExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.publishExam,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: examKeys.list() }),
  });
};

export const useCreateResult = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createResult,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: examKeys.results() }),
  });
};

export const useBulkCreateResults = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.bulkCreateResults,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: examKeys.results() }),
  });
};

export const usePublishResults = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.publishResults,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: examKeys.results() }),
  });
};

export const useGenerateGradeSheet = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.generateGradeSheet,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: examKeys.gradeSheets() }),
  });
};
```

---

## Part 3: Components

### 3.1 Exam Card

```javascript
const ExamCard = ({ exam }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="exam-card"
  >
    <div className="p-4">
      <div className="flex justify-between items-start mb-3">
        <h4 className="text-white font-semibold">{exam.title}</h4>
        <span className={`exam-status ${
          exam.status === 'published' ? 'status-published' :
          exam.status === 'scheduled' ? 'status-scheduled' : 'status-draft'
        }`}>
          {exam.status}
        </span>
      </div>
      <div className="flex gap-4 text-white/60 text-sm">
        <span>📅 {exam.date}</span>
        <span>⏰ {exam.duration}</span>
      </div>
    </div>
  </motion.div>
);
```

### 3.2 Results Table with Grade Badges

```javascript
const ResultsTable = ({ results }) => (
  <div className="glass-card overflow-hidden">
    <table className="w-full">
      <thead className="bg-white/5">
        <tr>
          <th className="text-left text-white/60 p-4">Student</th>
          <th className="text-left text-white/60 p-4">Subject</th>
          <th className="text-left text-white/60 p-4">Score</th>
          <th className="text-left text-white/60 p-4">Grade</th>
          <th className="text-left text-white/60 p-4">Status</th>
        </tr>
      </thead>
      <tbody>
        {results?.map((result, index) => (
          <motion.tr
            key={result.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className="border-t border-white/5"
          >
            <td className="p-4 text-white">{result.studentName}</td>
            <td className="p-4 text-white/60">{result.subject}</td>
            <td className="p-4 text-white">{result.score}/{result.maxScore}</td>
            <td className="p-4">
              <span className={`grade-badge ${
                result.grade === 'A' ? 'grade-a' :
                result.grade === 'B' ? 'grade-b' :
                result.grade === 'C' ? 'grade-c' : 'grade-d'
              }`}>
                {result.grade}
              </span>
            </td>
            <td className="p-4">
              <span className={`text-xs ${result.published ? 'text-emerald-400' : 'text-amber-400'}`}>
                {result.published ? 'Published' : 'Draft'}
              </span>
            </td>
          </motion.tr>
        ))}
      </tbody>
    </table>
  </div>
);
```

### 3.3 Grade Distribution Chart

```javascript
const GradeDistributionChart = ({ analytics }) => {
  const grades = ['A', 'B', 'C', 'D', 'F'];
  const maxCount = Math.max(...Object.values(analytics?.distribution || {}));
  
  return (
    <div className="glass-card p-6">
      <h3 className="text-white font-semibold mb-4">Grade Distribution</h3>
      <div className="flex items-end gap-3 h-40">
        {grades.map((grade) => {
          const count = analytics?.distribution?.[grade] || 0;
          const height = maxCount > 0 ? (count / maxCount) * 100 : 0;
          
          return (
            <div key={grade} className="flex-1 flex flex-col items-center">
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: `${height}%` }}
                className={`w-full rounded-t-lg ${
                  grade === 'A' ? 'bg-emerald-500' :
                  grade === 'B' ? 'bg-blue-500' :
                  grade === 'C' ? 'bg-amber-500' :
                  grade === 'D' ? 'bg-orange-500' : 'bg-red-500'
                }`}
              />
              <span className="text-white/60 text-sm mt-2">{grade}</span>
              <span className="text-white/40 text-xs">{count}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
```

---

## Summary

| Feature | Implementation |
|---------|----------------|
| TanStack Query | 7 query hooks + 6 mutations |
| Exam Cards | Status badges with animations |
| Results Table | Grade badges, published status |
| Grade Analytics | Distribution chart with animations |

---

*Last Updated: 2026-03-29*
