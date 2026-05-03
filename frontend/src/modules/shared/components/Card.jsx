import React from 'react';
import './Card.css';

export default function Card({ title, icon, action, children, className, noPadding }) {
  return (
    <div className={`card-custom ${className || ''}`}>
      {(title || action) && (
        <div className="card-header-custom">
          <div className="card-header-left">
            {icon && <span className="card-icon"><i className={`bi bi-${icon}`}></i></span>}
            {title && <h3 className="card-title">{title}</h3>}
          </div>
          {action && <div className="card-action">{action}</div>}
        </div>
      )}
      <div className={`card-body-custom ${noPadding ? 'no-padding' : ''}`}>
        {children}
      </div>
    </div>
  );
}