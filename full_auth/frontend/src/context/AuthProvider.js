import { createContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, logout, register } from '../api/authApi';

// Create a context
export const AuthContext = createContext();

// Define a component that provides user's authenticated token
const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    // Save the user's token on the client side
    const [token, setToken] = useState(localStorage.getItem("token"));
    const navigate = useNavigate();

    // Define a function for logging in with credentials (username/email and password)
    const handleLogin = async (credentials) => {
        const res = await login(credentials);

        // Make sure the data on the backend returns the same object 'user': {}, 'access_token': {}
        setUser(res.data.user);
        console.log('User object in the response:', res.data.user)
        setToken(res.data.access_token);
        localStorage.setItem('token', res.data.access_token);

        // Navigate to the dashboard page after being authenticated
        navigate('/dashboard')
    }

    // Define a function for registering with credentials (first_name, last_name, username, email, password)
    const handleRegister = async (credentials) => {
        const res = await register(credentials);
        setUser(res.data.user);
        setToken(res.data.access_token);
        localStorage.setItem('token', res.data.access_token);
        
        // Navigate to the dashboard page after being authenticated
        navigate('/dashboard')
    }

    const handleLogout = async (token) => {
        await logout(token);
        // Clear out the token and set it to an empty string
        setUser('');
        setToken('');
        navigate('/')
    }

    return (
        // Wrap the context to all the child components that will use the authenticated information
        <AuthContext.Provider value={{
            user,
            token,
            handleLogin,
            handleRegister,
            handleLogout
        }}>
            {children}
        </AuthContext.Provider>
    )
}