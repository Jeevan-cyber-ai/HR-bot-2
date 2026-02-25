import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import Chat from './pages/Chat'
import HRDashboard from './pages/HRDashboard'

function ProtectedRoute({ children, allowedRole }) {
  const { user } = useAuth()

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (allowedRole && user.role !== allowedRole) {
    return <Navigate to={user.role === 'employee' ? '/chat' : '/hr-dashboard'} replace />
  }

  return children
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route
            path="/chat"
            element={
              <ProtectedRoute allowedRole="employee">
                <Chat />
              </ProtectedRoute>
            }
          />

          <Route
            path="/hr-dashboard"
            element={
              <ProtectedRoute allowedRole="hr">
                <HRDashboard />
              </ProtectedRoute>
            }
          />

          {/* Redirect root to login or appropriate dashboard */}
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Catch all */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App