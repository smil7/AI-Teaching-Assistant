import React, { useState } from 'react';
import './App.css';
import botImage from './chatbot.jpg';

function App() {
  const [started, setStarted] = useState(false);
  const [visible, setVisible] = useState(true);

  const handleStart = () => {
    setVisible(false);
    setTimeout(() => {
      setStarted(true);
      setVisible(true);
    }, 500); // Wait for the transition to complete
  };

  return (
    <div className="App" style={{ opacity: visible ? 1 : 0, transition: 'opacity 0.5s ease-in-out' }}>
      {!started ? (
        <div className="welcome-container">
          <img src={botImage} alt="AI Bot" className="bot-image" />
          <div className="welcome-text">
            <h1>Welcome student, I'm your custom Teaching Assistant. I'm happy to help!</h1>
            <button onClick={handleStart} className="start-button">Start</button>
          </div>
        </div>
      ) : (
        <div className="form-container">
          <h1>Welcome student, I'm your custom Teaching Assistant. I'm happy to help!</h1>
          <form>
            <div className="form-group">
              <label htmlFor="courseName">Course or Chatbot Name:</label>
              <input type="text" id="courseName" name="courseName" required />
            </div>
            <div className="form-group">
              <label htmlFor="instructions">Additional Instructions (Optional):</label>
              <textarea id="instructions" name="instructions"></textarea>
            </div>
            <div className="form-group">
              <label htmlFor="courseMaterials">Upload Course Materials (Max 500MB):</label>
              <input type="file" id="courseMaterials" name="courseMaterials" accept=".pdf,.doc,.docx,.txt" />
            </div>
            <button type="submit" className="submit-button">Submit</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
