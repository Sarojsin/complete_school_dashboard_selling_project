import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Video, 
  Upload, 
  Play, 
  Trash2, 
  Search, 
  Filter, 
  X, 
  Plus, 
  Image as ImageIcon,
  Film,
  Clock,
  CheckCircle2,
  AlertCircle,
  FileVideo,
  ChevronRight,
  MoreVertical
} from 'lucide-react';
import { getTeacherCourses, getTeacherVideos, uploadVideo, deleteVideo } from '../api/teachers';
import GlassCard from '../../../shared/components/GlassCard';
import ModernBadge from '../../../shared/components/ModernBadge';
import ModernStatCard from '../../../shared/components/ModernStatCard';

const TeacherUploadVideos = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [videoFile, setVideoFile] = useState(null);
  const [thumbnail, setThumbnail] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [existingVideos, setExistingVideos] = useState([]);
  const [loadingVideos, setLoadingVideos] = useState(true);
  const [showUploadModal, setShowUploadModal] = useState(false);

  useEffect(() => {
    loadCourses();
    loadExistingVideos();
  }, []);

  const loadCourses = async () => {
    try {
      const data = await getTeacherCourses();
      setCourses(data);
    } catch (err) {
      setError('Failed to load courses');
    }
  };

  const loadExistingVideos = async () => {
    setLoadingVideos(true);
    try {
      const data = await getTeacherVideos();
      setExistingVideos(data);
    } catch (err) {
      setError('Failed to load video library');
    } finally {
      setLoadingVideos(false);
    }
  };

  const handleVideoChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > 500 * 1024 * 1024) {
        setError('Video size exceeds 500MB limit');
        return;
      }
      setVideoFile(selectedFile);
    }
  };

  const handleThumbnailChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setThumbnail(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!videoFile) {
      setError('Please select a video file');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('course_id', selectedCourse);
    formData.append('video', videoFile);
    if (thumbnail) formData.append('thumbnail', thumbnail);

    try {
      // Use XHR for progress tracking in a real implementation
      // For this high-fidelity UI, we'll simulate or use a wrapper
      await uploadVideo(formData, (progress) => setUploadProgress(progress));
      
      setSuccess('Video processed and published!');
      setTitle('');
      setDescription('');
      setVideoFile(null);
      setThumbnail(null);
      setShowUploadModal(false);
      loadExistingVideos();
    } catch (err) {
      setError('Upload failed. Please check your connection.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (videoId) => {
    if (!window.confirm('Archive this video? Students will lose access.')) return;
    try {
      await deleteVideo(videoId);
      setExistingVideos(existingVideos.filter(v => v.id !== videoId));
    } catch (err) {
      setError('Archive failed');
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
              <Film className="w-6 h-6 text-brand-500" />
            </div>
            <span className="text-sm font-bold text-brand-500 uppercase tracking-widest">Digital Media Hub</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Video Lecture Library</h1>
          <p className="text-slate-500 text-lg mt-1 font-medium">Create engaging asynchronous learning experiences.</p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex items-center gap-3">
          <button 
            onClick={() => setShowUploadModal(true)}
            className="px-6 py-3 bg-brand-500 text-white rounded-2xl text-sm font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand-500/20 flex items-center gap-2 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            New Broadcast
          </button>
        </motion.div>
      </section>

      {/* Quick Stats */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ModernStatCard icon={Video} title="Total Lectures" value={existingVideos.length} trend="Across all courses" trendType="neutral" />
        <ModernStatCard icon={Clock} title="Watch Time" value="124h" trend="↑ 4.2% this month" trendType="positive" />
        <ModernStatCard icon={CheckCircle2} title="Active Views" value="892" trend="Avg student engagement" trendType="neutral" />
      </motion.section>

      {/* Media Catalog Toolbar */}
      <motion.section variants={itemVariants} className="flex flex-col md:flex-row gap-4 items-center">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search by lecture title, chapter, or date..." 
            className="w-full pl-12 pr-4 py-4 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium text-slate-700 shadow-sm"
          />
        </div>
        <div className="flex items-center gap-2">
          <button className="px-6 py-4 bg-white border border-slate-200 rounded-2xl text-slate-600 font-bold flex items-center gap-2 hover:bg-slate-50 transition-all shadow-sm">
            <Filter className="w-4 h-4" /> All Subjects
          </button>
        </div>
      </motion.section>

      {/* Video Grid */}
      <motion.section variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {loadingVideos ? (
          [1,2,3].map(i => <div key={i} className="aspect-video bg-slate-50 rounded-3xl animate-pulse" />)
        ) : existingVideos.length === 0 ? (
          <div className="col-span-full py-40 text-center bg-slate-50/50 rounded-[3rem] border-2 border-dashed border-slate-200">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm">
               <FileVideo className="w-10 h-10 text-slate-200" />
            </div>
            <h3 className="text-2xl font-black text-slate-900 uppercase tracking-tight">No videos hosted yet</h3>
            <p className="text-slate-500 mt-2 font-medium max-w-sm mx-auto">Upload your first lecture to start building your class media archive.</p>
          </div>
        ) : (
          existingVideos.map((video) => (
            <motion.div key={video.id} whileHover={{ y: -8 }} transition={{ type: 'spring', stiffness: 300 }}>
              <GlassCard noPadding className="h-full flex flex-col group overflow-hidden border-transparent hover:border-brand-200">
                {/* Thumbnail Area */}
                <div className="relative aspect-video bg-slate-900 overflow-hidden">
                   {video.thumbnail_url ? (
                     <img src={video.thumbnail_url} alt={video.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 opacity-80" />
                   ) : (
                     <div className="w-full h-full flex items-center justify-center">
                        <Film className="w-12 h-12 text-slate-700" />
                     </div>
                   )}
                   <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-60" />
                   
                   {/* Play Button Overlay */}
                   <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <div className="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center text-white scale-75 group-hover:scale-100 transition-transform duration-300">
                         <Play className="w-8 h-8 fill-current translate-x-1" />
                      </div>
                   </div>

                   <div className="absolute bottom-4 left-4 right-4 flex justify-between items-center text-white z-10">
                      <ModernBadge variant="primary" size="sm" className="bg-brand-500/80 backdrop-blur-md border-transparent text-[8px]">
                        {video.duration || '12:40'}
                      </ModernBadge>
                      <span className="text-[10px] font-black uppercase tracking-widest drop-shadow-md">HD 1080p</span>
                   </div>
                </div>

                <div className="p-6 flex-1 space-y-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-black text-slate-900 line-clamp-1 group-hover:text-brand-500 transition-colors uppercase tracking-tight">{video.title}</h3>
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">{video.course_name}</p>
                    </div>
                    <button className="text-slate-300 hover:text-slate-600 transition-colors">
                      <MoreVertical className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <p className="text-sm text-slate-500 font-medium line-clamp-2 leading-relaxed">{video.description || "No description provided for this lecture."}</p>
                </div>

                <div className="p-4 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between">
                  <div className="flex gap-2">
                    <a 
                      href={video.video_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-slate-900 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-700 transition-all shadow-lg shadow-slate-900/10 flex items-center gap-2"
                    >
                      Watch <ChevronRight className="w-3 h-3" />
                    </a>
                  </div>
                  <button 
                    onClick={() => handleDelete(video.id)}
                    className="p-2 text-slate-400 hover:text-rose-500 transition-colors"
                    title="Delete Video"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </GlassCard>
            </motion.div>
          ))
        )}
      </motion.section>

      {/* Media Upload Modal */}
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
              className="relative w-full max-w-4xl bg-white rounded-[3rem] shadow-2xl overflow-hidden flex flex-col md:flex-row h-[85vh] md:h-auto"
            >
              {/* Image Preview / Branding Side */}
              <div className="w-full md:w-80 bg-brand-500 p-10 flex flex-col justify-between text-white relative">
                 <div className="space-y-4">
                    <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center">
                       <Film className="w-6 h-6" />
                    </div>
                    <h3 className="text-3xl font-black tracking-tight leading-none uppercase">Broadcast <br />Center</h3>
                    <p className="text-white/70 text-sm font-medium leading-relaxed">Publish high-definition lecture content directly to your students' dashboards.</p>
                 </div>
                 
                 <div className="space-y-4 pt-10">
                    <div className="p-4 bg-white/10 rounded-2xl border border-white/10 space-y-2">
                       <span className="text-[10px] font-black uppercase tracking-widest">Server Status</span>
                       <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                          <span className="text-xs font-bold uppercase">Uplink Ready</span>
                       </div>
                    </div>
                 </div>

                 {/* Decorative background shape */}
                 <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-white/10 rounded-full blur-3xl pointer-events-none" />
              </div>

              {/* Form Side */}
              <div className="flex-1 p-10 md:p-14 overflow-y-auto max-h-[85vh]">
                <div className="flex justify-between items-center mb-10">
                   <h4 className="text-sm font-black text-slate-400 uppercase tracking-[0.2em]">Meta Data & Files</h4>
                   <button onClick={() => setShowUploadModal(false)} className="p-2 hover:bg-slate-100 rounded-xl transition-all">
                     <X className="w-5 h-5 text-slate-400" />
                   </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-8">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="space-y-2">
                      <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Lecture Title</label>
                      <input
                        type="text"
                        placeholder="e.g. Intro to Quantum Theory"
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
                        <option value="">Select Course...</option>
                        {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Short Context / description</label>
                    <textarea
                      placeholder="What should students focus on in this video?"
                      className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-brand-500 transition-all font-medium min-h-[100px]"
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Video Upload */}
                    <div className="space-y-2">
                      <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Broadcast File (MP4/MOV)</label>
                      <div className="relative h-40 group">
                         <input
                           type="file"
                           accept="video/mp4,video/webm,video/mov"
                           onChange={handleVideoChange}
                           className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                           required
                         />
                         <div className={cn(
                           "w-full h-full border-2 border-dashed rounded-[2rem] flex flex-col items-center justify-center transition-all",
                           videoFile ? "border-emerald-200 bg-emerald-50/30" : "border-slate-200 bg-slate-50 hover:bg-slate-100 hover:border-brand-200"
                         )}>
                           {videoFile ? (
                             <>
                               <FileVideo className="w-10 h-10 text-emerald-500 mb-2" />
                               <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest max-w-[140px] truncate">{videoFile.name}</span>
                             </>
                           ) : (
                             <>
                               <Upload className="w-8 h-8 text-slate-300 mb-2 group-hover:text-brand-500 transition-colors" />
                               <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Source Clip</span>
                             </>
                           )}
                         </div>
                      </div>
                    </div>

                    {/* Thumbnail Upload */}
                    <div className="space-y-2">
                      <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Cover Art (Optional)</label>
                      <div className="relative h-40 group">
                         <input
                           type="file"
                           accept="image/*"
                           onChange={handleThumbnailChange}
                           className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                         />
                         <div className={cn(
                           "w-full h-full border-2 border-dashed rounded-[2rem] flex flex-col items-center justify-center transition-all",
                           thumbnail ? "border-amber-200 bg-amber-50/30" : "border-slate-200 bg-slate-50 hover:bg-slate-100 hover:border-brand-200"
                         )}>
                           {thumbnail ? (
                             <>
                               <ImageIcon className="w-10 h-10 text-amber-500 mb-2" />
                               <span className="text-[10px] font-black text-amber-600 uppercase tracking-widest max-w-[140px] truncate">{thumbnail.name}</span>
                             </>
                           ) : (
                             <>
                               <ImageIcon className="w-8 h-8 text-slate-300 mb-2 group-hover:text-brand-500 transition-colors" />
                               <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Poster Image</span>
                             </>
                           )}
                         </div>
                      </div>
                    </div>
                  </div>

                  {uploading && (
                    <div className="space-y-3">
                       <div className="flex justify-between items-end">
                          <span className="text-xs font-black text-brand-500 uppercase tracking-[0.2em] animate-pulse">Encoding & Uploading...</span>
                          <span className="text-xs font-black text-slate-900">{uploadProgress}%</span>
                       </div>
                       <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                          <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: `${uploadProgress}%` }}
                            className="h-full bg-brand-500 rounded-full"
                          />
                       </div>
                    </div>
                  )}

                  <div className="pt-6">
                    <button 
                      type="submit" 
                      disabled={uploading}
                      className="w-full py-5 bg-slate-900 text-white rounded-3xl text-sm font-black uppercase tracking-[0.2em] hover:bg-slate-800 transition-all shadow-2xl shadow-slate-900/20 active:scale-[0.98] disabled:opacity-50"
                    >
                      {uploading ? "Analyzing File Bits..." : "Finalize Broadcast"}
                    </button>
                  </div>
                </form>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// Tool utility
function cn(...inputs) {
  return inputs.filter(Boolean).join(' ');
}

export default TeacherUploadVideos;
