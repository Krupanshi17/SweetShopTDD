import axiosInstance from './axiosInstance';
export const loginApi = (email, password) => {
  return axios.post('/auth/login', { email, password });
};

export const registerApi = (email, password) => {
  return axios.post('/auth/register', { email, password });
};

export const login = async (email, password) => {
  try {
    const response = await axiosInstance.post('/auth/login', new URLSearchParams({
      username: email,
      password: password
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { detail: 'Login failed' };
  }
};

export const register = async (email, password, role = 'user', adminSecret = null) => {
  try {
    const data = { email, password, role };
    if (adminSecret) data.admin_secret = adminSecret;

    const response = await axiosInstance.post('/auth/register', data);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { detail: 'Registration failed' };
  }
};
