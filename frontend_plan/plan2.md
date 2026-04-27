# Plan 2: Reusable UI Components Library

## Objective
Create a library of reusable components matching the backup/templates design quality.

## Current State
- React components have inline styles
- No consistent component library
- Duplicated code across pages

## Required Components

### 2.1 StatCard Component
File: `frontend/src/modules/shared/components/StatCard.jsx`
```jsx
import './StatCard.css';

export default function StatCard({ icon, value, label, color = 'primary', trend }) {
  return (
    <div className={`stat-card stat-card-${color}`}>
      <div className="stat-card-content">
        <span className="stat-card-label">{label}</span>
        <span className="stat-card-value">{value}</span>
        {trend && <span className={`stat-card-trend ${trend.type}`}>{trend.value}</span>}
      </div>
      {icon && <div className="stat-card-icon">{icon}</div>}
    </div>
  );
}
```

File: `frontend/src/modules/shared/components/StatCard.css`
```css
.stat-card {
  background: var(--gradient-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  color: white;
  position: relative;
  overflow: hidden;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.stat-card.primary { background: var(--gradient-primary); }
.stat-card.success { background: var(--gradient-success); }
.stat-card.info { background: var(--gradient-info); }
.stat-card.warning { background: var(--gradient-warning); }
.stat-card.danger { background: var(--gradient-danger); }

.stat-card-icon {
  position: absolute;
  right: -10px;
  bottom: -10px;
  font-size: 5rem;
  opacity: 0.15;
}

.stat-card-label {
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.85;
}

.stat-card-value {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  display: block;
  margin: var(--spacing-xs) 0;
}

.stat-card-trend {
  font-size: var(--font-size-sm);
}

.stat-card-trend.positive { color: #86efac; }
.stat-card-trend.negative { color: #fca5a5; }
```

### 2.2 Card Component
File: `frontend/src/modules/shared/components/Card.jsx`
```jsx
import './Card.css';

export default function Card({ title, icon, action, children, className }) {
  return (
    <div className={`card-custom ${className || ''}`}>
      {(title || action) && (
        <div className="card-header-custom">
          {icon && <span className="card-icon">{icon}</span>}
          {title && <h3 className="card-title">{title}</h3>}
          {action && <div className="card-action">{action}</div>}
        </div>
      )}
      <div className="card-body-custom">{children}</div>
    </div>
  );
}
```

### 2.3 DataTable Component
File: `frontend/src/modules/shared/components/DataTable.jsx`
- Sortable columns
- Pagination
- Row hover effects
- Empty state handling

### 2.4 Badge Component
File: `frontend/src/modules/shared/components/Badge.jsx`
- Color variants (success, warning, danger, info, primary)
- Size variants

### 2.5 Button Component
File: `frontend/src/modules/shared/components/Button.jsx`
- Variants: primary, secondary, outline, ghost
- Sizes: sm, md, lg
- Icons support

### 2.6 EmptyState Component
File: `frontend/src/modules/shared/components/EmptyState.jsx`
- Icon, title, description, action button

## Priority
HIGH - Required for consistent UI across all pages

## Estimated Time
4-5 hours

## New Files to Create
- `frontend/src/modules/shared/components/StatCard.jsx`
- `frontend/src/modules/shared/components/StatCard.css`
- `frontend/src/modules/shared/components/Card.jsx`
- `frontend/src/modules/shared/components/Card.css`
- `frontend/src/modules/shared/components/DataTable.jsx`
- `frontend/src/modules/shared/components/DataTable.css`
- `frontend/src/modules/shared/components/Badge.jsx`
- `frontend/src/modules/shared/components/Badge.css`
- `frontend/src/modules/shared/components/Button.jsx`
- `frontend/src/modules/shared/components/Button.css`
- `frontend/src/modules/shared/components/EmptyState.jsx`
- `frontend/src/modules/shared/components/EmptyState.css`