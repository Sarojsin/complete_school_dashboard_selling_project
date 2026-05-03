import React, { useEffect, useState } from 'react';
import { getCollegeStudentProfile, getCollegeStudentCourses, getCollegeStudentGrades } from '../../../college/college_student/api/students';
import { logout } from '../../../auth/api/auth';
import { useNavigate } from 'react-router-dom';

export default function StudentDashboard() {
  const [profile, setProfile] = useState(null);
  const [courses, setCourses] = useState([]);
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      getCollegeStudentProfile(),
      getCollegeStudentCourses(),
      getCollegeStudentGrades()
    ])
      .then(([profileRes, coursesRes, gradesRes]) => {
        setProfile(profileRes.data);
        setCourses(coursesRes.data);
        setGrades(gradesRes.data);
      })
      .catch(err => {
        console.error('Failed to load data:', err);
        setError('Failed to load profile');
        // If 403, user might be in wrong portal - redirect to appropriate dashboard
        if (err.response?.status === 403) {
          navigate('/dashboard'); // Let DashboardRedirector handle it
        }
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  if (loading) return <div style={{display:'flex',justifyContent:'center',alignItems:'center',height:'100vh'}}>Loading...</div>;
  if (error) return <div style={{display:'flex',justifyContent:'center',alignItems:'center',height:'100vh',color:'red'}}>{error}</div>;

  return (
    <div style={{ padding: '2rem', background: 'linear-gradient(to bottom, #0f172a, #1e293b)', minHeight: '100vh', color: 'white' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: 0, background: 'linear-gradient(to right, #6366f1, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            College Student Dashboard
          </h1>
          <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>
            Welcome back, {profile?.full_name || 'Student'}
          </p>
        </div>
        <button onClick={logout} style={{ padding: '0.75rem 1.5rem', background: '#6366f1', color: 'white', border: 'none', borderRadius: '0.5rem', cursor: 'pointer', fontWeight: '500' }}>
          Logout
        </button>
      </div>

      {profile && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          <div style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '1rem', padding: '1.5rem' }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#818cf8' }}>Profile Information</h3>
            <p><strong>Roll Number:</strong> {profile.roll_number}</p>
            <p><strong>CGPA:</strong> {profile.cgpa}</p>
            <p><strong>Credits Completed:</strong> {profile.total_credits_completed}</p>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '1rem', padding: '1.5rem' }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#818cf8' }}>Quick Stats</h3>
            <p><strong>Current Courses:</strong> {courses.length}</p>
            <p><strong>Grades Released:</strong> {grades.length}</p>
          </div>
        </div>
      )}

      <div style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '1rem', padding: '1.5rem' }}>
        <h3 style={{ margin: '0 0 1rem 0', color: '#818cf8' }}>My Courses</h3>
        {courses.length === 0 ? (
          <p style={{ color: '#94a3b8' }}>No courses enrolled yet.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {courses.map(course => (
              <li key={course.id} style={{ padding: '0.75rem', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                {course.course_name || course.name || `Course ${course.id}`}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
