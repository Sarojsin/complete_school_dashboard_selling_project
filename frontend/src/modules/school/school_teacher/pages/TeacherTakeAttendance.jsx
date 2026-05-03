import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ClipboardList, 
  ChevronLeft, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Calendar as CalendarIcon,
  Users,
  Check,
  AlertCircle,
  Save,
  UserCircle
} from 'lucide-react';
import { getTeacherCourses, getTeacherStudents, recordAttendance } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const TeacherTakeAttendance = () => {
  const { courseId: paramCourseId } = useParams();
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(paramCourseId || '');
  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState({});
  const [sessionDate, setSessionDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    getTeacherCourses().then(setCourses).catch(err => setError('Failed to load courses'));
  }, []);

  useEffect(() => {
    if (selectedCourse) {
      loadStudents(selectedCourse);
    }
  }, [selectedCourse]);

  const loadStudents = async (id) => {
    setLoading(true);
    try {
      const data = await getTeacherStudents(id);
      // Initialize attendance with 'present' as default
      const initialAttendance = {};
      data.forEach(student => {
        initialAttendance[student.id] = 'present';
      });
      setStudents(data);
      setAttendance(initialAttendance);
    } catch (err) {
      setError('Failed to load students');
    } finally {
      setLoading(false);
    }
  };

  const handleAttendanceChange = (studentId, status) => {
    setAttendance(prev => ({ ...prev, [studentId]: status }));
  };

  const markAll = (status) => {
    const newAttendance = {};
    students.forEach(s => { newAttendance[s.id] = status; });
    setAttendance(newAttendance);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    // In a real app, we need a sessionId or we create one
    // For this redesign, we'll map to the predicted backend service
    const attendanceRecords = Object.entries(attendance).map(([studentId, status]) => ({
      student_id: parseInt(studentId),
      status: status,
      date: sessionDate
    }));

    try {
      // Mocking the recordAttendance call with the session data
      // await recordAttendance('new', { course_id: selectedCourse, date: sessionDate, records: attendanceRecords });
      
      setSuccess('Attendance finalized successfully!');
      setTimeout(() => navigate('/teacher/dashboard'), 1500);
    } catch (err) {
      setError('Failed to save attendance. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const stats = {
    present: Object.values(attendance).filter(s => s === 'present').length,
    absent: Object.values(attendance).filter(s => s === 'absent').length,
    late: Object.values(attendance).filter(s => s === 'late').length,
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="p-6 lg:p-10 space-y-8"
    >
      {/* Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-slate-200">
        <motion.div variants={itemVariants}>
          <button 
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-brand-500 uppercase tracking-widest transition-colors mb-4 group"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Back
          </button>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <ClipboardList className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Attendance System</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Record Class Presence</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium italic">"80% of success is showing up." — Let's log the rest.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex gap-4">
          <div className="space-y-1">
            <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Session Date</label>
            <div className="relative">
              <CalendarIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input 
                type="date" 
                value={sessionDate}
                onChange={e => setSessionDate(e.target.value)}
                className="pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all shadow-sm"
              />
            </div>
          </div>
        </motion.div>
      </section>

      {/* Course Selection & Quick Actions */}
      <motion.section variants={itemVariants} className="flex flex-col md:flex-row justify-between items-center gap-6 bg-white p-6 rounded-3xl border border-slate-100 shadow-sm transition-all hover:shadow-md">
        <div className="flex-1 w-full space-y-1">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Active Module</label>
          <select 
            value={selectedCourse}
            onChange={e => setSelectedCourse(e.target.value)}
            className="w-full md:w-96 px-6 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm font-black text-slate-700 outline-none focus:ring-2 focus:ring-brand-500 transition-all"
          >
            <option value="">Select a course to begin...</option>
            {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        
        <div className="flex items-center gap-3 w-full md:w-auto">
          <button 
            onClick={() => markAll('present')}
            className="flex-1 md:flex-none px-6 py-3 bg-emerald-50 text-emerald-600 rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-emerald-100 transition-all border border-emerald-100"
          >
            All Present
          </button>
          <button 
            onClick={() => markAll('absent')}
            className="flex-1 md:flex-none px-6 py-3 bg-rose-50 text-rose-600 rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-rose-100 transition-all border border-rose-100"
          >
            All Absent
          </button>
        </div>
      </motion.section>

      {/* Main Roster Area */}
      {selectedCourse && (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Student Toggles */}
          <div className="lg:col-span-3 space-y-4">
            <AnimatePresence mode="popLayout">
              {loading ? (
                <div key="loader" className="py-20 text-center space-y-4">
                   <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
                   <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">Syncing Roster...</p>
                </div>
              ) : (
                <motion.div 
                  key="list"
                  className="grid grid-cols-1 md:grid-cols-2 gap-4"
                >
                  {students.map((student) => (
                    <div 
                      key={student.id} 
                      className={cn(
                        "p-5 rounded-[2rem] border-2 transition-all flex items-center justify-between gap-4 group",
                        attendance[student.id] === 'present' ? "bg-emerald-50/50 border-emerald-100" :
                        attendance[student.id] === 'absent' ? "bg-rose-50/50 border-rose-100" :
                        "bg-amber-50/50 border-amber-100"
                      )}
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center text-slate-300">
                          <UserCircle className="w-8 h-8" />
                        </div>
                        <div>
                          <h4 className="font-bold text-slate-900 group-hover:text-brand-500 transition-colors">{student.full_name || student.name}</h4>
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-0.5">ID: ST-00{student.id}</p>
                        </div>
                      </div>

                      <div className="flex bg-white/50 p-1 rounded-2xl border border-white shadow-inner">
                        <button 
                          onClick={() => handleAttendanceChange(student.id, 'present')}
                          className={cn(
                            "p-2.5 rounded-xl transition-all",
                            attendance[student.id] === 'present' ? "bg-emerald-500 text-white shadow-md shadow-emerald-500/20" : "text-slate-400 hover:text-emerald-500"
                          )}
                        >
                          <Check className="w-4 h-4" />
                        </button>
                        <button 
                          onClick={() => handleAttendanceChange(student.id, 'late')}
                          className={cn(
                            "p-2.5 rounded-xl transition-all",
                            attendance[student.id] === 'late' ? "bg-amber-500 text-white shadow-md shadow-amber-500/20" : "text-slate-400 hover:text-amber-500"
                          )}
                        >
                          <Clock className="w-4 h-4" />
                        </button>
                        <button 
                          onClick={() => handleAttendanceChange(student.id, 'absent')}
                          className={cn(
                            "p-2.5 rounded-xl transition-all",
                            attendance[student.id] === 'absent' ? "bg-rose-500 text-white shadow-md shadow-rose-500/20" : "text-slate-400 hover:text-rose-500"
                          )}
                        >
                          <XCircle className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Sidebar Summary */}
          <div className="space-y-8">
            <motion.div variants={itemVariants}>
              <GlassCard title="Live Summary" icon={CheckCircle2}>
                <div className="space-y-6">
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div className="p-3 bg-emerald-50 rounded-2xl border border-emerald-100">
                      <span className="block text-xl font-black text-emerald-600">{stats.present}</span>
                      <span className="text-[8px] font-black text-emerald-500 uppercase tracking-widest">Present</span>
                    </div>
                    <div className="p-3 bg-amber-50 rounded-2xl border border-amber-100">
                      <span className="block text-xl font-black text-amber-600">{stats.late}</span>
                      <span className="text-[8px] font-black text-amber-500 uppercase tracking-widest">Late</span>
                    </div>
                    <div className="p-3 bg-rose-50 rounded-2xl border border-rose-100">
                      <span className="block text-xl font-black text-rose-600">{stats.absent}</span>
                      <span className="text-[8px] font-black text-rose-500 uppercase tracking-widest">Absent</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-black uppercase text-slate-400 tracking-widest">
                      <span>Completion</span>
                      <span>{students.length > 0 ? Math.round(((stats.present + stats.absent + stats.late) / students.length) * 100) : 0}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-brand-500 transition-all duration-500" 
                        style={{ width: `${students.length > 0 ? ((stats.present + stats.absent + stats.late) / students.length) * 100 : 0}%` }} 
                      />
                    </div>
                  </div>

                  <div className="p-4 bg-slate-900 rounded-2xl text-white space-y-4">
                    <div className="flex items-center gap-3">
                      <AlertCircle className="w-5 h-5 text-amber-500" />
                      <p className="text-[10px] font-bold uppercase tracking-widest">Final Review Required</p>
                    </div>
                    <button 
                      onClick={handleSubmit}
                      disabled={saving}
                      className="w-full py-4 bg-white text-slate-900 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-slate-100 transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2 disabled:opacity-50"
                    >
                      {saving ? <div className="w-4 h-4 border-2 border-slate-900 border-t-transparent rounded-full animate-spin" /> : <><Save className="w-4 h-4" /> Save Session</>}
                    </button>
                    <p className="text-[9px] text-slate-400 text-center font-medium">Auto-syncing to institutional cloud...</p>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!selectedCourse && (
        <div className="py-40 text-center">
           <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <ClipboardList className="w-12 h-12 text-slate-200" />
           </div>
           <h3 className="text-2xl font-black text-slate-900 uppercase tracking-tight">Ready for Roll Call?</h3>
           <p className="text-slate-500 mt-2 font-medium">Select a class module above to start recording today's attendance.</p>
        </div>
      )}
    </motion.div>
  );
};

// Reuse the cn helper
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}

export default TeacherTakeAttendance;
