# Migration Phase 5: Restructure Templates

**Duration:** 2-3 days  
**Goal:** Organize HTML templates into school/college folders

---

## Overview

Phase 5 reorganizes the templates directory to follow the new structure with separate folders for school and college templates.

---

## Current State

```
app/templates/
├── base.html
├── index.html
├── auth/
│   ├── login.html
│   └── signup.html
├── student/
│   ├── dashboard.html
│   ├── profile.html
│   └── ...
├── teacher/
├── authority/
├── parent/
├── hod/
├── exam_section/
├── library/
├── account/
├── admin/
└── groups/
```

---

## Target State After Phase 5

```
app/templates/
├── base.html
├── index.html
├── auth/
│   ├── login.html
│   └── signup.html
│
├── school/                    # ← NEW: School templates
│   ├── base.html
│   ├── authority/
│   │   ├── dashboard.html
│   │   ├── list.html
│   │   └── detail.html
│   ├── teacher/
│   │   ├── dashboard.html
│   │   ├── attendance.html
│   │   ├── assignments.html
│   │   └── ...
│   ├── student/
│   │   ├── dashboard.html
│   │   ├── timetable.html
│   │   ├── assignments.html
│   │   └── ...
│   ├── parent/
│   │   ├── dashboard.html
│   │   └── child_progress.html
│   ├── exam_section/
│   ├── account_section/
│   └── library/
│
└── college/                  # ← NEW: College templates
    ├── base.html
    ├── dean/
    │   └── dashboard.html
    ├── hod/
    │   └── dashboard.html
    ├── faculty/
    │   ├── dashboard.html
    │   └── courses.html
    ├── student/
    │   ├── dashboard.html
    │   ├── courses.html
    │   ├── grades.html
    │   └── ...
    ├── registrar/
    ├── exam_section/
    ├── account_section/
    ├── library/
    ├── placement/
    ├── research/
    ├── hostel/
    └── lab/
```

---

## Step-by-Step Tasks

### Step 1: Create School Directory Structure

Create folders:
```
app/templates/school/
app/templates/school/authority/
app/templates/school/teacher/
app/templates/school/student/
app/templates/school/parent/
app/templates/school/exam_section/
app/templates/school/account_section/
app/templates/school/library/
```

### Step 2: Move Templates to School

#### 2.1 Authority Templates
**Move: `app/templates/authority/`**  
**To: `app/templates/school/authority/`**

#### 2.2 Teacher Templates
**Move: `app/templates/teacher/`**  
**To: `app/templates/school/teacher/`**

#### 2.3 Student Templates
**Move: `app/templates/student/`**  
**To: `app/templates/school/student/`**

#### 2.4 Parent Templates
**Move: `app/templates/parent/`**  
**To: `app/templates/school/parent/`**

#### 2.5 Exam Section Templates
**Move: `app/templates/exam_section/`**  
**To: `app/templates/school/exam_section/`**

#### 2.6 Account Templates
**Move: `app/templates/account/`**  
**To: `app/templates/school/account_section/`**

#### 2.7 Library Templates
**Move: `app/templates/library/`**  
**To: `app/templates/school/library/`

### Step 3: Create College Directory Structure

Create folders:
```
app/templates/college/
app/templates/college/dean/
app/templates/college/hod/
app/templates/college/faculty/
app/templates/college/student/
app/templates/college/registrar/
app/templates/college/exam_section/
app/templates/college/account_section/
app/templates/college/library/
app/templates/college/placement/
app/templates/college/research/
app/templates/college/hostel/
app/templates/college/lab/
```

### Step 4: Move/Create College Templates

#### 4.1 HOD Templates
**Move: `app/templates/hod/`**  
**To: `app/templates/college/hod/`

