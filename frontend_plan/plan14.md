# Plan 14: Icons, Animations & Polish

## Objective
Add icons, animations, and final polish to match backup/templates quality.

## Current State (React)
- No icons (Bootstrap Icons not integrated)
- No animations
- No hover effects
- Flat design

## Required Changes

### 14.1 Integrate Bootstrap Icons
Add to `frontend/index.html` or as npm package:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
```

Create Icon component:
```jsx
// frontend/src/modules/shared/components/Icon.jsx
export default function Icon({ name, size = 16 }) {
  return <i className={`bi bi-${name}`} style={{ fontSize: `${size}px` }}></i>;
}
```

### 14.2 Common Icons to Add
Dashboard: `grid-view`, `speedometer2`
Students: `people`, `person`
Teachers: `person-badge`, `person-check`
Courses: `book`, `bookmark`
Grades: `graph-up`, `bar-chart`
Attendance: `calendar-check`, `calendar`
Assignments: `journal-text`, `clipboard`
Notes: `journal`, `file-text`
Videos: `play-circle`, `film`
Library: `book-half`, `library`
Fees: `cash-coin`, `wallet`
Notices: `megaphone`, `bell`
Messages: `chat-dots`, `envelope`
Groups: `people`, `group`
Profile: `person`, `user`
Settings: `gear`, `sliders`
Reports: `file-earmark-text`, `chart-bar`
Add/Plus: `plus-circle`, `plus-lg`
Edit: `pencil`, `pencil-square`
Delete: `trash`, `trash2`
View: `eye`, `view`
Search: `search`, `magnifying-glass`
Filter: `filter`, `funnel`
Download: `download`, `arrow-down`
Upload: `upload`, `arrow-up`

### 14.3 Add Animations
Create animation CSS file:
```css
/* frontend/src/styles/animations.css */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.4s ease-out;
}

.animate-pulse {
  animation: pulse 2s infinite;
}

/* Staggered animation delays */
.animate-delay-1 { animation-delay: 0.1s; }
.animate-delay-2 { animation-delay: 0.2s; }
.animate-delay-3 { animation-delay: 0.3s; }
.animate-delay-4 { animation-delay: 0.4s; }
```

### 14.4 Hover Effects
Add to component CSS:
```css
/* Card hover */
.card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

/* Button hover */
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(67, 97, 238, 0.4);
}

/* Sidebar link hover */
.nav-link:hover {
  transform: translateX(5px);
}
```

### 14.5 Loading States
Create Loading component:
```jsx
// Skeleton loader
export default function Skeleton({ width, height }) {
  return <div className="skeleton" style={{ width, height }}></div>;
}
```

### 14.6 Empty States
Enhance EmptyState component with:
- Appropriate icon
- Helpful message
- Action button

### 14.7 Toast/Notification System
Create toast notifications for:
- Success actions
- Error messages
- Info alerts

## Priority
MEDIUM - Final polish

## Estimated Time
3-4 hours

## Files to Create/Modify
- Create: `frontend/src/styles/animations.css`
- Modify: `frontend/src/index.html` - add icons link
- Create: `frontend/src/modules/shared/components/Icon.jsx`
- Create: `frontend/src/modules/shared/components/Skeleton.jsx`
- Create: `frontend/src/modules/shared/components/Toast.jsx`
- Enhance: All existing components with hover effects