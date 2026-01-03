// Import React and useState.
import React, { useState } from 'react';
// Import navigate for redirection.
import { useNavigate } from 'react-router-dom';
// Import auth hook.
import { useAuth } from '../hooks/useAuth';

// Define the Login component.
const Login: React.FC = () => {
  // State for email input.
  const [email, setEmail] = useState('');
  // State for password input.
  const [password, setPassword] = useState('');
  const { login } = useAuth();  // Get login function from hook.
  const navigate = useNavigate();  // Get navigate function.

  // Handle form submission.
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();  // Prevent default form behavior.
    const success = await login(email, password);  // Call login.
    if (success) {  // If successful.
      navigate('/dashboard');  // Redirect to dashboard.
    } else {  // If failed.
      alert('Invalid credentials');  // Show alert.
    }
  };

  // Render the login form.
  // return (
  //   <div style={{ maxWidth: '400px', margin: 'auto', padding: '20px' }}>
  //     <h2>Login to InsightForge</h2>
  //     <form onSubmit={handleSubmit}>
  //       <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
  //       <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
  //       <button type="submit">Login</button>
  //     </form>
  //     <p>Demo: Register via API first (email: admin@example.com, password: admin, role: admin)</p>
  //   </div>
  // );
  return (
    <div className="container vh-100 d-flex align-items-center justify-content-center">
      <div className="card p-4" style={{ width: '400px' }}>
        <h3 className="text-center mb-3">InsightForge</h3>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary w-100">
            Login
          </button>
        </form>

        <small className="text-muted mt-3 d-block text-center">
          Demo Admin: admin@example.com / admin
        </small>
      </div>
    </div>
  );
};

export default Login;  // Export component.