# Frontend Plan 5: Premium Landing & System Governance

Focuses on the public face and the ultimate system-wide administrative control.

## 1. Premium School Landing Page
- **Goal**: Wow factor for prospective and current users.
- **Features**: Hero section with glassmorphism, Feature bento grid, Testimonials, Contact section with map.
- **Backend**: Public access.

## 2. Super Admin Power Dashboard
- **Goal**: Full system oversight.
- **Features**: Statistics cards (Total Users by role, System Load, Active Sessions).
- **Backend**: `/api/admin/dashboard`, `/api/admin/users/*`.

## 3. Global Configuration & Settings
- **Goal**: Intuitive system control.
- **Features**: Form-driven settings (SMTP, Payment gateways, Notification toggles).
- **Backend**: `/api/admin/settings/*`.

## 4. Feature Toggle Management
- **Goal**: Modular modularity.
- **Features**: Switches for enabling/disabling entire modules (e.g., Library, Exams).
- **Backend**: `/api/admin/features/*`.

## 5. Security & Audit Logs
- **Goal**: Institutional safety.
- **Features**: Searchable audit logs with filtering, Backup management interface.
- **Backend**: `/api/admin/audit-logs`, `/api/admin/backups`.

---
*Implementation Order: 1 -> 5*
