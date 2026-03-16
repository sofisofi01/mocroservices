import { useState } from 'react';
import type {Token, UserLogin, UserRegister} from "../services/UserService/types.ts";
import UserService from "../services/UserService/UserService.ts";
import {hasSession, startSession, stopSession} from "../helpers/session.ts";


export function useAuth() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const register = async (userData: UserRegister) => {
        setLoading(true);
        setError(null);

        try {
            const token: Token = await UserService.registerUser(userData);
            startSession(token.token);
            return token;
        } catch (err) {
            const errorMessage = 'Ошибка регистрации';
            setError(errorMessage);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const login = async (userData: UserLogin) => {
        setLoading(true);
        setError(null);

        try {
            const token: Token = await UserService.loginUser(userData);
            startSession(token.token);
            return token;
        } catch (err) {
            const errorMessage =  'Ошибка авторизации';
            setError(errorMessage);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        stopSession();
    };

    return {
        register,
        login,
        logout,
        isAuthenticated: hasSession(),
        loading,
        error,
    };
}