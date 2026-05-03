import React, { useState, useEffect } from 'react';
import { getStudentNotices } from '../api/students';
import Card from '../../../shared/components/Card';
import Badge from '../../../shared/components/Badge';

export default function NoticesPage() {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');
  const [selectedNotice, setSelectedNotice] = useState(null);

  // Mock data matching backup/templates
  const categories = ['All', 'Academic', 'Administrative', 'Events', 'Sports', 'Exams'];

  const mockNotices = [
    { id: 1, title: 'Mid-term Examination Schedule', category: 'Exams', author: 'Exam Controller', date: '28 Mar 2024', content: 'The mid-term examinations will be conducted from April 15-25, 2024. All students must follow the detailed schedule provided below. Contact your class teacher for any queries.', priority: 'high' },
    { id: 2, title: 'Library Holiday Closure', category: 'Administrative', author: 'Library Administrator', date: '27 Mar 2024', content: 'The library will remain closed on March 30th for annual maintenance. All borrowed books due on that date will have extended return dates.', priority: 'normal' },
    { id: 3, title: 'Annual Sports Day Announcement', category: 'Sports', author: 'Physical Education Dept', date: '26 Mar 2024', content: 'Annual Sports Day will be held on April 5th, 2024. Register your name for various events by March 31st. Participation certificates will be awarded.', priority: 'normal' },
    { id: 4, title: 'New Course Material Available', category: 'Academic', author: 'Academic Director', date: '25 Mar 2024', content: 'Updated course materials for Data Structures and Algorithms are now available in the digital library. Students can download them from the student portal.', priority: 'normal' },
    { id: 5, title: 'Parent-Teacher Meeting Notice', category: 'Events', author: 'Principal Office', date: '24 Mar 2024', content: 'A parent-teacher meeting is scheduled for April 10th, 2024. Parents are requested to attend and discuss their child\'s progress with respective teachers.', priority: 'high' },
    { id: 6, title: 'Computer Lab Maintenance', category: 'Administrative', author: 'IT Department', date: '23 Mar 2024', content: 'Computer labs will be under maintenance on March 29th. Practical sessions scheduled for that day will be rescheduled.', priority: 'normal' },
  ];

  const importantNotices = mockNotices.filter(n => n.priority === 'high');

  useEffect(() => {
    getStudentNotices()
      .then(setNotices)
      .catch(() => setNotices(mockNotices))
      .finally(() => setLoading(false));
  }, []);

  const filteredNotices = activeTab === 'all' 
    ? mockNotices 
    : mockNotices.filter(n => n.category.toLowerCase() === activeTab.toLowerCase());

  const getCategoryVariant = (category) => {
    const variants = {
      'Academic': 'primary',
      'Administrative': 'secondary',
      'Events': 'info',
      'Sports': 'success',
      'Exams': 'warning',
    };
    return variants[category] || 'secondary';
  };

  const getPriorityVariant = (priority) => {
    return priority === 'high' ? 'danger' : 'secondary';
  };

  if (loading) return <div className="p-4 text-center">Loading notices...</div>;

  return (
    <div className="notices-page">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>Notices & Announcements</h1>
          <p className="text-muted mb-0">Stay updated with the latest news from all departments.</p>
        </div>
      </div>

      {/* Category Tabs */}
      <Card className="mb-4">
        <div className="d-flex gap-2 flex-wrap">
          {categories.map((cat) => (
            <button
              key={cat}
              className={`btn ${activeTab === cat.toLowerCase() ? 'btn-primary' : 'btn-outline-secondary'} fw-bold`}
              onClick={() => setActiveTab(cat.toLowerCase())}
            >
              {cat}
            </button>
          ))}
        </div>
      </Card>

      {/* Important Notices */}
      {activeTab === 'all' && importantNotices.length > 0 && (
        <div className="alert alert-danger border-0 shadow-sm mb-4" style={{ background: 'rgba(239, 68, 68, 0.1)' }}>
          <div className="d-flex align-items-center mb-3">
            <div className="icon-box bg-white text-danger me-3 shadow-sm rounded p-2">
              <i className="bi bi-exclamation-triangle-fill"></i>
            </div>
            <h5 className="mb-0 fw-bold">Priority Announcements</h5>
          </div>
          <div className="row g-3">
            {importantNotices.map((notice) => (
              <div className="col-md-4" key={notice.id}>
                <div 
                  className="card border-0 shadow-sm h-100 cursor-pointer"
                  style={{ cursor: 'pointer' }}
                  onClick={() => setSelectedNotice(notice)}
                >
                  <div className="card-body">
                    <div className="d-flex justify-content-between mb-2">
                      <Badge variant="danger">IMPORTANT</Badge>
                      <small className="text-muted">{notice.date}</small>
                    </div>
                    <h6 className="fw-bold">{notice.title}</h6>
                    <p className="small text-muted mb-0">{notice.content.substring(0, 60)}...</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Notice List */}
      <Card title={activeTab === 'all' ? 'Recent Updates' : `${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Announcements`} icon="bell">
        {filteredNotices.length > 0 ? (
          <div className="list-group">
            {filteredNotices.map((notice) => (
              <div 
                key={notice.id} 
                className="list-group-item list-group-item-action p-3 border-bottom cursor-pointer"
                style={{ cursor: 'pointer' }}
                onClick={() => setSelectedNotice(notice)}
              >
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <h6 className="mb-0 fw-bold">{notice.title}</h6>
                  <small className="text-muted">{notice.date}</small>
                </div>
                <div className="d-flex align-items-center gap-2 mb-2">
                  <Badge variant={getCategoryVariant(notice.category)} className="text-uppercase small">{notice.category}</Badge>
                  <span className="text-muted small">• By {notice.author}</span>
                </div>
                <p className="text-muted small mb-0">{notice.content.substring(0, 120)}...</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-5">
            <i className="bi bi-bell-slash display-4 text-muted"></i>
            <h5 className="text-muted mt-3">No notices in this category</h5>
            <p className="text-muted small">We'll notify you when something new arrives.</p>
            <button className="btn btn-sm btn-outline-primary mt-2" onClick={() => setActiveTab('all')}>
              View All Notices
            </button>
          </div>
        )}
      </Card>

      {/* Notice Detail Modal */}
      {selectedNotice && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} onClick={() => setSelectedNotice(null)}>
          <div className="modal-dialog modal-dialog-centered" onClick={e => e.stopPropagation()}>
            <div className="modal-content border-0 shadow">
              <div className="modal-header border-bottom-0 pb-0">
                <button type="button" className="btn-close" onClick={() => setSelectedNotice(null)}></button>
              </div>
              <div className="modal-body pb-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <Badge variant={getCategoryVariant(selectedNotice.category)}>{selectedNotice.category}</Badge>
                  {selectedNotice.priority === 'high' && <Badge variant="danger">Important</Badge>}
                </div>
                <h4 className="fw-bold mb-3">{selectedNotice.title}</h4>
                <div className="d-flex align-items-center gap-2 mb-4">
                  <span className="text-muted small">By {selectedNotice.author}</span>
                  <span className="text-muted">•</span>
                  <span className="text-muted small">{selectedNotice.date}</span>
                </div>
                <p className="mb-0" style={{ lineHeight: 1.8 }}>{selectedNotice.content}</p>
              </div>
              <div className="modal-footer border-top-0">
                <button className="btn btn-secondary" onClick={() => setSelectedNotice(null)}>Close</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
