import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

const LoginForm = () => {
  const { handleLogin, handleOAuthLogin, loading } = useAuth();
  const [form, setForm] = useState({ login: '', password: '' });
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await handleLogin(form);
    setMessage(result.message);
  };

  return (
    <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
        <input
            placeholder="Email"
            value={form.login}
            onChange={(e) => setForm({ ...form, login: e.target.value })}
            required
        />
        <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
        />
        <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
        </button>
        </form>

        {message && <div className="message">{message}</div>}

        <hr />
        <button
        onClick={handleOAuthLogin}
        className="google-button"
        disabled={loading}
        >
        <img
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
            alt="Google"
            style={{ width: '20px', height: '20px' }}
        />
        {loading ? 'Redirecting...' : 'Login with Google'}
        </button>

    </div>
  );
};

export default LoginForm;
