// Import React for component creation.
import React from 'react';
// Import routing components from react-router-dom.
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// Import custom components.
import Login from './components/Login';
import Dashboard from './components/Dashboard';
// Import auth hook.
import { useAuth } from './hooks/useAuth';

// Define the main App component.
const App: React.FC = () => {
  return (
    // Wrap routes in Router for client-side routing.
    <Router>
      {/* Define the routes. */}
      <Routes>
        {/* Route for login page. */}
        <Route path="/login" element={<Login />} />
        {/* Protected route for dashboard. */}
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        {/* Default route redirects to login. */}
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

// Define a private route component to protect pages.
const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token } = useAuth();  // Get token from auth hook.
  return token ? <>{children}</> : <Navigate to="/login" />;  // If token exists, render children; else redirect.
};

export default App;  // Export the App component.