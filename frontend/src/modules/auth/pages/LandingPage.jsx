import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { GraduationCap, School, ArrowRight, UserCircle } from "lucide-react";

export default function LandingPage() {
  const navigate = useNavigate();

  const handleChoice = (system) => {
    localStorage.setItem("selectedSystem", system);
    navigate("/register-choice");
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1, transition: { type: "spring", stiffness: 100 } }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6 relative overflow-hidden font-sans">
      {/* Background glow effects */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/30 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />

      <motion.div 
        className="max-w-5xl w-full z-10 flex flex-col items-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants} className="text-center mb-16">
          <div className="inline-flex items-center justify-center p-3 bg-white/5 rounded-2xl mb-6 backdrop-blur-sm border border-white/10 shadow-xl">
            <School className="w-8 h-8 text-blue-400 mr-3" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent">
              TARAISHA EDU
            </h1>
          </div>
          <h2 className="text-5xl md:text-6xl font-extrabold text-white mb-6 tracking-tight">
            The Future of <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">
              Education Management
            </span>
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            A comprehensive unified platform for institutions. Select your institution type below to begin transforming your academic ecosystem.
          </p>
        </motion.div>

        <motion.div variants={itemVariants} className="grid md:grid-cols-2 gap-8 w-full max-w-4xl mb-12">
          {/* School Card */}
          <div 
            onClick={() => handleChoice("school")}
            className="group relative bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/50 backdrop-blur-md rounded-3xl p-8 cursor-pointer transition-all duration-300 hover:shadow-[0_0_40px_rgba(59,130,246,0.15)] hover:-translate-y-2 overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-bl-full -z-10 transition-transform group-hover:scale-110" />
            
            <div className="w-16 h-16 bg-blue-500/20 rounded-2xl flex items-center justify-center mb-6 text-blue-400 group-hover:scale-110 transition-transform duration-300">
              <School className="w-8 h-8" />
            </div>
            <h3 className="text-3xl font-bold text-white mb-3">School System</h3>
            <p className="text-slate-400 mb-8 leading-relaxed">
              Complete management solution tailored for K-12 educational institutions with focused tools for teachers and parents.
            </p>
            <div className="flex items-center text-blue-400 font-semibold group-hover:text-blue-300 transition-colors">
              Continue as School <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* College Card */}
          <div 
            onClick={() => handleChoice("college")}
            className="group relative bg-white/5 hover:bg-white/10 border border-white/10 hover:border-indigo-500/50 backdrop-blur-md rounded-3xl p-8 cursor-pointer transition-all duration-300 hover:shadow-[0_0_40px_rgba(99,102,241,0.15)] hover:-translate-y-2 overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-bl-full -z-10 transition-transform group-hover:scale-110" />
            
            <div className="w-16 h-16 bg-indigo-500/20 rounded-2xl flex items-center justify-center mb-6 text-indigo-400 group-hover:scale-110 transition-transform duration-300">
              <GraduationCap className="w-8 h-8" />
            </div>
            <h3 className="text-3xl font-bold text-white mb-3">College System</h3>
            <p className="text-slate-400 mb-8 leading-relaxed">
              Advanced platform designed for higher education, universities, accommodating complex grading and multi-department structures.
            </p>
            <div className="flex items-center text-indigo-400 font-semibold group-hover:text-indigo-300 transition-colors">
              Continue as College <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </motion.div>

        {/* <motion.div variants={itemVariants} className="text-center">
          <button 
            onClick={() => navigate("/login")}
            className="inline-flex items-center space-x-2 text-slate-300 hover:text-white px-6 py-3 rounded-full hover:bg-white/5 transition-colors"
          >
            <UserCircle className="w-5 h-5" />
            <span>Already have an account? <span className="text-blue-400 font-semibold ml-1">Sign In</span></span>
          </button>
        </motion.div> */}

      </motion.div>
    </div>
  );
}
