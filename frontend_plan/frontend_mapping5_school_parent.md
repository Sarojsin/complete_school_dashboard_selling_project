# Frontend Mapping 5: School Parent Module

## Overview
Migration of Parent Portal from Jinja templates to React.

## Backend API Source
**Prefix:** `/api/parents`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/parents/ | Create new parent |
| GET | /api/parents/{parent_id} | Get parent by ID |
| GET | /api/parents/ | List all parents |
| GET | /api/parents/me | Get current parent profile |
| PUT | /api/parents/{parent_id} | Update parent |
| DELETE | /api/parents/{parent_id} | Delete parent |
| GET | /api/parents/dashboard | Get parent dashboard |
| GET | /api/parents/child/{student_id}/attendance | Get child attendance |
| GET | /api/parents/child/{student_id}/grades | Get child grades |
| GET | /api/parents/child/{student_id}/homework | Get child homework |
| GET | /api/parents/notices | Get notices for parent |
| GET | /api/parents/chat | Get chat contacts |

## Old Jinja Templates (Source)
Location: `backup/templates/parent/`
- dashboard.html
- profile.html
- attendance.html
- grades.html
- homework.html
- fees.html
- notices.html
- chat.html
- messages.html

## Frontend Module Structure
```
frontend/src/modules/school/school_parent/
├── api/
│   └── parents.js       # ❌ MISSING - NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── ChildAttendance.jsx  # ❌ MISSING
│   ├── ChildGrades.jsx  # ❌ MISSING
│   ├── ChildFees.jsx   # ❌ MISSING
│   ├── Notices.jsx     # ❌ MISSING
│   ├── Chat.jsx        # ❌ MISSING
│   └── Profile.jsx     # ❌ MISSING
└── styles/
    └── parent.css
```

## Frontend Pages - ALL MISSING ❌

### 1. Dashboard.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Overview of linked children
- Quick stats (attendance, grades summary)
- Recent notices
- Quick links

**API Calls needed:**
```javascript
// Create api/parents.js
- getParentDashboard() → GET /api/parents/dashboard
- getLinkedChildren() → GET /api/parents/me (includes children)
- getChildren() → GET /api/parents/children
```

### 2. ChildAttendance.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Select child dropdown
- Monthly attendance calendar
- Attendance percentage
- Present/Absent/Late details

**API Calls needed:**
```javascript
- getChildAttendance(studentId) → GET /api/parents/child/{student_id}/attendance
- getAttendanceByMonth(studentId, month) → GET /api/parents/child/{student_id}/attendance?month={month}
```

### 3. ChildGrades.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Select child dropdown
- Grade history
- Subject-wise grades
- GPA/percentage

**API Calls needed:**
```javascript
- getChildGrades(studentId) → GET /api/parents/child/{student_id}/grades
- getGradeHistory(studentId) → GET /api/parents/child/{student_id}/grades/history
```

### 4. ChildFees.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Fee structure for child
- Payment history
- Pending payments
- Payment form

**API Calls needed:**
```javascript
- getChildFees(studentId) → GET /api/fees/student/{student_id}
- getFeeStructure() → GET /api/fees/structure
- makePayment(feeId, data) → POST /api/fees/{id}/pay
```

### 5. Notices.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Notices relevant to parent
- Date, title, content
- Mark as read

**API Calls needed:**
```javascript
- getParentNotices() → GET /api/parents/notices
```

### 6. Chat.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Chat with teachers
- Message history
- Send/receive messages

**API Calls needed:**
```javascript
- getChatContacts() → GET /api/parents/chat
- getMessages(contactId) → GET /api/chat/messages/{contact_id}
- sendMessage(data) → POST /api/chat/messages
```

### 7. Profile.jsx
**Status:** ❌ MISSING
**Features to implement:**
- View profile
- Edit profile
- Link/unlink children
- Change password

**API Calls needed:**
```javascript
- getProfile() → GET /api/parents/me
- updateProfile(data) → PUT /api/parents/{id}
- linkChild(studentId, relation) → POST /api/parents/children/link
- unlinkChild(studentId) → DELETE /api/parents/children/{id}
```

## Data Schemas

### Parent Profile
```javascript
{
  id: number,
  user_id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone: string,
  address: string,
  occupation: string,
  children: [
    {
      student_id: number,
      student_name: string,
      class: string,
      section: string,
      relation: string  // father, mother, guardian
    }
  ]
}
```

### Child Attendance
```javascript
{
  student_id: number,
  student_name: string,
  month: string,
  total_days: number,
  present: number,
  absent: number,
  late: number,
  percentage: number,
  details: [
    {
      date: string,
      status: "present" | "absent" | "late"
    }
  ]
}
```

### Child Grade
```javascript
{
  student_id: number,
  student_name: string,
  grades: [
    {
      id: number,
      subject: string,
      score: number,
      grade: string,
      semester: string,
      exam_type: string
    }
  ],
  gpa: number,
  percentage: number
}
```

### Fee Record
```javascript
{
  id: number,
  student_id: number,
  student_name: string,
  fee_type: string,
  amount: number,
  due_date: string,
  paid_amount: number,
  paid_date?: string,
  status: "paid" | "pending" | "overdue"
}
```

## Implementation Order
1. ❌ Dashboard - First
2. ❌ ChildAttendance - Second
3. ❌ ChildGrades - Third
4. ❌ ChildFees - Fourth
5. ❌ Notices - Fifth
6. ❌ Chat - Sixth
7. ❌ Profile - Seventh

## Notes
- Parent module is 0% complete - needs full implementation
- First need to create api/parents.js
- Parent can link to multiple children
- Key feature: View child's academic progress
