import { useState, useEffect } from 'react';
import api from '../../../shared/api/client';
import Card from '../../../shared/components/Card';
import Badge from '../../../shared/components/Badge';
import './StudentTeachers.css';

const StudentTeachers = () => {
  const [teachers, setTeachers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDepartment, setFilterDepartment] = useState('all');

  // Mock data for demonstration
  const mockTeachers = [
    { id: 1, name: 'Dr. Sarah Johnson', subject: 'Data Structures', department: 'Computer Science', email: 'sarah.johnson@school.edu', phone: '+1 234-567-8901', avatar: null, qualification: 'Ph.D. in Computer Science', experience: '8 years', rating: 4.8 },
    { id: 2, name: 'Prof. Michael Chen', subject: 'Algorithms', department: 'Computer Science', email: 'michael.chen@school.edu', phone: '+1 234-567-8902', avatar: null, qualification: 'M.Tech, IIT Bombay', experience: '12 years', rating: 4.9 },
    { id: 3, name: 'Dr. Emily Williams', subject: 'Linear Algebra', department: 'Mathematics', email: 'emily.williams@school.edu', phone: '+1 234-567-8903', avatar: null, qualification: 'Ph.D. in Mathematics', experience: '6 years', rating: 4.7 },
    { id: 4, name: 'Prof. David Miller', subject: 'Physics I', department: 'Physics', email: 'david.miller@school.edu', phone: '+1 234-567-8904', avatar: null, qualification: 'M.Sc. Physics', experience: '10 years', rating: 4.6 },
    { id: 5, name: 'Ms. Jessica Brown', subject: 'Technical Writing', department: 'English', email: 'jessica.brown@school.edu', phone: '+1 234-567-8905', avatar: null, qualification: 'M.A. English', experience: '5 years', rating: 4.5 },
    { id: 6, name: 'Dr. Robert Taylor', subject: 'Database Systems', department: 'Computer Science', email: 'robert.taylor@school.edu', phone: '+1 234-567-8906', avatar: null, qualification: 'Ph.D. in Data Science', experience: '9 years', rating: 4.8 },
  ];

  const departments = ['All', 'Computer Science', 'Mathematics', 'Physics', 'English', 'Chemistry'];

  const getAvatarUrl = (avatar, name) => {
    if (avatar) return avatar.startsWith('http') ? avatar : `/uploads/avatars/${avatar}`;
    // Generate initials avatar
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&color=fff`;
  };

  const filteredTeachers = mockTeachers.filter(teacher => {
    const matchesSearch = teacher.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      teacher.subject?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDept = filterDepartment === 'all' || teacher.department === filterDepartment;
    return matchesSearch && matchesDept;
  });

  useEffect(() => {
    loadTeachers();
  }, []);

  const loadTeachers = async () => {
    try {
      const response = await api.get('/student/teachers');
      setTeachers(response.data || mockTeachers);
    } catch (err) {
      console.error('Failed to load teachers:', err);
      setTeachers(mockTeachers);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="teachers-loading">Loading teachers...</div>;
  }

  return (
    <div className="student-teachers-page">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>My Teachers</h1>
          <p className="text-muted mb-0">View your teachers and their details</p>
        </div>
        <div className="d-flex gap-2">
          <select 
            className="form-select form-select-sm" 
            value={filterDepartment} 
            onChange={(e) => setFilterDepartment(e.target.value)}
            style={{ width: 'auto' }}
          >
            {departments.map(dept => (
              <option key={dept} value={dept === 'All' ? 'all' : dept}>{dept}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Search Bar */}
      <Card className="mb-4">
        <div className="row g-3">
          <div className="col-md-6">
            <div className="input-group">
              <span className="input-group-text bg-white">
                <i className="bi bi-search"></i>
              </span>
              <input
                type="text"
                className="form-control"
                placeholder="Search teachers by name or subject..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
          <div className="col-md-6">
            <div className="d-flex align-items-center">
              <span className="text-muted me-2">
                <i className="bi bi-people me-1"></i>
                {filteredTeachers.length} teachers found
              </span>
            </div>
          </div>
        </div>
      </Card>

      {/* Teachers Grid */}
      <div className="row g-4">
        {filteredTeachers.length === 0 ? (
          <div className="col-12">
            <Card>
              <div className="text-center py-5">
                <i className="bi bi-person-x display-4 text-muted"></i>
                <h5 className="text-muted mt-3">No Teachers Found</h5>
                <p className="text-muted small">No teachers match your search criteria</p>
                <button className="btn btn-sm btn-outline-primary mt-2" onClick={() => {setSearchQuery(''); setFilterDepartment('all');}}>
                  Clear Filters
                </button>
              </div>
            </Card>
          </div>
        ) : (
          filteredTeachers.map((teacher) => (
            <div className="col-md-6 col-lg-4" key={teacher.id}>
              <Card className="h-100">
                <div className="card-body">
                  <div className="text-center mb-3">
                    <img 
                      src={getAvatarUrl(teacher.avatar, teacher.name)} 
                      alt={teacher.name}
                      className="rounded-circle mb-3"
                      style={{ width: '80px', height: '80px', objectFit: 'cover' }}
                    />
                    <h5 className="mb-1">{teacher.name}</h5>
                    <Badge variant="primary">{teacher.subject}</Badge>
                  </div>
                  
                  <div className="teacher-details mt-3">
                    <div className="d-flex align-items-center mb-2">
                      <i className="bi bi-mortarboard text-muted me-2"></i>
                      <span className="small">{teacher.qualification}</span>
                    </div>
                    <div className="d-flex align-items-center mb-2">
                      <i className="bi bi-briefcase text-muted me-2"></i>
                      <span className="small">{teacher.experience} experience</span>
                    </div>
                    <div className="d-flex align-items-center mb-2">
                      <i className="bi bi-envelope text-muted me-2"></i>
                      <span className="small text-truncate">{teacher.email}</span>
                    </div>
                    <div className="d-flex align-items-center mb-3">
                      <i className="bi bi-telephone text-muted me-2"></i>
                      <span className="small">{teacher.phone}</span>
                    </div>
                    
                    <div className="d-flex justify-content-between align-items-center">
                      <div className="rating">
                        <i className="bi bi-star-fill text-warning"></i>
                        <span className="ms-1 small fw-bold">{teacher.rating}</span>
                      </div>
                      <Badge variant={teacher.department === 'Computer Science' ? 'info' : 'secondary'}>
                        {teacher.department}
                      </Badge>
                    </div>
                  </div>
                </div>
                <div className="card-footer bg-transparent border-top-0">
                  <div className="d-grid gap-2">
                    <button className="btn btn-outline-primary btn-sm">
                      <i className="bi bi-chat-dots me-2"></i>Send Message
                    </button>
                    <button className="btn btn-outline-secondary btn-sm">
                      <i className="bi bi-calendar-check me-2"></i>Request Meeting
                    </button>
                  </div>
                </div>
              </Card>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default StudentTeachers;
