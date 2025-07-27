import axios from './axiosInstance';

export const getAllSweets = async () => {
  const res = await axios.get('/sweets/');
  return res.data;
};

export const searchSweets = async (name, category) => {
  const query = new URLSearchParams({ name, category });
  const res = await axios.get(`/sweets/search?${query}`);
  return res.data;
};

export const addSweet = async (sweetData) => {
  const res = await axios.post('/sweets/', sweetData);
  return res.data;
};

export const updateSweet = async (id, sweetData) => {
  const res = await axios.put(`/sweets/${id}`, sweetData);
  return res.data;
};

export const deleteSweet = async (id) => {
  const res = await axios.delete(`/sweets/${id}`);
  return res.data;
};

export const restockSweet = async (id, amount) => {
  const res = await axios.patch(`/sweets/${id}/restock`, { amount });
  return res.data;
};
