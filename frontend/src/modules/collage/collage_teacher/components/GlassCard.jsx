import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', padding = 'p-6', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3, delay }}
    className={`bg-gradient-to-br from-violet-900/30 to-slate-900/30 backdrop-blur-xl border border-white/10 rounded-2xl ${className}`}>
    <div className={padding}>{children}</div>
  </motion.div>
);

export const CourseCard = ({ course, onTakeAttendance, onSubmitGrades }) => (
  <GlassCard>
    <div className="flex justify-between items-start mb-2">
      <div><h4 className="text-white font-medium">{course.name}</h4><p className="text-white/60 text-sm">{course.code} • {course.students} students</p></div>
    </div>
    <div className="flex gap-2 mt-4">
      <button onClick={() => onTakeAttendance(course.id)} className="flex-1 py-2 bg-violet-500/20 text-violet-400 rounded-lg text-sm">Attendance</button>
      <button onClick={() => onSubmitGrades(course.id)} className="flex-1 py-2 bg-violet-500/20 text-violet-400 rounded-lg text-sm">Grades</button>
    </div>
  </GlassCard>
);

export default GlassCard;
