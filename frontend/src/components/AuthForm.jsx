import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './AuthForm.css';

export default function AuthForm({ mode = 'login', onSubmit }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const isSignup = mode === 'signup';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await onSubmit(isSignup ? { username, email, password } : { username, password });
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.username?.[0] || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-bg-gradient" />
      <div className="auth-container animate-fade-in">
        <div className="auth-logo">
          <div className="auth-logo-icon">🧠</div>
          <h1>NeuroStack</h1>
          <p className="auth-subtitle">RAG Copilot</p>
        </div>

        <form className="auth-form glass-card" onSubmit={handleSubmit}>
          <h2>{isSignup ? 'Create Account' : 'Welcome Back'}</h2>
          <p className="auth-description">
            {isSignup ? 'Sign up to access the AI support copilot' : 'Sign in to continue'}
          </p>

          {error && <div className="auth-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              className="input"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          {isSignup && (
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                className="input"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              className="input"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          <button className="btn btn-primary auth-button" type="submit" disabled={loading}>
            {loading ? (
              <span className="spinner" />
            ) : isSignup ? (
              'Create Account'
            ) : (
              'Sign In'
            )}
          </button>

          <p className="auth-switch">
            {isSignup ? (
              <>Already have an account? <Link to="/login">Sign in</Link></>
            ) : (
              <>Don't have an account? <Link to="/signup">Sign up</Link></>
            )}
          </p>
        </form>
      </div>
    </div>
  );
}
