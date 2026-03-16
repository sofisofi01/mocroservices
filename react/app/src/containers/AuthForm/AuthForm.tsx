import {TextField, Button, Box, Alert, Container, Paper, Typography, Link} from '@mui/material';
import {useAuth} from "../../hooks/useAuth.ts";
import {Link as RouterLink, useLocation, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {hasSession} from "../../helpers/session.ts";

export function AuthForm() {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [localError, setLocalError] = useState('');

    const location = useLocation();
    const navigate = useNavigate();
    const { register, login: authLogin, loading, error } = useAuth();

    const isRegister = location.pathname === '/register';
    const title = isRegister ? 'Регистрация' : 'Вход';
    const buttonText = isRegister ? 'Зарегистрироваться' : 'Войти';
    const linkText = isRegister ? 'Уже есть аккаунт?' : 'Нет аккаунта?';
    const linkTo = isRegister ? '/' : '/register';
    const linkAction = isRegister ? 'Войдите' : 'Зарегистрируйтесь';

    useEffect(() => {
        if (hasSession()) {
            navigate('/expenseslist');
        }
    }, [navigate]);

    const handleSubmit = async () => {
        setLocalError('');

        if (!login.trim()) {
            setLocalError('Введите логин');
            return;
        }

        if (!password.trim()) {
            setLocalError('Введите пароль');
            return;
        }

        const authFunction = isRegister ? register : authLogin;

        authFunction({ login, password })
            .then((result) => {
                if (result) {
                    navigate('/expenseslist');
                }
            });
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && login && password) {
            handleSubmit();
        }
    };

    const displayError = localError || error;

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 8 }}>
                <Paper elevation={3} sx={{ p: 4 }}>
                    <Typography variant="h4" component="h1" align="center" gutterBottom>
                        {title}
                    </Typography>

                    {displayError && (
                        <Alert severity="error" sx={{ mb: 3 }}>
                            {displayError}
                        </Alert>
                    )}

                    <TextField
                        fullWidth
                        label="Логин"
                        value={login}
                        onChange={(e) => {
                            setLogin(e.target.value);
                            setLocalError('');
                        }}
                        onKeyDown={handleKeyPress}
                        margin="normal"
                        disabled={loading}
                        required
                        autoFocus
                    />

                    <TextField
                        fullWidth
                        label="Пароль"
                        type="password"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                            setLocalError('');
                        }}
                        onKeyDown={handleKeyPress}
                        margin="normal"
                        disabled={loading}
                        required
                    />

                    <Button
                        fullWidth
                        variant="contained"
                        size="large"
                        onClick={handleSubmit}
                        sx={{ mt: 3 }}
                        disabled={loading}
                    >
                        {loading ? '...' : buttonText}
                    </Button>

                    <Box sx={{ mt: 3, textAlign: 'center' }}>
                        <Typography variant="body2">
                            {linkText}{' '}
                            <Link component={RouterLink} to={linkTo} underline="hover">
                                {linkAction}
                            </Link>
                        </Typography>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
}