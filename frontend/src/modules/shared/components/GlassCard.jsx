import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function GlassCard({ children, title, icon: Icon, action, className, noPadding = false }) {
  return (
    <div className={cn(
      "bg-white border border-slate-100 rounded-[2.5rem] overflow-hidden shadow-sm transition-all duration-300 hover:shadow-xl",
      className
    )}>
      {(title || Icon || action) && (
        <div className="flex items-center justify-between px-8 py-5 border-b border-slate-100">
          <div className="flex items-center gap-3">
            {Icon && <Icon className="w-5 h-5 text-brand-500" />}
            {title && <h3 className="text-sm font-black tracking-tight text-slate-900 uppercase">{title}</h3>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {noPadding ? children : <div className="p-8">{children}</div>}
    </div>
  );
}
