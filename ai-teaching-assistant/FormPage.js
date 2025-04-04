import React, { useState } from 'react';
import '../styles/FormPage.css';

function FormPage({ onSubmit }) {
  const [courseName, setCourseName] = useState('');
  const [instructions, setInstructions] = useState('');
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsUploading(true);

    const formData = new FormData();
    formData.append('courseName', courseName);
    formData.append('instructions', instructions);
    
    // Append each file to formData
    for (let i = 0; i < files.length; i++) {
      formData.append('courseMaterials', files[i]);
    }
    console.log(formData);
    try {
      const response = await fetch('http://localhost:5000/api/ingest', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        if (result.message === 'the files and names are ingested') {
          onSubmit(courseName, instructions);
        } else {
          alert('Failed to ingest data');
        }
      } else {
        alert('Failed to send data to the server');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while sending data');
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
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
          <input
            type="file"
            id="courseMaterials"
            name="courseMaterials"
            accept=".pdf,.doc,.docx,.txt"
            onChange={handleFileChange}
            multiple
          />
        </div>
        <button 
          type="submit" 
          className="submit-button"
          disabled={isUploading}
        >
          {isUploading ? 'Uploading...' : 'Submit'}
        </button>
      </form>
    </div>
  );
}

export default FormPage; 