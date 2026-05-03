import React from 'react';
import { cn } from './GlassCard';

export default function ModernBadge({ variant = 'neutral', size = 'md', children, className }) {
  const variants = {
    primary: "bg-brand-50 text-brand-700 border-brand-100",
    success: "bg-emerald-50 text-emerald-700 border-emerald-100",
    warning: "bg-amber-50 text-amber-700 border-amber-100",
    danger: "bg-rose-50 text-rose-700 border-rose-100",
    info: "bg-sky-50 text-sky-700 border-sky-100",
    neutral: "bg-slate-50 text-slate-700 border-slate-100",
  };

  const sizes = {
    sm: "px-1.5 py-0.5 text-[10px]",
    md: "px-2.5 py-1 text-xs",
    lg: "px-3 py-1.5 text-sm",
  };

  return (
    <span className={cn(
      "inline-flex font-bold rounded-full border items-center justify-center uppercase tracking-wide shadow-sm",
      variants[variant],
      sizes[size],
      className
    )}>
      {children}
    </span>
  );
}
