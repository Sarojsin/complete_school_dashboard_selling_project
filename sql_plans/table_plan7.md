# Table Plan 7: Student Welfare & Discipline

## Overview
Student counseling, disciplinary tracking, leave management, and welfare programs.

## Tables (12)

### Counseling & Support
- `college_student_counseling` - Mental health and academic counseling sessions
- `college_counseling_categories` - Counseling type taxonomy
- `college_student_welfare_programs` - Support initiatives enrollment
- `college_student_leave_applications` - Leave requests and approvals
- `college_student_warnings` - Academic and behavioral warnings

### Discipline Management
- `school_disciplinary_actions` - Incident reports and consequences
- `school_disciplinary_categories` - Violation types and severity levels
- `school_disciplinary_hearings` - Review board proceedings and decisions
- `school_disciplinary_appeals` - Student/family appeal processes

### Health & Medical
- `school_student_health_records` - Medical history and conditions
- `school_vaccination_records` - Immunization tracking
- `school_medical_visits` - On-campus medical visits log
- `school_health_announcements` - Health alerts and advisories

### Additional Welfare
- `student_special_needs` - Accommodations and support requirements
- `student_safety_incidents` - Accident and incident reporting

## Dependencies
- Requires `college_students` and `college_teachers`
- May require `college_parents` for notifications

## Estimated Complexity
High - Sensitive data handling, privacy compliance, and workflow approvals.