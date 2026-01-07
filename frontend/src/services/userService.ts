import api from "../../src/api/axios";
import type { User } from "../types/dashboard";

export const userService = {
  // 1. GET (Read all)
  // Usage: getEntities("interns") or getEntities("teams")
  getEntities: async (type: string) => {
    const response = await api.get<User[]>(`/api/${type}`);
    return response.data;
  },

  // 2. DELETE
  deleteEntity: async (type: string, id: string) => {
    await api.delete(`/api/${type}/${id}`);
  },

  // 3. PUT (Update)
  updateEntity: async (type: string, id: string, data: Partial<User>) => {
    const response = await api.put<User>(`/api/${type}/${id}`, data);
    return response.data;
  },

  // 4. POST (Create)
  addEntity: async (type: string, data: Partial<User>) => {
    const response = await api.post<User>(`/api/${type}`, data);
    return response.data;
  },
};
