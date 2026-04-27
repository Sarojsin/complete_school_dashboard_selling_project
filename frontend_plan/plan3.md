# Plan 3: Sidebar and Layout Enhancement

## Objective
Create a rich, interactive sidebar with icons and proper navigation matching backup/templates.

## Current State
- Simple sidebar without icons
- Limited navigation items
- No active state styling

## Required Changes

### 3.1 Enhanced Sidebar Component
File: `frontend/src/modules/shared/components/Sidebar.jsx` (Enhance existing)

```jsx
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const menuItems = {
  student: [
    { path: '/student/dashboard', icon: 'bi-speedometer2', label: 'Dashboard' },
    { path: '/student/courses', icon: 'bi-book', label: 'Courses' },
    { path: '/student/assignments', icon: 'bi-journal-text', label: 'Assignments' },
    { path: '/student/grades', icon: 'bi-graph-up', label: 'Grades' },
    { path: '/student/attendance', icon: 'bi-calendar-check', label: 'Attendance' },
    { path: '/student/timetable', icon: 'bi-calendar-week', label: 'Timetable' },
    { path: '/student/notes', icon: 'bi-journal', label: 'Study Materials' },
    { path: '/student/videos', icon: 'bi-play-circle', label: 'Videos' },
    { path: '/student/library', icon: 'bi-book-half', label: 'Library' },
    { path: '/student/fees', icon: 'bi-cash-coin', label: 'Fees' },
    { path: '/student/notices', icon: 'bi-megaphone', label: 'Notices' },
    { path: '/student/messages', icon: 'bi-chat-dots', label: 'Messages' },
    { path: '/student/groups', icon: 'bi-people', label: 'Groups' },
    { path: '/student/profile', icon: 'bi-person', label: 'Profile' },
  ],
  teacher: [
    { path: '/teacher/dashboard', icon: 'bi-speedometer2', label: 'Dashboard' },
    { path: '/teacher/students', icon: 'bi-people', label: 'Students' },
    { path: '/teacher/courses', icon: 'bi-book', label: 'Courses' },
    { path: '/teacher/assignments', icon: 'bi-journal-text', label: 'Assignments' },
    { path: '/teacher/grades', icon: 'bi-graph-up', label: 'Grades' },
    { path: '/teacher/attendance', icon: 'bi-calendar-check', label: 'Attendance' },
    { path: '/teacher/tests', icon: 'bi-pencil-square', label: 'Tests' },
    { path: '/teacher/timetable', icon: 'bi-calendar3', label: 'Timetable' },
    { path: '/teacher/chat', icon: 'bi-chat-dots', label: 'Chat' },
    { path: '/teacher/groups', icon: 'bi-people-fill', label: 'Groups' },
    { path: '/teacher/profile', icon: 'bi-person', label: 'Profile' },
  ],
  authority: [
    { path: '/authority/dashboard', icon: 'bi-speedometer2', label: 'Dashboard' },
    { path: '/authority/students', icon: 'bi-people', label: 'Students' },
    { path: '/authority/teachers', icon: 'bi-person-badge', label: 'Teachers' },
    { path: '/authority/courses', icon: 'bi-book', label: 'Courses' },
    { path: '/authority/fees', icon: 'bi-cash-coin', label: 'Fee Management' },
    { path: '/authority/notices', icon: 'bi-megaphone', label: 'Notices' },
    { path: '/authority/analytics', icon: 'bi-graph-up', label: 'Analytics' },
    { path: '/authority/groups', icon: 'bi-people-fill', label: 'Groups' },
    { path: '/authority/departments', icon: 'bi-building', label: 'Departments' },
  ],
  superadmin: [
    { path: '/superadmin/dashboard', icon: 'bi-grid-view', label: 'Command Center' },
    { path: '/superadmin/users', icon: 'bi-people', label: 'User Management' },
    { path: '/superadmin/academic', icon: 'bi-school', label: 'Academic' },
    { path: '/superadmin/finance', icon: 'bi-payments', label: 'Finance' },
    { path: '/superadmin/features', icon: 'bi-vitals', label: 'Feature Matrix' },
    { path: '/superadmin/audit', icon: 'bi-history', label: 'Audit Spectrum' },
    { path: '/superadmin/settings', icon: 'bi-gear', label: 'System Tuning' },
    { path: '/superadmin/system', icon: 'bi-memory', label: 'System Monitor' },
    { path: '/superadmin/security', icon: 'bi-shield', label: 'Security Control' },
    { path: '/superadmin/backups', icon: 'bi-backup', label: 'Backups' },
    { path: '/superadmin/reports', icon: 'bi-file-text', label: 'Reports' },
  ]
};

export default function Sidebar({ role = 'student' }) {
  const items = menuItems[role] || menuItems.student;
  
  return (
    <aside className="sidebar-enhanced">
      <nav className="sidebar-nav">
        {items.map(item => (
          <NavLink 
            key={item.path} 
            to={item.path} 
            className={({ isActive }) => `nav-link-enhanced ${isActive ? 'active' : ''}`}
          >
            <i className={`bi ${item.icon}`}></i>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
```

### 3.2 Sidebar CSS
File: `frontend/src/modules/shared/components/Sidebar.css`

```css
.sidebar-enhanced {
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  height: fit-content;
  position: sticky;
  top: 20px;
  padding: var(--spacing-md);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.nav-link-enhanced {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 14px 18px;
  color: #475569;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link-enhanced:hover {
  background: #f1f5f9;
  color: var(--primary);
  transform: translateX(5px);
}

.nav-link-enhanced.active {
  background: var(--gradient-primary);
  color: white;
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}

.nav-link-enhanced i {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
}
```

### 3.3 Page Header Component
File: `frontend/src/modules/shared/components/PageHeader.jsx`

```jsx
import './PageHeader.css';

export default function PageHeader({ title, subtitle, actions, icon }) {
  return (
    <div className="page-header">
      <div className="page-header-content">
        {icon && <div className="page-header-icon">{icon}</div>}
        <div>
          <h1 className="page-title">{title}</h1>
          {subtitle && <p className="page-subtitle">{subtitle}</p>}
        </div>
      </div>
      {actions && <div className="page-header-actions">{actions}</div>}
    </div>
  );
}
```

## Priority
HIGH - Essential for navigation and page structure

## Estimated Time
3-4 hours

## Files to Modify
- Modify: `frontend/src/modules/shared/components/Sidebar.jsx`
- Create: `frontend/src/modules/shared/components/Sidebar.css`
- Create: `frontend/src/modules/shared/components/PageHeader.jsx`
- Create: `frontend/src/modules/shared/components/PageHeader.css`