# Plan 1: Design System & CSS Variables Setup

## Objective
Create a centralized design system with CSS variables matching the backup/templates quality.

## Current State
- React frontend uses basic inline styles with hardcoded colors
- No CSS variables or design tokens
- No consistent color system

## Required Changes

### 1.1 Create Global CSS Variables
File: `frontend/src/styles/variables.css`
```css
:root {
  /* Primary Colors */
  --primary: #4361ee;
  --primary-light: #4895ef;
  --primary-dark: #3a0ca3;
  --secondary: #3f37c9;
  
  /* Status Colors */
  --success: #10b981;
  --info: #4895ef;
  --warning: #f72585;
  --danger: #ef4444;
  
  /* Neutral Colors */
  --light: #f8f9fa;
  --dark: #212529;
  --text-primary: #1a1a2e;
  --text-secondary: #666;
  --text-muted: #888;
  
  /* Background Colors */
  --bg-primary: #f5f7fa;
  --bg-card: #ffffff;
  --bg-sidebar: #ffffff;
  
  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
  --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
  --gradient-info: linear-gradient(135deg, #4895ef 0%, #3f37c9 100%);
  --gradient-warning: linear-gradient(135deg, #f72585 0%, #b5179e 100%);
  --gradient-danger: linear-gradient(135deg, #ef4444 0%, #991b1b 100%);
  
  /* Shadows */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 15px rgba(0,0,0,0.05);
  --shadow-lg: 0 12px 25px rgba(0,0,0,0.1);
  
  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  
  /* Typography */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.85rem;
  --font-size-md: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 2rem;
  
  /* Transitions */
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

### 1.2 Import Variables in Main CSS
File: `frontend/src/index.css`
- Add `@import './styles/variables.css';` at the top
- Replace hardcoded colors with CSS variables

### 1.3 Create Theme Helper
File: `frontend/src/styles/theme.js`
```javascript
export const theme = {
  colors: {
    primary: '#4361ee',
    success: '#10b981',
    warning: '#f72585',
    danger: '#ef4444',
    info: '#4895ef',
  },
  gradients: {
    primary: 'linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%)',
    success: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
  },
  shadows: {
    card: '0 4px 15px rgba(0,0,0,0.05)',
    hover: '0 12px 25px rgba(0,0,0,0.1)',
  }
};
```

## Priority
HIGH - This foundation is required for all other plans

## Estimated Time
2-3 hours

## Files to Modify
- Create: `frontend/src/styles/variables.css`
- Create: `frontend/src/styles/theme.js`
- Modify: `frontend/src/index.css`