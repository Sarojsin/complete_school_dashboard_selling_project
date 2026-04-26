# Frontend Mapping 7: Super Admin Module

## Overview
Migration of Super Admin Portal from Jinja templates to React.

## Backend API Source
**Prefix:** `/api/admin`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/dashboard | Get dashboard statistics |
| GET | /api/admin/users | List all users |
| GET | /api/admin/users/{user_id} | Get user by ID |
| PUT | /api/admin/users/{user_id}/deactivate | Deactivate user |
| GET | /api/admin/users-by-role | Get user count by role |
| GET | /api/admin/settings | List all system settings |
| GET | /api/admin/settings/{key} | Get specific setting |
| PUT | /api/admin/settings/{key} | Update system setting |
| GET | /api/admin/features | List all features |
| PUT | /api/admin/features/{name}/toggle | Toggle feature |
| GET | /api/admin/audit-logs | Get audit logs |
| GET | /api/admin/backups | List all backups |
| POST | /api/admin/backups | Create new backup |

## Old Jinja Templates (Source)
Location: `backup/templates/admin/`
- dashboard.html
- users.html
- settings.html
- security.html
- features.html
- feature_detail.html
- backup.html
- reports.html
- academic.html
- finance.html
- media.html
- communication.html
- advanced.html
- notices.html
- audit_logs.html
- system.html

## Frontend Module Structure
```
frontend/src/modules/super_admin/
├── api/
│   └── superadmin.js     # ❌ MISSING - NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx     # ✅ ALREADY EXISTS (partial)
│   ├── Users.jsx         # ❌ MISSING
│   ├── Settings.jsx      # ❌ MISSING
│   ├── Security.jsx      # ❌ MISSING
│   ├── Features.jsx      # ❌ MISSING
│   ├── Backups.jsx       # ❌ MISSING
│   ├── Reports.jsx      # ❌ MISSING
│   ├── Academic.jsx      # ❌ MISSING
│   ├── Finance.jsx       # ❌ MISSING
│   ├── Media.jsx         # ❌ MISSING
│   ├── Notices.jsx       # ❌ MISSING
│   └── AuditLogs.jsx    # ❌ MISSING
└── styles/
    └── superadmin.css
```

## Frontend Pages Status

### Partial Complete ⚠️

#### 1. Dashboard.jsx
**Status:** ⚠️ PARTIAL
**Features:**
- Basic statistics
- Quick links

**API Calls needed:**
```javascript
// Create api/superadmin.js
- getAdminDashboard() → GET /api/admin/dashboard
- getUserStats() → GET /api/admin/users-by-role
```

### Missing Pages ❌

#### 2. Users.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List all users
- Filter by role/status
- Search users
- Activate/Deactivate user
- View user details
- Add new user

**API Calls needed:**
```javascript
- getAllUsers() → GET /api/admin/users
- getUserById(userId) → GET /api/admin/users/{user_id}
- deactivateUser(userId) → PUT /api/admin/users/{user_id}/deactivate
- activateUser(userId) → PUT /api/admin/users/{user_id}/activate
```

#### 3. Settings.jsx
**Status:** ❌ MISSING
**Features to implement:**
- System settings list
- Edit settings
- Site configuration
- Email settings

**API Calls needed:**
```javascript
- getSettings() → GET /api/admin/settings
- getSetting(key) → GET /api/admin/settings/{key}
- updateSetting(key, value) → PUT /api/admin/settings/{key}
```

#### 4. Security.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Security settings
- Password policies
- Session management
- IP whitelist

**API Calls needed:**
```javascript
- getSecuritySettings() → GET /api/admin/security
- updateSecuritySettings(data) → PUT /api/admin/security
```

#### 5. Features.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List all features
- Toggle features on/off
- Feature configuration

**API Calls needed:**
```javascript
- getFeatures() → GET /api/admin/features
- toggleFeature(name) → PUT /api/admin/features/{name}/toggle
```

#### 6. Backups.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List backups
- Create backup
- Download backup
- Restore backup
- Delete backup

**API Calls needed:**
```javascript
- getBackups() → GET /api/admin/backups
- createBackup() → POST /api/admin/backups
- downloadBackup(backupId) → GET /api/admin/backups/{id}/download
- restoreBackup(backupId) → POST /api/admin/backups/{id}/restore
- deleteBackup(backupId) → DELETE /api/admin/backups/{id}
```

#### 7. Reports.jsx
**Status:** ❌ MISSING
**Features to implement:**
- System reports
- User activity reports
- Export reports

**API Calls needed:**
```javascript
- getReports() → GET /api/admin/reports
- generateReport(type) → POST /api/admin/reports/generate
```

#### 8. Academic.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Academic settings
- Curriculum management
- Academic years

**API Calls needed:**
```javascript
- getAcademicSettings() → GET /api/admin/academic
- updateAcademicSettings(data) → PUT /api/admin/academic
```

#### 9. Finance.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Financial settings
- Fee structure
- Payment gateways

**API Calls needed:**
```javascript
- getFinanceSettings() → GET /api/admin/finance
- updateFinanceSettings(data) → PUT /api/admin/finance
```

#### 10. Media.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Media library
- Upload files
- Manage uploads

**API Calls needed:**
```javascript
- getMediaFiles() → GET /api/admin/media
- uploadMedia(file) → POST /api/admin/media
- deleteMedia(fileId) → DELETE /api/admin/media/{id}
```

#### 11. Notices.jsx (Admin)
**Status:** ❌ MISSING
**Features to implement:**
- System-wide notices
- Create notice
- Manage notices

**API Calls needed:**
```javascript
- getAdminNotices() → GET /api/admin/notices
- createNotice(data) → POST /api/admin/notices
```

#### 12. AuditLogs.jsx
**Status:** ❌ MISSING
**Features to implement:**
- View audit logs
- Filter by date/user/action
- Export logs

**API Calls needed:**
```javascript
- getAuditLogs() → GET /api/admin/audit-logs
- getAuditLogsByUser(userId) → GET /api/admin/audit-logs?user={user_id}
- getAuditLogsByDate(start, end) → GET /api/admin/audit-logs?start={date}&end={date}
```

## Data Schemas

### User
```javascript
{
  id: number,
  email: string,
  first_name: string,
  last_name: string,
  role: string,
  is_active: boolean,
  created_at: string,
  last_login?: string
}
```

### Setting
```javascript
{
  key: string,
  value: string,
  type: string,
  description: string
}
```

### Feature
```javascript
{
  name: string,
  enabled: boolean,
  description: string,
  config?: object
}
```

### Backup
```javascript
{
  id: number,
  filename: string,
  size: number,
  created_at: string,
  status: "completed" | "in_progress" | "failed"
}
```

### AuditLog
```javascript
{
  id: number,
  user_id: number,
  user_email: string,
  action: string,
  resource: string,
  details: object,
  ip_address: string,
  timestamp: string
}
```

## Implementation Order
1. ⚠️ Dashboard - Partial (needs completion)
2. ❌ Users - Second
3. ❌ Settings - Third
4. ❌ Security - Fourth
5. ❌ Features - Fifth
6. ❌ Backups - Sixth
7. ❌ Reports - Seventh
8. ❌ Academic - Eighth
9. ❌ Finance - Ninth
10. ❌ Media - Tenth
11. ❌ Notices - Eleventh
12. ❌ AuditLogs - Twelfth

## Notes
- Super Admin module is ~10% complete
- Need to create api/superadmin.js first
- This is the most complex module with many features
- Security and settings are critical