#### 4.2 Create Dean Templates
**Create: `app/templates/college/dean/dashboard.html`**
```html
{% extends "college/base.html" %}

{% block content %}
<div class="dean-dashboard">
    <h2>Dean Dashboard</h2>
    
    <div class="stats">
        <div class="stat-card">
            <h3>Departments</h3>
            <p>{{ department_count }}</p>
        </div>
        <div class="stat-card">
            <h3>Faculty</h3>
            <p>{{ faculty_count }}</p>
        </div>
        <div class="stat-card">
            <h3>Students</h3>
            <p>{{ student_count }}</p>
        </div>
    </div>
    
    <div class="sections">
        <section>
            <h3>Department Overview</h3>
            <!-- Department list -->
        </section>
        <section>
            <h3>Recent Activities</h3>
            <!-- Activity feed -->
        </section>
    </div>
</div>
{% endblock %}
```

#### 4.3 Create Faculty Templates
**Create: `app/templates/college/faculty/`**
- `dashboard.html`
- `courses.html`
- `students.html`
- `research.html`

#### 4.4 Create College Student Templates
**Create: `app/templates/college/student/`**
- `dashboard.html`
- `courses.html` (with course registration)
- `grades.html` (GPA display)
- `timetable.html`
- `enrollments.html`

#### 4.5 Create Registrar Templates
**Create: `app/templates/college/registrar/`**
- `dashboard.html`
- `enrollments.html`
- `transcripts.html`
- `certificates.html`

#### 4.6 Create Placement Templates
**Create: `app/templates/college/placement/`**
- `dashboard.html`
- `companies.html`
- `jobs.html`
- `applications.html`

#### 4.7 Create Research Templates
**Create: `app/templates/college/research/`**
- `dashboard.html`
- `projects.html`
- `publications.html`

#### 4.8 Create Hostel Templates
**Create: `app/templates/college/hostel/`**
- `dashboard.html`
- `rooms.html`
- `allocations.html`
- `complaints.html`

#### 4.9 Create Lab Templates
**Create: `app/templates/college/lab/`**
- `dashboard.html`
- `equipment.html`
- `bookings.html`

### Step 5: Create Base Templates

#### 5.1 School Base Template
**Create: `app/templates/school/base.html`**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}School Portal{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/school.css">
</head>
<body>
    <nav>
        <a href="/school/authority">Dashboard</a>
        <a href="/school/students">Students</a>
        <a href="/school/teachers">Teachers</a>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

#### 5.2 College Base Template
**Create: `app/templates/college/base.html`**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}College Portal{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/college.css">
</head>
<body>
    <nav>
        <a href="/college/dean">Dashboard</a>
        <a href="/college/faculty">Faculty</a>
        <a href="/college/students">Students</a>
        <a href="/college/placements">Placements</a>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### Step 6: Update Web Routes

**Modify: `app/web/routes/`**

Update routes to point to new template locations:
```python
# Old
return templates.TemplateResponse("student/dashboard.html", {...})

# New
return templates.TemplateResponse("school/student/dashboard.html", {...})
```

---

## Files to Move Summary

| Current Location | New Location |
|-----------------|---------------|
| `templates/authority/` | `templates/school/authority/` |
| `templates/teacher/` | `templates/school/teacher/` |
| `templates/student/` | `templates/school/student/` |
| `templates/parent/` | `templates/school/parent/` |
| `templates/exam_section/` | `templates/school/exam_section/` |
| `templates/account/` | `templates/school/account_section/` |
| `templates/library/` | `templates/school/library/` |
| `templates/hod/` | `templates/college/hod/` |

---

## Files to Create Summary

| File | Purpose |
|------|---------|
| `templates/school/base.html` | School base template |
| `templates/college/base.html` | College base template |
| `templates/college/dean/*` | Dean templates |
| `templates/college/faculty/*` | Faculty templates |
| `templates/college/student/*` | College student templates |
| `templates/college/registrar/*` | Registrar templates |
| `templates/college/placement/*` | Placement templates |
| `templates/college/research/*` | Research templates |
| `templates/college/hostel/*` | Hostel templates |
| `templates/college/lab/*` | Lab templates |

---

## Verification Checklist

- [ ] School templates organized
- [ ] College templates created
- [ ] Base templates working
- [ ] Web routes updated
- [ ] All pages render correctly
- [ ] Navigation works

---

## Next Phase

After Phase 5 → Go to [Phase 6: Create College Features](migration_phase6.md)

---

*End of Phase 5*
