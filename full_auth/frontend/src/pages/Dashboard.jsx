import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Dashboard = () => {
  const { handleLogout } = useAuth();
  const navigate = useNavigate();

  const logout = () => {
    handleLogout();
    navigate('/login');
  };

  return (
    <div style={{ textAlign: 'center', paddingTop: '4rem' }}>
      <h1>Welcome! You're authenticated!</h1>
      <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '1rem' }}>
        <button onClick={logout} style={buttonStyle}>
          Logout
        </button>
        <button onClick={() => navigate('/profile')} style={buttonStyle}>
          Go to Profile
        </button>
      </div>
    </div>
  );
};

const buttonStyle = {
  padding: '0.75rem 1.5rem',
  fontSize: '1rem',
  borderRadius: '6px',
  border: 'none',
  cursor: 'pointer',
  backgroundColor: '#6366f1',
  color: 'white',
};

export default Dashboard;
