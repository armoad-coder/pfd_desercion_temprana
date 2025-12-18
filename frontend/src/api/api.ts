import axios from "axios";
import { useUserStore } from "@/stores/userStore";
import router from "@/router";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

// === REQUEST INTERCEPTOR ===
// Adjunta automáticamente el token a cada petición
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// === RESPONSE INTERCEPTOR ===
// Si recibimos 401, significa token inválido/expirado
api.interceptors.response.use(
  (response) => response,

  (error) => {
    const userStore = useUserStore();

    if (error.response?.status === 401) {
      userStore.logout();
      router.push("/login");
    }

    return Promise.reject(error);
  }
);

export default api;
