import api from '@shared/api/client';

export const login = async (username, password, portalType = null) => {
  const payload = { username, password };
  if (portalType) {
    payload.portal_type = portalType;  // Send portal type to backend
  }
  
  const response = await api.post('/auth/login-json', payload);
  
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('token', response.data.access_token);
    
    // Store full user data including portal_type
    const userData = response.data.user;
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('portal_type', userData.portal_type); // Store separately for easy access
  }
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  window.location.href = '/login';
};
