import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from "framer-motion";
import { Lock, User, LogIn, AlertCircle, ArrowLeft } from "lucide-react";
import { login } from '../api/auth';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [selectedPortal, setSelectedPortal] = useState('school');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Determine portal from URL query param or localStorage (fallback)
  useEffect(() => {
    const portalFromUrl = searchParams.get('portal');
    if (portalFromUrl) {
      setSelectedPortal(portalFromUrl);
      localStorage.setItem('selectedPortal', portalFromUrl);
    } else {
      const saved = localStorage.getItem('selectedSystem') || 'school';
      setSelectedPortal(saved);
    }
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password, selectedPortal);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6 relative overflow-hidden font-sans text-slate-200">
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        className="w-full max-w-md relative z-10"
      >
        <button 
          onClick={() => navigate('/')}
          className="group flex items-center text-slate-400 hover:text-white mb-6 transition-colors text-sm font-medium"
        >
          <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Home
        </button>

        <div className="bg-white/[0.03] backdrop-blur-xl border border-white/10 rounded-3xl p-8 sm:p-10 shadow-2xl">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-white/10 mb-4 shadow-inner">
              <LogIn className="w-8 h-8 text-blue-400" />
            </div>
            <h2 className="text-3xl font-extrabold text-white tracking-tight">Welcome Back</h2>
            <p className="text-slate-400 mt-2">Sign in to your EduManage account</p>
          </div>
          
          {/* Portal Selector */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-slate-300 mb-3 text-center">Select Portal</label>
            <div className="flex rounded-xl overflow-hidden border border-white/10 bg-white/5 p-1">
              <button
                type="button"
                onClick={() => setSelectedPortal('school')}
                className={`flex-1 py-2 px-4 text-sm font-semibold rounded-lg transition-all ${
                  selectedPortal === 'school'
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                School Portal
              </button>
              <button
                type="button"
                onClick={() => setSelectedPortal('college')}
                className={`flex-1 py-2 px-4 text-sm font-semibold rounded-lg transition-all ${
                  selectedPortal === 'college'
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                College Portal
              </button>
            </div>
          </div>
           
          {error && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl mb-6 flex items-start text-sm"
            >
              <AlertCircle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
              <span>{error}</span>
            </motion.div>
          )}
           
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-300 ml-1">Username</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-slate-500 group-focus-within:text-blue-400 transition-colors" />
                </div>
                <input 
                  type="text" 
                  value={username} 
                  onChange={(e) => setUsername(e.target.value)} 
                  required 
                  className="block w-full pl-11 pr-4 py-3.5 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-white placeholder-slate-500 transition-all outline-none"
                  placeholder="Enter your username"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-300 ml-1">Password</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-slate-500 group-focus-within:text-blue-400 transition-colors" />
                </div>
                <input 
                  type="password" 
                  value={password} 
                  onChange={(e) => setPassword(e.target.value)} 
                  required 
                  className="block w-full pl-11 pr-4 py-3.5 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-white placeholder-slate-500 transition-all outline-none"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div className="flex items-center justify-between mt-2">
              <label className="flex items-center">
                <input type="checkbox" className="w-4 h-4 rounded border-white/10 bg-white/5 text-blue-500 focus:ring-blue-500/50 focus:ring-offset-slate-900" />
                <span className="ml-2 text-sm text-slate-400">Remember me</span>
              </label>
              <a href="#" className="text-sm font-medium text-blue-400 hover:text-blue-300 transition-colors">Forgot password?</a>
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full relative overflow-hidden group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-3.5 px-4 rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.3)] transition-all duration-300 disabled:opacity-70 disabled:cursor-not-allowed transform hover:-translate-y-0.5"
            >
              <span className="relative z-10 flex items-center justify-center">
                {loading ? (
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : 'Sign In'}
              </span>
            </button>
          </form>

          <p className="mt-8 text-center text-sm text-slate-400">
            Don't have an account?{' '}
            <button onClick={() => navigate('/register-choice')} className="font-medium text-blue-400 hover:text-blue-300 transition-colors ml-1">
              Register now
            </button>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
