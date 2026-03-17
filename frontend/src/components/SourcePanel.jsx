import './SourcePanel.css';
import { useState } from 'react';

export default function SourcePanel({ sources, onFeedback }) {
  const [feedback, setFeedback] = useState(null);

  if (!sources || sources.length === 0) return null;

  const handleFeedback = (type) => {
    setFeedback(type);
    if (onFeedback) onFeedback(type);
  };

  return (
    <div className="source-panel glass-card animate-slide-up">
      <div className="source-panel-header">
        <h3>📚 Retrieved Sources</h3>
        <div className="feedback-buttons">
          <button
            className={`feedback-btn ${feedback === 'up' ? 'active-up' : ''}`}
            onClick={() => handleFeedback('up')}
            title="Helpful"
          >
            👍
          </button>
          <button
            className={`feedback-btn ${feedback === 'down' ? 'active-down' : ''}`}
            onClick={() => handleFeedback('down')}
            title="Not helpful"
          >
            👎
          </button>
        </div>
      </div>

      <div className="source-list">
        {sources.map((source, index) => {
          const scorePercent = Math.round(source.score * 100);
          const scoreColor =
            source.score >= 0.6 ? 'var(--success)' :
            source.score >= 0.3 ? 'var(--warning)' :
            'var(--danger)';

          return (
            <div key={index} className="source-item">
              <div className="source-rank">#{index + 1}</div>
              <div className="source-body">
                <p className="source-text">{source.text}</p>
                <div className="source-score-row">
                  <div className="source-score-bar-bg">
                    <div
                      className="source-score-bar-fill"
                      style={{ width: `${scorePercent}%`, background: scoreColor }}
                    />
                  </div>
                  <span className="source-score-label" style={{ color: scoreColor }}>
                    {scorePercent}%
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
