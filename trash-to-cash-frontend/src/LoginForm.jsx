import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
        username,
        password,
      });
      setMessage(`Login successful! Access token: ${response.data.access}`);
    } catch (error) {
      console.error(error);
      setMessage('Login failed. Check credentials.');
    }
  };

  return (
    <div className="form-box">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>
        {message && <p>{message}</p>}
      </form>
    </div>
  );
};

export default LoginForm;
