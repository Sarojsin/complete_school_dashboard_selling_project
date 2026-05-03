import React from 'react';
import './Badge.css';

export default function Badge({ children, variant = 'primary', size = 'md', className }) {
  return (
    <span className={`badge-custom badge-${variant} badge-${size} ${className || ''}`}>
      {children}
    </span>
  );
}