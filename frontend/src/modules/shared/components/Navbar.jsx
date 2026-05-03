import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get user info from localStorage (set after login)
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h3>School Management System</h3>
      </div>
      <div className="navbar-right">
        {user ? (
          <div className="user-info">
            <span className="user-name">{user.full_name || user.username}</span>
            <span className="user-role">{user.role}</span>
            <Link to="/profile" className="profile-link">Profile</Link>
          </div>
        ) : (
          <Link to="/login" className="login-link">Login</Link>
        )}
      </div>
    </nav>
  );
}
