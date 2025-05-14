import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const signUp = (data) => API.post("/client/signup", data);
export const login = (data) => API.post("/client/login", null, { params: data });
export const getFiles = (token) =>
  API.get("/client/list", { headers: { Authorization: `Bearer ${token}` } });
export const getDownloadLink = (id, token) =>
  API.get(`/client/download-file/${id}`, { headers: { Authorization: `Bearer ${token}` } });
