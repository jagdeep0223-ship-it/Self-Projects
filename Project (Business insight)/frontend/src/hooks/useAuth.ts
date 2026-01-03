// Import hooks from React.
import { useState, useEffect } from 'react';
// Import axios for API requests.
import axios from 'axios';

// Define and export the useAuth custom hook.
export const useAuth = () => {
  // State for storing the auth token, initialized from localStorage.
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  // Async function for login.
  const login = async (email: string, password: string) => {
    try {
      // Post login data to backend.
      const response = await axios.post('http://localhost:8000/login', { username: email, password });
      const { access_token } = response.data;  // Extract token from response.
      localStorage.setItem('token', access_token);  // Save to localStorage.
      setToken(access_token);  // Update state.
      return true;  // Return success.
    } catch (error) {
      console.error('Login failed', error);  // Log error.
      return false;  // Return failure.
    }
  };

  // Function for logout.
  const logout = () => {
    localStorage.removeItem('token');  // Remove token from storage.
    setToken(null);  // Update state.
  };

  // Effect to set axios default headers with token.
  useEffect(() => {
    axios.defaults.headers.common['Authorization'] = token ? `Bearer ${token}` : '';  // Set auth header if token exists.
  }, [token]);  // Run when token changes.

  // Return auth state and functions.
  return { token, login, logout };
};