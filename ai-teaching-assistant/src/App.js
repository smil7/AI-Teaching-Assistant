import React, { useState } from 'react';
import WelcomePage from './frontend/components/WelcomePage';
import FormPage from './frontend/components/FormPage';
import ChatbotInterface from './frontend/components/ChatbotInterface';
import './frontend/styles/Transitions.css';

function App() {
  const [page, setPage] = useState('welcome');
  const [courseName, setCourseName] = useState('');

  const handleStart = () => {
    setPage('form');
  };

  const handleFormSubmit = (courseName, instructions) => {
    // Here you would send the data to the backend
    setCourseName(courseName);
    setPage('chatbot');
  };

  return (
    <div className={`App fade-${page}`}>
      {page === 'welcome' && <WelcomePage onStart={handleStart} />}
      {page === 'form' && <FormPage onSubmit={handleFormSubmit} />}
      {page === 'chatbot' && <ChatbotInterface courseName={courseName} />}
    </div>
  );
}

export default App;
