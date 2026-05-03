import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, 
  Upload, 
  Plus, 
  Trash2, 
  Eye, 
  Download, 
  BookOpen, 
  Search, 
  Filter, 
  X,
  FilePlus,
  ChevronRight,
  ShieldCheck,
  AlertCircle
} from 'lucide-react';
import { getTeacherCourses, getTeacherNotes, uploadNote, deleteNote } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const TeacherUploadNotes = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [existingNotes, setExistingNotes] = useState([]);
  const [loadingNotes, setLoadingNotes] = useState(true);
  const [showUploadModal, setShowUploadModal] = useState(false);

  useEffect(() => {
    loadCourses();
    loadExistingNotes();
  }, []);

  const loadCourses = async () => {
    try {
      const data = await getTeacherCourses();
      setCourses(data);
    } catch (err) {
      setError('Failed to load courses');
    }
  };

  const loadExistingNotes = async () => {
    setLoadingNotes(true);
    try {
      const data = await getTeacherNotes();
      setExistingNotes(data);
    } catch (err) {
      setError('Failed to load existing notes');
    } finally {
      setLoadingNotes(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > 50 * 1024 * 1024) {
        setError('File size must be less than 50MB');
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('course_id', selectedCourse);
    formData.append('file', file);

    try {
      await uploadNote(formData);
      setSuccess('Resources updated successfully!');
      setTitle('');
      setDescription('');
      setFile(null);
      setShowUploadModal(false);
      loadExistingNotes();
    } catch (err) {
      setError('Failed to process upload. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (noteId) => {
    if (!window.confirm('Archive this resource? This action cannot be undone.')) return;
    try {
      await deleteNote(noteId);
      setExistingNotes(existingNotes.filter(n => n.id !== noteId));
    } catch (err) {
      setError('Failed to delete resource');
    }
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
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-brand-50 rounded-xl">
              <BookOpen className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Resource Center</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Lecture Notes & Handouts</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Distribute academic materials to your classes with one click.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <button 
            onClick={() => setShowUploadModal(true)}
            className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-sm font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 flex items-center gap-2 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            Upload Materials
          </button>
        </motion.div>
      </section>

      {/* Quick Stats */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard icon={FileText} title="Total Resources" value={existingNotes.length} trend="All departments" trendType="neutral" />
        <ModernStatCard icon={Download} title="Monthly Downloads" value="412" trend="↑ 12% Engagement" trendType="positive" />
        <ModernStatCard icon={ShieldCheck} title="Storage Used" value="1.2 GB" trend="of 50GB Limit" trendType="neutral" />
      </motion.section>

      {/* Content Toolbar */}
      <motion.section variants={itemVariants} className="flex flex-col md:flex-row gap-4 items-center">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search by note title or keyword..." 
            className="w-full pl-12 pr-4 py-4 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium text-slate-700 shadow-sm"
          />
        </div>
        <div className="flex items-center gap-2">
          <button className="px-6 py-4 bg-white border border-slate-200 rounded-2xl text-slate-600 font-bold flex items-center gap-2 hover:bg-slate-50 transition-all shadow-sm">
            <Filter className="w-4 h-4" /> All Subjects
          </button>
        </div>
      </motion.section>

      {/* Notes Grid */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loadingNotes ? (
          [1,2,3].map(i => <div key={i} className="h-48 bg-slate-50 rounded-3xl animate-pulse" />)
        ) : existingNotes.length === 0 ? (
          <div className="col-span-full py-20 text-center bg-slate-50/50 rounded-3xl border-2 border-dashed border-slate-200">
            <FileText className="w-12 h-12 text-slate-200 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-slate-900">No materials uploaded yet</h3>
            <p className="text-slate-500 mt-2">Start building your resource academic library today.</p>
          </div>
        ) : (
          existingNotes.map((note) => (
            <motion.div key={note.id} whileHover={{ y: -4 }}>
              <GlassCard noPadding className="h-full flex flex-col group border-transparent hover:border-brand-200">
                <div className="p-6 flex-1 space-y-4">
                  <div className="flex justify-between items-start">
                    <div className="p-3 bg-brand-50 rounded-2xl text-brand-500">
                      <FileText className="w-6 h-6" />
                    </div>
                    <ModernBadge variant="primary" size="sm">{note.course_name?.split(' ')[0] || 'GEN'}</ModernBadge>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-black text-slate-900 group-hover:text-brand-500 transition-colors">{note.title}</h3>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">{note.course_name}</p>
                    {note.description && (
                      <p className="text-sm text-slate-500 font-medium mt-3 line-clamp-2 leading-relaxed">{note.description}</p>
                    )}
                  </div>
                </div>

                <div className="p-4 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between">
                  <div className="flex gap-2">
                    <a 
                      href={note.file_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="p-2.5 bg-white border border-slate-200 text-slate-400 hover:text-brand-500 rounded-xl transition-all shadow-sm"
                    >
                      <Eye className="w-4 h-4" />
                    </a>
                    <button 
                      onClick={() => handleDelete(note.id)}
                      className="p-2.5 bg-white border border-slate-200 text-slate-400 hover:text-rose-500 rounded-xl transition-all shadow-sm"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                  <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                    {new Date(note.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                  </span>
                </div>
              </GlassCard>
            </motion.div>
          ))
        )}
      </motion.section>

      {/* Upload Modal */}
      <AnimatePresence>
        {showUploadModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowUploadModal(false)}
              className="absolute inset-0 bg-slate-900/60 backdrop-blur-md"
            />
            <motion.div 
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              className="relative w-full max-w-xl bg-white rounded-[2.5rem] shadow-2xl overflow-hidden"
            >
              <div className="p-8 border-b border-slate-100 flex justify-between items-center">
                <h3 className="text-2xl font-black text-slate-900 tracking-tight">Post Resources</h3>
                <button onClick={() => setShowUploadModal(false)} className="p-2 hover:bg-slate-100 rounded-xl transition-all">
                  <X className="w-6 h-6 text-slate-400" />
                </button>
              </div>
              
              <form onSubmit={handleSubmit} className="p-10 space-y-8">
                {error && (
                  <div className="p-4 bg-rose-50 border border-rose-100 rounded-2xl flex items-center gap-3 text-rose-600 text-xs font-bold uppercase tracking-wider">
                    <AlertCircle className="w-4 h-4" /> {error}
                  </div>
                )}

                <div className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Title & Subject</label>
                    <input
                      type="text"
                      placeholder="e.g. Unit 4: Vector Calculus Summary"
                      className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-bold"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Target Module</label>
                    <select
                      value={selectedCourse}
                      onChange={(e) => setSelectedCourse(e.target.value)}
                      className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-bold"
                      required
                    >
                      <option value="">Choose Course...</option>
                      {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                    </select>
                  </div>

                  {/* Drag and Drop Zone */}
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Materials (PDF/PPT/DOC)</label>
                    <div className="relative group">
                      <input
                        type="file"
                        accept=".pdf,.doc,.docx,.ppt,.pptx,.txt"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                        required
                      />
                      <div className={cn(
                        "w-full py-10 border-2 border-dashed rounded-3xl flex flex-col items-center justify-center transition-all",
                        file ? "border-emerald-200 bg-emerald-50/30" : "border-slate-200 bg-slate-50 group-hover:bg-slate-100 group-hover:border-brand-200"
                      )}>
                        {file ? (
                          <>
                            <div className="w-12 h-12 bg-emerald-500 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-emerald-500/20 mb-3">
                              <ShieldCheck className="w-6 h-6" />
                            </div>
                            <span className="text-sm font-black text-emerald-600 uppercase">{file.name}</span>
                            <span className="text-[10px] font-bold text-emerald-400 uppercase">{(file.size / 1024).toFixed(0)} KB ready</span>
                          </>
                        ) : (
                          <>
                            <div className="w-12 h-12 bg-white border border-slate-200 rounded-2xl flex items-center justify-center text-slate-400 shadow-sm mb-3 group-hover:text-brand-500 transition-colors">
                              <Upload className="w-6 h-6" />
                            </div>
                            <p className="text-xs font-black text-slate-400 uppercase tracking-widest">Drag or Click to Choose</p>
                            <p className="text-[10px] text-slate-400 font-medium mt-1">PDF, DOC, PPT up to 50MB</p>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pt-4 flex gap-4">
                   <button 
                     type="button"
                     onClick={() => setShowUploadModal(false)}
                     className="flex-1 py-4 bg-slate-100 text-slate-600 rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-slate-200 transition-all active:scale-95"
                   >
                     Cancel
                   </button>
                   <button 
                     type="submit" 
                     disabled={uploading}
                     className="flex-[2] py-4 bg-brand-500 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 active:scale-95 flex items-center justify-center gap-2"
                   >
                     {uploading ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <><Plus className="w-4 h-4" /> Finalize Upload</>}
                   </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// Helper
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}

export default TeacherUploadNotes;
