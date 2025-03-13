import axios from "axios";

// Создаем экземпляр axios
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Добавляем интерсептор (автоматически подставляем токен в заголовки)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
