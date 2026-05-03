import React, { useState } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import {
  signupStudent,
  signupCollegeStudent,
  signupTeacher,
  signupCollegeTeacher,
  signupAuthority,
  signupCollegeAuthority,
  signupParent,
  signupAdmin,
  signupHOD,
  signupExamSection,
  signupLibrary,
  signupAccount
} from '../api/signup';
import '../styles/auth.css';

const roles = [
  { value: 'student', label: 'Student', icon: '🎓', description: 'Join as a student' },
  { value: 'teacher', label: 'Teacher', icon: '👨‍🏫', description: 'Join as a teacher' },
  { value: 'authority', label: 'Authority', icon: '🛡️', description: 'School/College Authority' },
  { value: 'account_section', label: 'Account Section', icon: '💰', description: 'Financial Management' },
  { value: 'exam_section', label: 'Exam Section', icon: '📝', description: 'Examination Management' },
  { value: 'parent', label: 'Parent', icon: '👨‍👩‍👧', description: 'Parent/Guardian' },
  { value: 'others', label: 'HOD/Staff', icon: '👥', description: 'Other departments' },
];

export default function SignupPage() {
  const [searchParams] = useSearchParams();
  const initialRole = searchParams.get('role');
  const selectedSystem = searchParams.get('system') || 'school';
  const [selectedRole, setSelectedRole] = useState(initialRole || null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    // Student specific
    grade_level: '',
    student_id: '',
    // Teacher/HOD specific
    employee_id: '',
    // Teacher/Authority/Account/Exam/HOD specific
    department: '',
    secret_key: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Effect to update selectedRole if URL param changes
  React.useEffect(() => {
    if (initialRole) {
      setSelectedRole(initialRole);
    }
  }, [initialRole]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      const signupData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
        portal_type: selectedSystem,  // indicate school or college
      };

      // Add role-specific fields
      if (selectedRole === 'student') {
        signupData.grade_level = formData.grade_level;
        signupData.student_id = formData.student_id;
      } else if (['teacher', 'others'].includes(selectedRole)) {
        signupData.department = formData.department;
        signupData.employee_id = formData.employee_id;
      } else if (['account_section', 'exam_section'].includes(selectedRole)) {
        signupData.department = formData.department;
        signupData.secret_key = formData.secret_key;
      } else if (selectedRole === 'authority') {
        signupData.secret_key = formData.secret_key;
        signupData.department = formData.department;
      } else if (selectedRole === 'parent') {
        signupData.student_id = formData.student_id;
      }

       // Route to appropriate endpoint based on portal AND role
       if (selectedSystem === 'college') {
         // College signup endpoints
         switch (selectedRole) {
           case 'student':
             await signupCollegeStudent(signupData);
             break;
           case 'teacher':
             await signupCollegeTeacher(signupData);
             break;
           case 'authority':
           case 'account_section':
           case 'exam_section':
             // College authorities use the college authority endpoint
             await signupCollegeAuthority(signupData);
             break;
           case 'others':
             // College HOD also uses college authority endpoint
             await signupCollegeAuthority(signupData);
             break;
           case 'parent':
             // College parent? Could use same endpoint if profile structure matches
             // For now, regular parent endpoint but with college portal_type
             await signupParent(signupData);
             break;
           default:
             throw new Error('Role not supported for college portal');
         }
       } else {
         // School signup endpoints (existing code)
         switch (selectedRole) {
           case 'student':
             await signupStudent(signupData);
             break;
           case 'teacher':
             await signupTeacher(signupData);
             break;
           case 'authority':
             await signupAuthority(signupData);
             break;
           case 'account_section':
             await signupAccount(signupData);
             break;
           case 'exam_section':
             await signupExamSection(signupData);
             break;
           case 'parent':
             await signupParent(signupData);
             break;
           case 'others':
             // Default to HOD for others or handle specifically
             await signupHOD(signupData);
             break;
           default:
             throw new Error('Invalid role');
         }
       }

      // Redirect to login after successful signup
      navigate('/login');
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        // Handle FastAPI validation errors (array of objects)
        const messages = detail.map(err => `${err.loc[err.loc.length - 1]}: ${err.msg}`);
        setError(messages.join(', '));
      } else if (typeof detail === 'string') {
        setError(detail);
      } else {
        setError('Signup failed. Please ensure all fields are correct.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (!selectedRole) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h2>Create Account</h2>
          <p>Select your role to get started</p>
          
          <div className="role-selection">
            {roles.map((role) => (
              <button
                key={role.value}
                className="role-card"
                onClick={() => setSelectedRole(role.value)}
              >
                <span className="role-icon">{role.icon}</span>
                <span className="role-label">{role.label}</span>
                <span className="role-desc">{role.description}</span>
              </button>
            ))}
          </div>
          
          <p className="text-center mt-3">
            Already have an account? <Link to="/login">Sign In</Link>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <button className="back-btn" onClick={() => setSelectedRole(null)}>
          ← Back
        </button>
        
        <h2>{roles.find(r => r.value === selectedRole)?.label} Registration</h2>
        <p>Create your {selectedRole} account for the <span className="highlight">{selectedSystem.toUpperCase()}</span> system</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={6}
            />
          </div>
          
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </div>

          {/* Role-specific fields */}
          {selectedRole === 'student' && (
            <>
              <div className="form-group">
                <label>Student ID</label>
                <input
                  type="text"
                  name="student_id"
                  value={formData.student_id}
                  onChange={handleChange}
                  required
                  placeholder="Official Student ID"
                />
              </div>
              <div className="form-group">
                <label>Grade Level</label>
                <select
                  name="grade_level"
                  value={formData.grade_level}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Grade</option>
                  <option value="1">Class 1</option>
                  <option value="2">Class 2</option>
                  <option value="3">Class 3</option>
                  <option value="4">Class 4</option>
                  <option value="5">Class 5</option>
                  <option value="6">Class 6</option>
                  <option value="7">Class 7</option>
                  <option value="8">Class 8</option>
                  <option value="9">Class 9</option>
                  <option value="10">Class 10</option>
                  <option value="11">Class 11</option>
                  <option value="12">Class 12</option>
                </select>
              </div>
            </>
          )}

          {['teacher', 'others'].includes(selectedRole) && (
            <div className="form-group">
              <label>Employee ID</label>
              <input
                type="text"
                name="employee_id"
                value={formData.employee_id}
                onChange={handleChange}
                required
                placeholder="Official Staff ID"
              />
            </div>
          )}

          {['authority', 'account_section', 'exam_section'].includes(selectedRole) && (
            <div className="form-group">
              <label>Secret Key</label>
              <input
                type="password"
                name="secret_key"
                value={formData.secret_key}
                onChange={handleChange}
                required
                placeholder="Enter security/secret key"
              />
            </div>
          )}

          {['teacher', 'account_section', 'exam_section', 'others'].includes(selectedRole) && (
            <div className="form-group">
              <label>Department / Section</label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                required
                placeholder="e.g., Mathematics, Finance, Exams"
              />
            </div>
          )}

          {selectedRole === 'parent' && (
            <div className="form-group">
              <label>Student ID</label>
              <input
                type="text"
                name="student_id"
                value={formData.student_id}
                onChange={handleChange}
                required
                placeholder="Enter your child's student ID"
              />
            </div>
          )}
          
          <button type="submit" disabled={loading}>
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>
        
        <p className="text-center mt-3">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  );
}
