import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // Backend base URL

// Create axios instance with auth header
const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getTodos = async () => {
  const response = await axiosInstance.get(`/todos/`);
  return response.data;
};

export const addTodo = async (todo) => {
  const response = await axiosInstance.post(`/todos/`, todo);
  return response.data;
};
export const updateTodo = async (id, updatedTodo) => {
  const response = await axiosInstance.put(`/todos/${id}`, updatedTodo);
  return response.data;
};
export const deleteTodo = async (id) => {
  await axiosInstance.delete(`/todos/${id}`);
};