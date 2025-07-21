import { createContext, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { delete_profile, login, login_oauth, logout, protected_route, register, update_profile } from '../api/authApi';

// Create a context
export const AuthContext = createContext();

// Define a component that provides user's authenticated token
const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("token"));
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();

    // Handle OAuth callback when user returns from Google
    useEffect(() => {
        const handleOAuthCallback = async () => {
            // Check if this is an OAuth callback with token in URL
            const urlParams = new URLSearchParams(location.search);
            const accessToken = urlParams.get('token') || urlParams.get('access_token');
            
            if (accessToken && location.pathname.includes('oauth')) {
                try {
                    setLoading(true);
                    setToken(accessToken);
                    localStorage.setItem('token', accessToken);
                    
                    // Get user info
                    const userResponse = await protected_route();
                    setUser(userResponse);
                    
                    // Clean up URL and navigate to dashboard
                    navigate('/dashboard', { replace: true });
                } catch (error) {
                    console.error('OAuth callback failed:', error);
                    navigate('/login', { replace: true });
                } finally {
                    setLoading(false);
                }
            }
        };

        handleOAuthCallback();
    }, [location, navigate]);

    // Check if user is authenticated on component mount
    useEffect(() => {
        const checkAuth = async () => {
            if (token && !location.pathname.includes('oauth')) {
                try {
                    // Use the protected route to get current user info
                    const response = await protected_route();
                    setUser(response);
                } catch (error) {
                    // Token is invalid, clear it
                    handleLogout();
                }
            }
        };
        
        checkAuth();
    }, [token]);

    // Define a function for logging in with credentials (username/email and password)
    const handleLogin = async (credentials) => {
        try {
            setLoading(true);
            const res = await login(credentials);

            // Backend returns: { message, access_token }
            if (res.access_token) {
                setToken(res.access_token);
                localStorage.setItem('token', res.access_token);
                
                // Get user info using the protected route
                try {
                    const userResponse = await protected_route();
                    setUser(userResponse);
                } catch (error) {
                    console.error('Failed to get user info:', error);
                    // Still proceed with login if token is valid
                    setUser({ id: 'unknown' });
                }

                // Navigate to the dashboard page after being authenticated
                navigate('/dashboard');
                return { success: true, message: res.message };
            }
        } catch (error) {
            console.error('Login failed:', error);
            const errorMessage = error.response?.data?.message || 'Login failed';
            return { success: false, message: errorMessage };
        } finally {
            setLoading(false);
        }
    }

    // Define a function for registering with credentials (first_name, last_name, username, email, password)
    const handleRegister = async (credentials) => {
        try {
            setLoading(true);
            const res = await register(credentials);

            // Backend returns: { message, access_token }
            if (res.access_token) {
                setToken(res.access_token);
                localStorage.setItem('token', res.access_token);
                
                // Get user info using the protected route
                try {
                    const userResponse = await protected_route();
                    setUser(userResponse);
                } catch (error) {
                    console.error('Failed to get user info:', error);
                    // Still proceed with registration if token is valid
                    setUser({ id: 'unknown' });
                }
                
                // Navigate to the dashboard page after being authenticated
                navigate('/dashboard');
                return { success: true, message: res.message };
            }
        } catch (error) {
            console.error('Registration failed:', error);
            const errorMessage = error.response?.data?.message || 'Registration failed';
            return { success: false, message: errorMessage };
        } finally {
            setLoading(false);
        }
    }

    const handleLogout = async () => {
        try {
            setLoading(true);
            if (token) {
                await logout(); // No need to pass token, it's in the Authorization header
            }
        } catch (error) {
            console.error('Logout error:', error);
            // Continue with logout even if API call fails
        } finally {
            // Clear local state regardless of API call success
            setUser(null);
            setToken(null);
            localStorage.removeItem('token');
            setLoading(false);
            navigate('/login');
        }
    }

    // OAuth login function
    const handleOAuthLogin = () => {
        try {
            setLoading(true);
            // This will redirect to Google OAuth
            login_oauth();
        } catch (error) {
            console.error('OAuth login failed:', error);
            setLoading(false);
            return { success: false, message: 'OAuth login failed' };
        }
    }

    // Check if user is authenticated
    const isAuthenticated = () => {
        return token !== null && user !== null;
    }

    const updateUserProfile = async (data) => {
        const res = await update_profile(data);
        setUser(prev => ({ ...prev, ...data }));
        return res;
    };

    const deleteUser = async () => {
        try {
            await delete_profile();
            setUser(null);
            setToken(null);
            localStorage.removeItem("token");
            navigate('/login');
        } catch (error) {
            console.error("Account deletion failed:", error);
            throw error;
        }
    };



    return (
        // Wrap the context to all the child components that will use the authenticated information
        <AuthContext.Provider value={{
            user,
            token,
            loading,
            handleLogin,
            handleRegister,
            handleLogout,
            handleOAuthLogin,
            isAuthenticated,
            setToken,
            setUser,
            updateUserProfile,
            deleteUser
        }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthProvider;