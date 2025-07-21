import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { protected_route } from '../api/authApi';
import { useAuth } from '../hooks/useAuth';

const OAuthCallback = () => {
  const { setToken, setUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleOAuth = async () => {
      const params = new URLSearchParams(location.search);
      const token = params.get('token');

      if (token) {
        setToken(token);
        localStorage.setItem('token', token);
        try {
          const userRes = await protected_route();
          setUser({ id: userRes.logged_in_as });
          navigate('/dashboard');
        } catch (err) {
          console.error('Token invalid after OAuth:', err);
          navigate('/login');
        }
      } else {
        navigate('/login');
      }
    };

    handleOAuth();
  }, [location, setToken, setUser, navigate]);

  return <p>Logging you in via Google...</p>;
};

export default OAuthCallback;
