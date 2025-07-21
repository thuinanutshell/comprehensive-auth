import { Route, Routes } from 'react-router-dom';
import './App.css';
import ProtectedRoute from './components/ProtectedRoute';
import AuthProvider from './context/AuthProvider';
import Dashboard from './pages/Dashboard';
import LoginPage from './pages/LoginPage';
import OAuthCallback from './pages/OAuthCallback';
import ProfilePage from './pages/ProfilePage';
import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/oauth/callback" element={<OAuthCallback />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
