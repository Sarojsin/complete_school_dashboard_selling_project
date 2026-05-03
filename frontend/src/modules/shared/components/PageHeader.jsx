import React from 'react';
import './PageHeader.css';

export default function PageHeader({ title, subtitle, icon, actions, className }) {
  return (
    <div className={`page-header ${className || ''}`}>
      <div className="page-header-content">
        {icon && (
          <div className="page-header-icon">
            <i className={`bi bi-${icon}`}></i>
          </div>
        )}
        <div className="page-header-text">
          <h1 className="page-title">{title}</h1>
          {subtitle && <p className="page-subtitle">{subtitle}</p>}
        </div>
      </div>
      {actions && <div className="page-header-actions">{actions}</div>}
    </div>
  );
}