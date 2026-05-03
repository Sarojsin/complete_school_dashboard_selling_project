import React from 'react';
import './StatCard.css';

export default function StatCard({ icon, value, label, color = 'primary', trend, className }) {
  const colorClass = `stat-card-${color}`;
  
  return (
    <div className={`stat-card ${colorClass} ${className || ''}`}>
      <div className="stat-card-content">
        <span className="stat-card-label">{label}</span>
        <span className="stat-card-value">{value}</span>
        {trend && (
          <span className={`stat-card-trend ${trend.type}`}>
            <i className={`bi bi-arrow-${trend.type === 'up' ? 'up' : 'down'}`}></i>
            {trend.value}
          </span>
        )}
      </div>
      {icon && <div className="stat-card-icon"><i className={`bi bi-${icon}`}></i></div>}
    </div>
  );
}