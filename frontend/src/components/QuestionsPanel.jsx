import { useState, useEffect } from 'react';
import { getQuestions } from '../services/api';
import './QuestionsPanel.css';

export default function QuestionsPanel({ onQuestionClick }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const data = await getQuestions();
        setQuestions(data);
      } catch (err) {
        console.error('Failed to load questions:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuestions();
  }, []);

  return (
    <aside className="questions-panel">
      <div className="questions-panel-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <h3>Available FAQs</h3>
      </div>
      
      <div className="questions-list">
        {loading ? (
          <div className="questions-loading">Loading questions...</div>
        ) : questions.length === 0 ? (
          <div className="questions-empty">No questions found.</div>
        ) : (
          questions.map((q, i) => (
            <button
              key={i}
              className="question-card"
              onClick={() => onQuestionClick(q)}
            >
              {q}
            </button>
          ))
        )}
      </div>
    </aside>
  );
}
