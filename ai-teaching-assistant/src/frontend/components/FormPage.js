import React, { useState } from 'react';
import '../styles/FormPage.css';

function FormPage({ onSubmit }) {
  const [courseName, setCourseName] = useState('');
  const [instructions, setInstructions] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(courseName, instructions);
  };

  return (
    <div className="form-container">
      <img src={'/chatbot.jpg'} alt="AI Bot" className="bot-image" />
      <h1>Welcome student, I'm your custom Teaching Assistant. I'm happy to help!</h1>
      <form onSubmit={handleSubmit} className="submit-form">
        <div className="form-group">
          <label htmlFor="courseName">Course or Chatbot Name:</label>
          <input
            type="text"
            id="courseName"
            name="courseName"
            value={courseName}
            onChange={(e) => setCourseName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="instructions">Additional Instructions (Optional):</label>
          <textarea
            id="instructions"
            name="instructions"
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
          ></textarea>
        </div>
        <div className="form-group">
          <label htmlFor="courseMaterials">Upload Course Materials (Max 500MB):</label>
          <input type="file" id="courseMaterials" name="courseMaterials" accept=".pdf,.doc,.docx,.txt" />
        </div>
        <button type="submit" className="submit-button">Submit</button>
      </form>
    </div>
  );
}

export default FormPage; 