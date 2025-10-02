import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
  // Simple state variables
  const [showLogin, setShowLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle form submission
  const submitForm = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    let url = '';
    let data = {};
    
    if (showLogin) {
      url = 'http://localhost:5000/api/auth/login';
      data = { username: username, password: password };
    } else {
      url = 'http://localhost:5000/api/auth/register';
      data = { username: username, email: email, password: password };
    }

    axios.post(url, data)
      .then(function(response) {
        onLogin(response.data.access_token, response.data.user);
      })
      .catch(function(error) {
        setError('Login failed. Please try again.');
        setLoading(false);
      });
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={submitForm}>
        <h2>{showLogin ? 'Login' : 'Register'}</h2>
        
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        {!showLogin && (
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
        )}

        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading}
          style={{ width: '100%' }}
        >
          {loading ? 'Loading...' : (showLogin ? 'Login' : 'Register')}
        </button>

        {error && <div className="error-message">{error}</div>}

        <div className="auth-toggle">
          <button
            type="button"
            onClick={() => setShowLogin(!showLogin)}
          >
            {showLogin ? 'Need an account? Register' : 'Have an account? Login'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default Login;