import axios from "axios";

export async function loginApi(email, password) {
  const response = await axios.post("/api/auth/login", { email, password });
  return response.data.token;
}

export async function registerApi(name, email, password) {
  const response = await axios.post("/api/auth/register", { name, email, password });
  return response.data;
}
