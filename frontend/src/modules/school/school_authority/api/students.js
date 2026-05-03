import api from '../../../shared/api/client';

export const getMyStudentProfile = async () => {
  const response = await api.get('/school/authorities/me');
  return response.data;
};

export const getAuthorityStudents = async (skip = 0) => {
  const response = await api.get(`/school/authority/students?skip=${skip}`);
  return response.data;
};

export const getAuthorityTeachers = async (skip = 0) => {
  const response = await api.get(`/school/authority/teachers?skip=${skip}`);
  return response.data;
};

export const getAuthorityDashboard = async () => {
  const response = await api.get('/school/authority');
  return response.data;
};

export const createCourse = async (data) => {
  const response = await api.post('/school/courses/', data);
  return response.data;
};

export const createNotice = async (data) => {
  const response = await api.post('/school/notices/', data);
  return response.data;
};
