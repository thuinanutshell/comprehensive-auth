import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

const RegisterForm = () => {
  const { handleRegister, loading } = useAuth();
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    password: '',
  });
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await handleRegister(form);
    setMessage(result.message);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>Register</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        <input
          type="text"
          placeholder="First Name"
          required
          value={form.first_name}
          onChange={(e) => setForm({ ...form, first_name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Last Name"
          required
          value={form.last_name}
          onChange={(e) => setForm({ ...form, last_name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Username"
          required
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          required
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          required
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
        {message && <p style={{ marginTop: '0.5rem', color: '#e63946' }}>{message}</p>}
      </form>
    </div>
  );
};

export default RegisterForm;
