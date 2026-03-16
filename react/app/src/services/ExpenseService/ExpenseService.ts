
import axios from 'axios';
import type { Expense, ExpenseCreate, ExpenseUpdate, PaginatedResponse } from './types';
import {getToken} from "../../helpers/header.ts";

const API_URL = 'http://localhost:9002/expenses/';

const axiosInstance = axios.create({
  baseURL: API_URL,
});

axiosInstance.interceptors.request.use(
    (config) => {
      const token = getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
);

class ExpenseService {
  async getAll(page: number = 1, limit: number = 10): Promise<PaginatedResponse> {
    const response = await axiosInstance.get<PaginatedResponse>('', {
      params: {
        page,
        limit,
      }
    });
    return response.data;
  }

  async getById(id: number): Promise<Expense> {
    const response = await axiosInstance.get<Expense>(`${id}`);
    return response.data;
  }

  async create(data: ExpenseCreate): Promise<Expense> {
    const response = await axiosInstance.post<Expense>('', data);
    return response.data;
  }

  async update(id: number, data: ExpenseUpdate): Promise<Expense> {
    const response = await axiosInstance.patch<Expense>(`${id}`, data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await axiosInstance.delete(`${id}`);
  }
}

export default new ExpenseService();