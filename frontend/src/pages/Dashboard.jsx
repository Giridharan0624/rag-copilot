import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatBox from '../components/ChatBox';
import QuestionsPanel from '../components/QuestionsPanel';
import { logout, getUser } from '../services/api';
import './Dashboard.css';

export default function Dashboard() {
  const navigate = useNavigate();
  const user = getUser();
  const [input, setInput] = useState('');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <span className="header-logo">🧠</span>
          <div>
            <h1 className="header-title">NeuroStack</h1>
            <span className="header-badge">RAG Copilot</span>
          </div>
        </div>
        <div className="header-right">
          <span className="header-user">
            <span className="user-avatar">{user?.username?.[0]?.toUpperCase() || 'U'}</span>
            {user?.username}
          </span>
          <button className="btn btn-ghost" onClick={handleLogout}>
            Sign Out
          </button>
        </div>
      </header>
      <main className="dashboard-main">
        <ChatBox input={input} setInput={setInput} />
        <QuestionsPanel onQuestionClick={(q) => setInput(q)} />
      </main>
    </div>
  );
}
