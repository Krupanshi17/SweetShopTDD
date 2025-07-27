import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: '/api', // This will be proxied by Vite
});

// Add token automatically for authenticated requests
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default axiosInstance;
