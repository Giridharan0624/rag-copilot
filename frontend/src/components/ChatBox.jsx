import { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import { queryRAG } from '../services/api';
import './ChatBox.css';

export default function ChatBox({ input, setInput }) {
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      text: "👋 Hello! I'm the NeuroStack AI Copilot. Ask me anything about TaskFlow AI — account setup, features, integrations, billing, and more!",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [activeSources, setActiveSources] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, activeSources]);

  const handleSend = async () => {
    const query = input.trim();
    if (!query || loading) return;

    // Add user message
    setMessages((prev) => [...prev, { role: 'user', text: query }]);
    setInput('');
    setLoading(true);
    setActiveSources(null);

    // Add loading bubble
    setMessages((prev) => [...prev, { role: 'ai', loading: true }]);

    try {
      const data = await queryRAG(query);
      // Replace loading bubble with actual response
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          role: 'ai',
          text: data.answer,
          confidence: data.confidence,
          validated: data.validated,
          sources: data.sources,
        },
      ]);
      setActiveSources(data.sources);
    } catch (err) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          role: 'ai',
          text: err.response?.data?.error || 'Something went wrong. Please try again.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestions = [
    'How do I reset my password?',
    'What are the pricing plans?',
    'How do I integrate with Slack?',
    'How do I use the Kanban board?',
  ];

  return (
    <div className="chatbox">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        <div ref={chatEndRef} />
      </div>

      {messages.length <= 1 && (
        <div className="chat-suggestions">
          {suggestions.map((s, i) => (
            <button
              key={i}
              className="suggestion-chip"
              onClick={() => {
                setInput(s);
              }}
            >
              {s}
            </button>
          ))}
        </div>
      )}

      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <textarea
            id="chat-input"
            className="chat-input"
            placeholder="Ask about TaskFlow AI..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!input.trim() || loading}
            aria-label="Send message"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 2L11 13" /><path d="M22 2L15 22L11 13L2 9L22 2Z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
