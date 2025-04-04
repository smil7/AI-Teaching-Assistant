import React from 'react';
import '../styles/WelcomePage.css';

function WelcomePage({ onStart }) {
  return (
    <div className="welcome-container">
      <img src={'/chatbot.jpg'} alt="AI Bot" className="bot-image" />
      <div className="welcome-text">
        <h1>Welcome student, I'm your custom Teaching Assistant. I'm happy to help!</h1>
        <button onClick={onStart} className="start-button">Start</button>
      </div>
    </div>
  );
}

export default WelcomePage; 