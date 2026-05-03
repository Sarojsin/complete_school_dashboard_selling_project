import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  ShieldCheck, GraduationCap, Calculator, 
  FileText, Users, Library, 
  ArrowLeft, UserCircle, Briefcase, Network
} from "lucide-react";

export default function RegisterChoice() {
  const navigate = useNavigate();
  const selectedSystem = localStorage.getItem("selectedSystem") || "school";

  const roles = [
    { id: "student", icon: <GraduationCap className="w-8 h-8" />, title: "Student", description: "Access courses, grades, and records", color: "from-blue-500 to-cyan-400" },
    { id: "teacher", icon: <Briefcase className="w-8 h-8" />, title: "Teacher", description: "Manage classes, attendance, and grades", color: "from-indigo-500 to-purple-400" },
    { id: "parent", icon: <Users className="w-8 h-8" />, title: "Parent", description: "Monitor child's progress and fees", color: "from-emerald-500 to-teal-400" },
    { id: "authority", icon: <ShieldCheck className="w-8 h-8" />, title: "Authority", description: "Overall administrative control", color: "from-red-500 to-orange-400" },
    { id: "account_section", icon: <Calculator className="w-8 h-8" />, title: "Account Section", description: "Manage finances, salaries and fees", color: "from-amber-500 to-yellow-400" },
    { id: "exam_section", icon: <FileText className="w-8 h-8" />, title: "Exam Section", description: "Schedule exams and post results", color: "from-pink-500 to-rose-400" },
    { id: "hod", icon: <Network className="w-8 h-8" />, title: "HOD", description: "Head of Department management", color: "from-violet-500 to-fuchsia-400" },
    { id: "library", icon: <Library className="w-8 h-8" />, title: "Librarian", description: "Manage books, logs and issues", color: "from-lime-500 to-green-400" },
  ];

  const handleRoleSelect = (roleId) => {
    navigate(`/register?role=${roleId}&system=${selectedSystem}`);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.05, delayChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1, transition: { type: "spring", stiffness: 100 } }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 relative overflow-hidden font-sans">
      {/* Background glow effects */}
      <div className="absolute top-0 right-0 w-[50%] h-[50%] bg-indigo-600/20 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 rounded-full blur-[150px] pointer-events-none" />

      <motion.div 
        className="max-w-6xl w-full z-10"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants} className="flex flex-col md:flex-row items-start md:items-center justify-between mb-12">
          <div>
            <button 
              onClick={() => navigate("/")}
              className="group flex items-center text-slate-400 hover:text-white mb-4 transition-colors text-sm font-medium"
            >
              <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
              Change System
            </button>
            <h1 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-2">
              Select Your Role
            </h1>
            <p className="text-slate-400 text-lg">
              Registering for the <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 font-bold uppercase tracking-wider">{selectedSystem}</span> system
            </p>
          </div>
          
          <button 
            onClick={() => navigate("/login")}
            className="mt-6 md:mt-0 inline-flex items-center space-x-2 text-slate-300 hover:text-white px-5 py-2.5 rounded-full hover:bg-white/5 border border-transparent hover:border-white/10 transition-all"
          >
            <UserCircle className="w-5 h-5" />
            <span>Already registered? <span className="text-blue-400 font-semibold ml-1">Sign In</span></span>
          </button>
        </motion.div>

        <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {roles.map(role => (
            <div 
              key={role.id} 
              onClick={() => handleRoleSelect(role.id)}
              className="group relative bg-white/[0.03] hover:bg-white/[0.08] border border-white/5 hover:border-white/20 backdrop-blur-md rounded-2xl p-6 cursor-pointer transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 overflow-hidden flex flex-col h-full"
            >
              <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${role.color} opacity-50 group-hover:opacity-100 transition-opacity`} />
              
              <div className={`w-14 h-14 rounded-xl flex items-center justify-center mb-5 bg-gradient-to-br ${role.color} bg-opacity-10 text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                {role.icon}
              </div>
              
              <h3 className="text-xl font-bold text-white mb-2">{role.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed flex-grow">{role.description}</p>
              
              <div className="mt-6 pt-4 border-t border-white/5 text-sm font-semibold text-slate-300 group-hover:text-white flex items-center justify-between transition-colors">
                <span>Join as {role.title}</span>
                <ArrowLeft className="w-4 h-4 rotate-180 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}
