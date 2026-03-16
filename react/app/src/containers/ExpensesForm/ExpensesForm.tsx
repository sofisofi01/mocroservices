import React, {useEffect, useState} from 'react';
import {
    Box,
    TextField,
    Button,
    Alert,
    CircularProgress,
    Stack, Typography,
} from '@mui/material';
import {Close, Save} from '@mui/icons-material';
import { useExpenses } from '../../hooks/useExpenses.ts';
import type {ExpensesFormProps} from "./types.ts";
import {useNavigate, useParams} from "react-router-dom";


export function ExpensesForm({ onSuccess}: ExpensesFormProps) {
    const navigate = useNavigate();
    const { id } = useParams<{ id: string }>();
    const [title, setTitle] = useState('');
    const [cost, setCost] = useState('');
    const [quantity, setQuantity] = useState('1');

    const isEditMode = !!id;

    const {
        loading,
        error,
        createExpense,
        updateExpense,
        getExpenseById
    } = useExpenses();

    const loadExpenseData = async () => {
        try {
            const expense = await getExpenseById(Number(id));
            if (expense) {
                setTitle(expense.title);
                setCost(expense.cost.toString());
                setQuantity(expense.quantity.toString());
            }
        } catch (err) {
            console.error('Ошибка загрузки данных:', err);
        }
    };

    useEffect(() => {
        if (isEditMode && id) {
            loadExpenseData();
        }
    }, [id, isEditMode]);


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!title.trim()) return;

        try {
            if (isEditMode && id) {
                await updateExpense(Number(id), {
                    title,
                    cost: parseFloat(cost) || 0,
                    quantity: parseInt(quantity) || 1,
                    date: new Date().toISOString().split('T')[0],
                });
            } else {
                await createExpense({
                    title,
                    cost: parseFloat(cost) || 0,
                    quantity: parseInt(quantity) || 1,
                    date: new Date().toISOString().split('T')[0],
                });
            }

            onSuccess?.();

            navigate('/expenseslist');

        } catch (err) {
            console.error('Ошибка:', err);
        }
    };

    const handleCancel = () => {
        navigate('/expenseslist');
    };

    return (
        <Box sx={{ maxWidth: 500, margin: 'auto', p: 3 }}>
            <Typography variant="h5" gutterBottom>
                {isEditMode ? 'Редактирование расхода' : 'Создание нового расхода'}
            </Typography>

            <Box
                component="form"
                onSubmit={handleSubmit}
                sx={{
                    p: 3,
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 2,
                    backgroundColor: 'background.paper'
                }}
            >
                <Stack spacing={3}>
                    {error && <Alert severity="error">{error}</Alert>}

                    <TextField
                        label="Название"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                        autoFocus={!isEditMode}
                        disabled={loading}
                        fullWidth
                        helperText="Введите название расхода"
                    />

                    <Box display="flex" gap={2}>
                        <TextField
                            label="Стоимость"
                            type="number"
                            value={cost}
                            onChange={(e) => setCost(e.target.value)}
                            required
                            disabled={loading}
                            sx={{ flex: 2 }}
                            InputProps={{
                                inputProps: {
                                    min: 0,
                                    step: 0.01
                                }
                            }}
                            helperText="Общая стоимость"
                        />
                        <TextField
                            label="Кол-во"
                            type="number"
                            value={quantity}
                            onChange={(e) => setQuantity(e.target.value)}
                            required
                            disabled={loading}
                            sx={{ flex: 1 }}
                            InputProps={{
                                inputProps: {
                                    min: 1,
                                    step: 1
                                }
                            }}
                        />
                    </Box>

                    {cost && quantity && (
                        <Typography variant="body2" color="text.secondary">
                            Цена за единицу: {(parseFloat(cost) / parseInt(quantity) || 0).toFixed(2)} ₽
                        </Typography>
                    )}

                    <Box display="flex" gap={2}>
                        <Button
                            variant="outlined"
                            startIcon={<Close />}
                            onClick={handleCancel}
                            disabled={loading}
                            fullWidth
                            sx={{ py: 1.5 }}
                        >
                            Отмена
                        </Button>
                        <Button
                            type="submit"
                            variant="contained"
                            startIcon={isEditMode ? <Save /> : undefined}
                            disabled={loading || !title.trim() || !cost}
                            fullWidth
                            sx={{ py: 1.5 }}
                        >
                            {loading ? (
                                <CircularProgress size={24} />
                            ) : isEditMode ? (
                                'Сохранить изменения'
                            ) : (
                                'Добавить'
                            )}
                        </Button>
                    </Box>
                </Stack>
            </Box>
        </Box>
    );
}