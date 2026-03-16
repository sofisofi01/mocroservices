import {useEffect, useRef, useState} from 'react';
import {
  Grid,
  Box,
  Alert,
  CircularProgress,
  IconButton,
} from '@mui/material';
import { Refresh, DeleteForever } from '@mui/icons-material';
import { ExpenseCard } from '../../components/ExpenseCard/ExpenseCard';
import { useExpenses } from '../../hooks/useExpenses.ts';
import type { Expense } from '../../services/ExpenseService/types';
import {useNavigate} from "react-router-dom";

export function Expenses() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const navigate = useNavigate();
  const loadMoreRef = useRef<HTMLDivElement>(null);

  const loadMore = async () => {
    if (!hasMore || loading) return;

    try {
      const nextPage = page + 1;
      const response = await fetchExpenses(nextPage, 10);

      setExpenses(prev => [...prev, ...response.results]);
      setHasMore(response.next);
      setPage(nextPage);
    } catch (err) {
      console.error('Ошибка загрузки:', err);
    }
  };

  const {
    loading,
    error,
    fetchExpenses,
    deleteExpense,
    deleteAllExpenses,
  } = useExpenses();

  useEffect(() => {
    const loadExpenses = async () => {
      try {
        const response = await fetchExpenses(1, 10);
        setExpenses(response.results);
        setHasMore(response.next);
      } catch (err) {
        console.error('Ошибка загрузки расходов:', err);
      }
    };

    loadExpenses();
  }, []);

  useEffect(() => {
    if (!loadMoreRef.current || !hasMore || loading) return;

    const observer = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting) {
            loadMore();
          }
        },
        { rootMargin: '100px', threshold: 0.1 }
    );

    observer.observe(loadMoreRef.current);
    return () => observer.disconnect();
  }, [hasMore, loading]);

  const handleDelete = async (id: number) => {
    await deleteExpense(id);
    setExpenses(prev => prev.filter(e => e.id !== id));
  };

  const handleChange = (id: number) => {
    navigate(`/expenseslist/${id}/change`);
  };

  const handleDeleteAll = async () => {
    await deleteAllExpenses(expenses);
    setExpenses([]);
  };

  const handleRefresh = async () => {
    const response = await fetchExpenses(1, 10);
    setExpenses(response.results);
    setPage(1);
    setHasMore(response.next);
  };

  if (loading && expenses.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert
        severity="error"
        action={
          <IconButton size="small" onClick={handleRefresh}>
            <Refresh />
          </IconButton>
        }
      >
        {error}
      </Alert>
    );
  }

 return (
    <Box p={2}>
      <Box display="flex" justifyContent="flex-end" gap={1} mb={3}>
        <IconButton onClick={handleRefresh} disabled={loading}>
          <Refresh />
        </IconButton>
        {expenses.length > 0 && (
          <IconButton onClick={handleDeleteAll} disabled={loading} color="error">
            <DeleteForever />
          </IconButton>
        )}
      </Box>

      <Grid container spacing={5}>
        {expenses.map(expense => (
          <Grid key={expense.id} item
                xs={12}
                sm={6}
                md={4}
                lg={3}>
            <ExpenseCard
              {...expense}
                onChange={()=>handleChange(expense.id)}
              onDelete={handleDelete}
            />
          </Grid>
        ))}
      </Grid>

      {hasMore && (
          <Box
              ref={loadMoreRef}
              display="flex"
              justifyContent="center"
              alignItems="center"
              height="100px"
              mt={2}
          >
            {loading && <CircularProgress size={24} />}
          </Box>
      )}
    </Box>
  );
}