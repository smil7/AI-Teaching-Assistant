import React, { useState } from 'react';
import '../styles/ChatbotInterface.css';

function ChatbotInterface({ courseName }) {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');

  const handleSendQuery = async (e) => {
    e.preventDefault();
    if (query.trim()) {
      setMessages([...messages, { type: 'user', text: query }]);
      setQuery('');

      try {
        const response = await fetch('http://localhost:5000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setMessages(prevMessages => [
          ...prevMessages,
          { type: 'ai', text: data.answer }
        ]);
      } catch (error) {
        console.error('Error fetching AI response:', error);
        setMessages(prevMessages => [
          ...prevMessages,
          { type: 'ai', text: 'Sorry, there was an error processing your request.' }
        ]);
      }
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