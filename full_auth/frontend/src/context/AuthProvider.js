import { createContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, logout, register } from '../api/authApi';

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("token"));
    const navigate = useNavigate();

    const handleLogin = async (credentials) => {
        const res = await login(credentials);
        setUser(res.user);
        setToken(res.token);
        localStorage.setItem('token', res.access_token);
        navigate('/')
    }

    const handleRegister = async (credentials) => {
        const res = await register(credentials);
        setUser(res.user);
        setToken(res.token);
        localStorage.setItem('token', res.access_token);
        navigate('/')
    }

    const handleLogout = async (token) => {
        await logout(token);
        setUser('');
        setToken('');
        navigate('/')
    }

    return (
        <AuthProvider.Provider value={{
            user,
            token,
            handleLogin,
            handleRegister,
            handleLogout
        }}>
            {children}
        </AuthProvider.Provider>
    )
}