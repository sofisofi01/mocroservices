import { useState } from 'react';
import expenseService from '../services/ExpenseService/ExpenseService'
import type {Expense, ExpenseCreate, ExpenseUpdate, PaginatedResponse} from '../services/ExpenseService/types';

export const useExpenses = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchExpenses = async (
      page: number = 1,
      limit: number = 10
  ): Promise<PaginatedResponse> => {
    try {
      setLoading(true);
      setError(null);
      return await expenseService.getAll(page, limit);

    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при загрузке расходов';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getExpenseById = async (id: number): Promise<Expense> => {
    try {
      setLoading(true);
      setError(null);
      return await expenseService.getById(id);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при получении расхода';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const createExpense = async (data: ExpenseCreate): Promise<Expense> => {
    try {
      setLoading(true);
      setError(null);
      return await expenseService.create(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при создании расхода';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateExpense = async (id: number, data: ExpenseUpdate): Promise<Expense> => {
    try {
      setLoading(true);
      setError(null);
      return await expenseService.update(id, data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при обновлении расхода';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteExpense = async (id: number): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      await expenseService.delete(id);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при удалении расхода';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteAllExpenses = async (expenses: Expense[]): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      const deletePromises = expenses.map(expense => 
        expenseService.delete(expense.id)
      );
      await Promise.all(deletePromises);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при удалении всех расходов';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    fetchExpenses,
    getExpenseById,
    createExpense,
    updateExpense,
    deleteExpense,
    deleteAllExpenses,
  };
};