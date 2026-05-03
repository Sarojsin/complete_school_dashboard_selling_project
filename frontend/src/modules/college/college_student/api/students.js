import api from '../../../shared/api/client';

// College Student API endpoints
export const getCollegeStudentProfile = () => api.get('/college/students/me');
export const getCollegeStudentDashboard = () => api.get('/college/students/dashboard');
export const getCollegeStudentCourses = () => api.get('/college/students/my-courses');
export const getCollegeStudentGrades = () => api.get('/college/students/my-grades');
export const getCollegeStudentEnrollments = () => api.get('/college/students/my-enrollments');
export const getCollegeStudentHostel = () => api.get('/college/students/my-hostel');

// College student CRUD (for admin/faculty)
export const getCollegeStudents = (params) => api.get('/college/students', { params });
export const getCollegeStudent = (id) => api.get(`/college/students/${id}`);
export const createCollegeStudent = (data) => api.post('/college/students', data);
export const updateCollegeStudent = (id, data) => api.put(`/college/students/${id}`, data);
export const deleteCollegeStudent = (id) => api.delete(`/college/students/${id}`);
