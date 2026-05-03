import React from 'react';
import { cn } from './GlassCard';

export default function ModernStatCard({ 
  icon: Icon, 
  title, 
  value, 
  trend, 
  trendType = 'neutral',
  className 
}) {
  return (
    <div className={cn(
      "bg-white border border-slate-100 p-6 rounded-[2rem] flex items-center gap-4 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 shadow-sm", 
      className
    )}>
      <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-brand-50 text-brand-500 shrink-0">
        {Icon && <Icon className="w-6 h-6" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest truncate">{title}</p>
        <div className="flex items-baseline gap-2 mt-0.5 flex-wrap">
          <h4 className="text-2xl font-black text-slate-900 leading-none">{value}</h4>
          {trend && (
            <span className={cn(
              "text-[9px] px-2 py-1 rounded-full font-black uppercase tracking-wider",
              trendType === 'positive' ? "bg-emerald-100 text-emerald-700" : 
              trendType === 'danger'   ? "bg-rose-100 text-rose-700" :
              trendType === 'warning'  ? "bg-amber-100 text-amber-700" :
              "bg-slate-100 text-slate-600"
            )}>
              {trend}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
