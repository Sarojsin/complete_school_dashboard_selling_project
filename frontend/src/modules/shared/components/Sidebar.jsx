import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const roleBasedLinks = {
  student: [
    { path: '/student/dashboard', label: 'Dashboard', icon: 'speedometer2' },
    { path: '/student/courses', label: 'Courses', icon: 'book' },
    { path: '/student/assignments', label: 'Assignments', icon: 'journal-text' },
    { path: '/student/grades', label: 'Grades', icon: 'graph-up' },
    { path: '/student/attendance', label: 'Attendance', icon: 'calendar-check' },
    { path: '/student/timetable', label: 'Timetable', icon: 'calendar-week' },
    { path: '/student/notes', label: 'Study Materials', icon: 'journal' },
    { path: '/student/videos', label: 'Videos', icon: 'play-circle' },
    { path: '/student/library', label: 'Library', icon: 'book-half' },
    { path: '/student/fees', label: 'Fees', icon: 'cash-coin' },
    { path: '/student/notices', label: 'Notices', icon: 'megaphone' },
    { path: '/student/messages', label: 'Messages', icon: 'chat-dots' },
    { path: '/student/groups', label: 'Groups', icon: 'people' },
    { path: '/student/profile', label: 'Profile', icon: 'person' },
  ],
  teacher: [
    { path: '/teacher/dashboard', label: 'Dashboard', icon: 'speedometer2' },
    { path: '/teacher/students', label: 'Students', icon: 'people' },
    { path: '/teacher/courses', label: 'Courses', icon: 'book' },
    { path: '/teacher/assignments', label: 'Assignments', icon: 'journal-text' },
    { path: '/teacher/grades', label: 'Grades', icon: 'graph-up' },
    { path: '/teacher/attendance', label: 'Attendance', icon: 'calendar-check' },
    { path: '/teacher/tests', label: 'Tests', icon: 'pencil-square' },
    { path: '/teacher/timetable', label: 'Timetable', icon: 'calendar3' },
    { path: '/teacher/chat', label: 'Chat', icon: 'chat-dots' },
    { path: '/teacher/groups', label: 'Groups', icon: 'people-fill' },
    { path: '/teacher/notices', label: 'Notices', icon: 'megaphone' },
    { path: '/teacher/profile', label: 'Profile', icon: 'person' },
  ],
  authority: [
    { path: '/authority/dashboard', label: 'Dashboard', icon: 'speedometer2' },
    { path: '/authority/students', label: 'Students', icon: 'people' },
    { path: '/authority/teachers', label: 'Teachers', icon: 'person-badge' },
    { path: '/authority/courses', label: 'Courses', icon: 'book' },
    { path: '/authority/fees', label: 'Fee Management', icon: 'cash-coin' },
    { path: '/authority/notices', label: 'Notices', icon: 'megaphone' },
    { path: '/authority/analytics', label: 'Analytics', icon: 'graph-up' },
    { path: '/authority/groups', label: 'Groups', icon: 'people-fill' },
    { path: '/authority/departments', label: 'Departments', icon: 'building' },
  ],
  parent: [
    { path: '/parent/dashboard', label: 'Dashboard', icon: 'speedometer2' },
    { path: '/parent/child/attendance', label: 'Child Attendance', icon: 'calendar-check' },
    { path: '/parent/child/grades', label: 'Child Grades', icon: 'graph-up' },
    { path: '/parent/child/fees', label: 'Child Fees', icon: 'cash-coin' },
    { path: '/parent/notices', label: 'Notices', icon: 'megaphone' },
    { path: '/parent/chat', label: 'Chat', icon: 'chat-dots' },
    { path: '/parent/profile', label: 'Profile', icon: 'person' },
  ],
  superadmin: [
    { path: '/superadmin/dashboard', label: 'Command Center', icon: 'grid-view' },
    { path: '/superadmin/users', label: 'User Management', icon: 'people' },
    { path: '/superadmin/academic', label: 'Academic', icon: 'school' },
    { path: '/superadmin/finance', label: 'Finance', icon: 'payments' },
    { path: '/superadmin/features', label: 'Feature Matrix', icon: 'vitals' },
    { path: '/superadmin/audit', label: 'Audit Spectrum', icon: 'history' },
    { path: '/superadmin/settings', label: 'System Tuning', icon: 'gear' },
    { path: '/superadmin/system', label: 'System Monitor', icon: 'memory' },
    { path: '/superadmin/security', label: 'Security Control', icon: 'shield-check' },
    { path: '/superadmin/backups', label: 'Backups', icon: 'backup' },
    { path: '/superadmin/reports', label: 'Reports', icon: 'file-earmark-text' },
  ],
};

export default function Sidebar() {
  const location = useLocation();
  const userRole = localStorage.getItem('userRole') || 'student';
  
  const links = roleBasedLinks[userRole] || roleBasedLinks.student;

  return (
    <aside className="sidebar-enhanced">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <i className="bi bi-mortarboard-fill"></i>
        </div>
        <h2 className="sidebar-title">School MS</h2>
      </div>
      
      <div className="sidebar-section">
        <span className="sidebar-section-title">MAIN MENU</span>
      </div>
      
      <nav className="sidebar-nav">
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className={`sidebar-link ${location.pathname === link.path ? 'active' : ''}`}
          >
            <i className={`bi bi-${link.icon}`}></i>
            <span>{link.label}</span>
          </Link>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <Link to="/logout" className="sidebar-link">
          <i className="bi bi-box-arrow-right"></i>
          <span>Logout</span>
        </Link>
      </div>
    </aside>
  );
}
