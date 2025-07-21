import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

const ProfilePage = () => {
  const { user, handleLogout, updateUserProfile, deleteUser } = useAuth();
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState(user || {});
  const [message, setMessage] = useState('');

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
        const res = await updateUserProfile(form);
        setMessage(res.message || 'Profile updated');
        setEditing(false);
    } catch (err) {
        setMessage(err.response?.data?.message || 'Update failed');
    }
    };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete your account?')) return;

    try {
        await deleteUser();
    } catch (err) {
        setMessage(err.response?.data?.message || 'Delete failed');
    }
    };

  return (
    <div className="profile-container">
      <h1>👤 Profile</h1>

      {editing ? (
        <form className="profile-card" onSubmit={handleUpdate}>
          <input
            type="text"
            value={form.first_name || ''}
            onChange={(e) => setForm({ ...form, first_name: e.target.value })}
            placeholder="First Name"
          />
          <input
            type="text"
            value={form.last_name || ''}
            onChange={(e) => setForm({ ...form, last_name: e.target.value })}
            placeholder="Last Name"
          />
          <input
            type="text"
            value={form.username || ''}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            placeholder="Username"
          />
          <input
            type="email"
            value={form.email || ''}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            placeholder="Email"
          />
          <input
            type="password"
            placeholder="Current Password"
            value={form.current_password || ''}
            onChange={(e) => setForm({ ...form, current_password: e.target.value })}
          />
            <input
            type="password"
            placeholder="New Password"
            value={form.password || ''}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <button type="submit">Save</button>
          <button type="button" onClick={() => setEditing(false)}>Cancel</button>
        </form>
      ) : (
        <div className="profile-card">
          <p><strong>First Name:</strong> {user?.first_name}</p>
          <p><strong>Last Name:</strong> {user?.last_name}</p>
          <p><strong>Username:</strong> {user?.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <button onClick={() => setEditing(true)}>✏️ Edit</button>
          <button onClick={handleDelete} style={{ backgroundColor: '#dc2626', color: 'white' }}>
            🗑️ Delete Account
          </button>
        </div>
      )}

      {message && <p>{message}</p>}
    </div>
  );
};

export default ProfilePage;
