import './App.css'
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';

function App() {

  return (
    <>
      /* Public Routes */
      <Routes>
        <Route path="/register" element={<RegisterPage />}/>
        <Route path="/login" element={<LoginPage />}/>
      </Routes>
      /* Private Route */
      <ProtectedRoute>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />}/>
        </Routes>
      </ProtectedRoute>
    </>
  )
}

export default App
