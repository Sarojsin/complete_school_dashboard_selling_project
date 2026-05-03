import api from '@shared/api/client';

export const signupStudent = async (data) => {
  const response = await api.post('/auth/signup/student', data);
  return response.data;
};

export const signupCollegeStudent = async (data) => {
  const response = await api.post('/auth/signup/college/student', data);
  return response.data;
};

export const signupTeacher = async (data) => {
  const response = await api.post('/auth/signup/teacher', data);
  return response.data;
};

export const signupCollegeTeacher = async (data) => {
  const response = await api.post('/auth/signup/college/teacher', data);
  return response.data;
};

export const signupAuthority = async (data) => {
  const response = await api.post('/auth/signup/authority', data);
  return response.data;
};

export const signupCollegeAuthority = async (data) => {
  const response = await api.post('/auth/signup/college/authority', data);
  return response.data;
};

export const signupParent = async (data) => {
  const response = await api.post('/auth/signup/parent', data);
  return response.data;
};

export const signupAdmin = async (data) => {
  const response = await api.post('/auth/signup/admin', data);
  return response.data;
};

export const signupHOD = async (data) => {
  const response = await api.post('/auth/signup/hod', data);
  return response.data;
};

export const signupExamSection = async (data) => {
  const response = await api.post('/auth/signup/exam-section', data);
  return response.data;
};

export const signupLibrary = async (data) => {
  const response = await api.post('/auth/signup/library', data);
  return response.data;
};

export const signupAccount = async (data) => {
  const response = await api.post('/auth/signup/account', data);
  return response.data;
};
