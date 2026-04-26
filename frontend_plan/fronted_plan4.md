# Frontend Plan 4: Campus Life & Support

Focuses on daily life, community, and support services.

## 1. Parent Experience Portal
- **Goal**: Transparency and tracking for families.
- **Features**: Child Performance/Attendance Dashboard, Communication with teachers.
- **Backend**: `/api/parents/dashboard`, `/api/parents/child/{id}/*`.

## 2. Library Digital Catalog
- **Goal**: Resource accessibility.
- **Features**: Searchable book list, Loan status, Overdue alerts.
- **Backend**: `/api/library/*`.

## 3. Global Schools Notices
- **Goal**: Critical updates.
- **Features**: Filterable notice feed by Urgency/Category, Document/attachment view.
- **Backend**: `/api/notices/*`.

## 4. Modern Chat & Messaging Hub
- **Goal**: Social connectivity.
- **Features**: Real-time chat (if backend supports) or Threaded Messaging for parents/teachers.
- **Backend**: `/api/parents/chat` (existing placeholder).

## 5. User Profiles & General Support
- **Goal**: Profile and help desk.
- **Features**: Role-based profile management, Contact School Admin form.
- **Backend**: `/api/auth/profile`.

---
*Implementation Order: 1 -> 5*
