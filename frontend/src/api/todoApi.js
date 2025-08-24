import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // Backend base URL

export const getTodos = async () => {
  const response = await axios.get(`${API_URL}/todos/`);
  return response.data;
};

export const addTodo = async (todo) => {
  const response = await axios.post(`${API_URL}/todos/`, todo);
  return response.data;
};
export const updateTodo = async (id, updatedTodo) => {
  const response = await axios.put(`${API_URL}/todos/${id}`, updatedTodo);
  return response.data;
};
export const deleteTodo = async (id) => {
  await axios.delete(`${API_URL}/todos/${id}`);
};