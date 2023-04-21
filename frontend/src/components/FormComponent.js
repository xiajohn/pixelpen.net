import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import '../css/Form.css';
import { getServerURL } from '../util/utils';

function FormComponent({ formData, setFormData, setEssay, setIsLoading }) {
  const [showTopicError, setShowTopicError] = useState(false);
  const [showWordCountError, setShowWordCountError] = useState(false);
  const [showTopicChangedError, setShowTopicChangedError] = useState(false);

  const initialTopic = 'Pixel Pen'; // Set the initial topic value here

  // ... (rest of the code)

  // Add error messages for word count and topic change in the form
  {showWordCountError && (
    <div className="form-error" style={{ color: 'red' }}>
      Word count must be less than 2000
    </div>
  )}
  
  {showTopicChangedError && (
    <div className="form-error" style={{ color: 'red' }}>
      Please change the topic
    </div>
  )}
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setShowTopicError(false);
  };

  function validateFormData(formData) {
    // Initialize validation flags
    let valid = true;
  
    // Check if the topic field is empty
    if (!formData.Topic) {
      setShowTopicError(true);
      valid = false;
    } else {
      setShowTopicError(false);
    }
  
    // Check if the word count is less than 2000
    if (formData.WordCount > 2000) {
      setShowWordCountError(true);
      valid = false;
    } else {
      setShowWordCountError(false);
    }
  
    // Check if the topic has changed
    if (formData.Topic === initialTopic) {
      setShowTopicChangedError(true);
      valid = false;
    } else {
      setShowTopicChangedError(false);
    }
  
    return valid;
  }
  

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let generateEssayURL = getServerURL() + '/generate-essay';
  
    // Check if the topic has changed
    if (formData.Topic === initialTopic) {
      setShowTopicChangedError(true);
      setIsLoading(false);
      return;
    } else {
      setShowTopicChangedError(false);
    }
  
    if (validateFormData(formData)) {
      const payload = {
        grade: formData.Grade,
        wordCount: formData.Word_Count,
        topic: formData.Topic,
        language: formData.Language,
      };
  
      try {
        const response = await axios.post(generateEssayURL, payload);
        const essay = response.data.essay;
        console.log('Generated Essay:', essay);
        setEssay(essay);
      } catch (error) {
        console.error('Error generating essay:', error.message);
      }
      setIsLoading(false);
    } else {
      setIsLoading(false);
      return;
    }
  };
  

  return (
    <Form onSubmit={handleSubmit} className="form">
      <h1>Finish your essay free</h1>
      {Object.keys(formData).map((key) => (
        <Form.Group key={key} className="form-group">
          <Form.Label className="form-label">{key}</Form.Label>
          <Form.Control
            className="form-field"
            type="text"
            name={key}
            value={formData[key]}
            onChange={handleChange}
          />
        </Form.Group>
      ))}

      {showTopicError && (
        <div className="form-error" style={{ color: 'red' }}>
          Please enter a topic
        </div>
      )}

      <Button variant="primary" type="submit" className="form-btn">
        Generate Essay
      </Button>
    </Form>
  );
}

export default FormComponent;
