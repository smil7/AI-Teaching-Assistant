import React, { useState } from 'react';
import '../styles/ChatbotInterface.css';

function ChatbotInterface({ courseName }) {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');

  const handleSendQuery = (e) => {
    e.preventDefault();
    if (query.trim()) {
      setMessages([...messages, { type: 'user', text: query }]);
      setQuery('');

      setTimeout(() => {
        setMessages(prevMessages => [
          ...prevMessages,
          { type: 'ai', text: 'This is a simulated AI response.' }
        ]);
      }, 1000);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbox">
        <h2>{courseName}</h2>
        <p>Thanks for enrolling in {courseName}! I'm your AI teaching assistant, ready to help you with your questions.</p>
        <p className="warning">The chats in this webpage won't be stored</p>
        <div className={`chat-history ${messages.length === 0 ? 'empty' : ''}`}>
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <img
                src={message.type === 'user' ? '/user-query.png' : '/ai-response.png'}
                alt={message.type}
                className="message-icon"
              />
              <span className="message-text">{message.text}</span>
            </div>
          ))}
        </div>
        <form className="input-area" onSubmit={handleSendQuery}>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your query here..."
            rows="1"
          />
          <button type="submit">
            <img src="/send-icon.png" alt="Send" />
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatbotInterface; 