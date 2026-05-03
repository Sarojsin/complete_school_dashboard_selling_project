import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const PrivateRoute = ({ 
  children, 
  allowedRoles = null, 
  allowedPortal = null,
  redirectTo = '/login' 
}) => {
  const token = localStorage.getItem('access_token');
  const userJson = localStorage.getItem('user');
  const location = useLocation();

  if (!token) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  let user = null;
  try {
    user = userJson ? JSON.parse(userJson) : null;
  } catch (e) {}

  if (!user) {
    return <Navigate to={redirectTo} replace />;
  }

  // Check portal type restriction
  if (allowedPortal && user.portal_type !== allowedPortal) {
    // Redirect to appropriate dashboard based on actual portal
    const portalDashboard = user.portal_type === 'college' 
      ? '/college/teacher/dashboard'  // fallback; actual redirect will be handled by DashboardRedirector after login
      : '/teacher/dashboard';
    return <Navigate to={portalDashboard} replace />;
  }

  // Check role restriction
  if (allowedRoles && user.role && !allowedRoles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default PrivateRoute;
