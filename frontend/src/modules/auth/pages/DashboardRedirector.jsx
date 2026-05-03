import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DashboardRedirector = () => {
  const navigate = useNavigate();
  const [portalType, setPortalType] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login', { replace: true });
      return;
    }

    let user = null;
    try {
      user = JSON.parse(localStorage.getItem('user') || 'null');
    } catch (e) {}

    if (!user || !user.role) {
      navigate('/login', { replace: true });
      return;
    }

    // Store portal_type for display
    setPortalType(user.portal_type || '');

    const role = String(user.role).toLowerCase();
    const portal = user.portal_type || 'school';

    // Build route based on BOTH role AND portal
    let dashboardRoute;

    if (portal === 'college') {
      // College routes (all prefixed with /college)
      switch (role) {
        case 'faculty':
        case 'teacher':
          dashboardRoute = '/college/teacher/dashboard';
          break;
        case 'hod':
          dashboardRoute = '/college/hod/dashboard';
          break;
        case 'student':
          dashboardRoute = '/college/student/dashboard';
          break;
        case 'dean':
          dashboardRoute = '/college/dean/dashboard';
          break;
        case 'registrar':
          dashboardRoute = '/college/registrar/dashboard';
          break;
        case 'exam_section':
          dashboardRoute = '/college/exam/dashboard';
          break;
        case 'account_section':
          dashboardRoute = '/college/account/dashboard';
          break;
        case 'placement':
          dashboardRoute = '/college/placement/dashboard';
          break;
        case 'research':
          dashboardRoute = '/college/research/dashboard';
          break;
        default:
          // Fallback for other college roles - redirect to student dashboard as default
          dashboardRoute = '/college/student/dashboard';
      }
    } else {
      // School routes (existing - no prefix change)
      switch (role) {
        case 'admin':
        case 'super_admin':
          dashboardRoute = '/admin/dashboard';
          break;
        case 'student':
          dashboardRoute = '/student/dashboard';
          break;
        case 'teacher':
          dashboardRoute = '/teacher/dashboard';
          break;
        case 'parent':
          dashboardRoute = '/parent/dashboard';
          break;
        case 'authority':
          dashboardRoute = '/authority/dashboard';
          break;
        case 'hod':
          dashboardRoute = '/hod/dashboard';
          break;
        case 'exam_section':
          dashboardRoute = '/exam/dashboard';
          break;
        case 'account_section':
          dashboardRoute = '/account/dashboard';
          break;
        case 'library_manager':
          dashboardRoute = '/library/dashboard';
          break;
        default:
          // Fallback for other school roles - redirect to student dashboard
          dashboardRoute = '/student/dashboard';
      }
    }

    navigate(dashboardRoute, { replace: true });
  }, [navigate]);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <h2>Redirecting to your {portalType} dashboard...</h2>
    </div>
  );
};

export default DashboardRedirector;
