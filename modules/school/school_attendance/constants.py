"""
School Attendance Constants

Module-specific constants for school attendance.
"""

# Attendance Status Constants
ATTENDANCE_STATUS_PRESENT = "present"
ATTENDANCE_STATUS_ABSENT = "absent"
ATTENDANCE_STATUS_LATE = "late"
ATTENDANCE_STATUS_EXCUSED = "excused"

ATTENDANCE_STATUSES = [
    ATTENDANCE_STATUS_PRESENT,
    ATTENDANCE_STATUS_ABSENT,
    ATTENDANCE_STATUS_LATE,
    ATTENDANCE_STATUS_EXCUSED,
]

# Attendance Types
ATTENDANCE_TYPE_DAILY = "daily"
ATTENDANCE_TYPE_PERIOD = "period"

# Default Settings
DEFAULT_ATTENDANCE_CUTOFF_HOUR = 10  # 10 AM - students arriving after are marked late
LATE_ARRIVAL_MINUTES = 15  # Minutes after scheduled time to mark late

# Permission Constants
CAN_MARK_ATTENDANCE = "attendance:mark"
CAN_VIEW_ATTENDANCE = "attendance:view"
CAN_VIEW_REPORTS = "attendance:reports"
CAN_EXPORT_ATTENDANCE = "attendance:export"

# Route Names
ROUTE_ATTENDANCE_HOME = "attendance:home"
ROUTE_MARK_ATTENDANCE = "attendance:mark"
ROUTE_CLASS_ATTENDANCE = "attendance:class"
ROUTE_STUDENT_ATTENDANCE = "attendance:student"
ROUTE_ATTENDANCE_REPORTS = "attendance:reports"

# Template Paths
TEMPLATE_ATTENDANCE_INDEX = "attendance/index.html"
TEMPLATE_ATTENDANCE_CLASS = "attendance/class.html"
TEMPLATE_ATTENDANCE_STUDENT = "attendance/student.html"
TEMPLATE_ATTENDANCE_MARK = "attendance/mark.html"
TEMPLATE_ATTENDANCE_REPORTS = "attendance/reports.html"

# Messages
MSG_ATTENDANCE_MARKED = "Attendance marked successfully"
MSG_ATTENDANCE_UPDATED = "Attendance updated successfully"
MSG_SESSION_CREATED = "Attendance session created"
MSG_ALREADY_MARKED = "Attendance already marked for this student"
MSG_SESSION_NOT_FOUND = "Attendance session not found"

# Validation
MINIMUM_ATTENDANCE_PERCENTAGE = 75.0  # Minimum required attendance percentage
ATTENDANCE_WARNING_THRESHOLD = 80.0  # Warning when below this percentage
