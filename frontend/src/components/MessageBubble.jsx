import './MessageBubble.css';

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message-bubble ${isUser ? 'message-user' : 'message-ai'}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🧠'}
      </div>
      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">{isUser ? 'You' : 'NeuroStack AI'}</span>
        </div>
        <div className="message-text">
          {message.loading ? (
            <div className="typing-indicator">
              <span /><span /><span />
            </div>
          ) : (
            message.text
          )}
        </div>
        {message.confidence !== undefined && !isUser && (
          <div className="message-confidence">
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{
                  width: `${Math.round(message.confidence * 100)}%`,
                  background: message.confidence >= 0.6
                    ? 'var(--success)'
                    : message.confidence >= 0.3
                    ? 'var(--warning)'
                    : 'var(--danger)',
                }}
              />
            </div>
            <span className="confidence-label">
              {Math.round(message.confidence * 100)}% confidence
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
