import axios from "axios";

const api = axios.create({
  baseURL: "https://mainweb-backend-topaz.vercel.app/",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor
api.interceptors.response.use(
  (response) => {
    //passing the data if it is successful
    return response;
  },
  (error) => {
    //if error occurs
    if (error.response && error.response.status === 401) {
      console.warn("Token expired or invalid. Logging out...");
      localStorage.removeItem("access_token");

      window.location.href = "/";
    }

    return Promise.reject(error);
  }
);
export default api;
