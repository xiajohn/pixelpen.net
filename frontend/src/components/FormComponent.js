import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import '../css/Form.css';
import { getServerURL } from '../util/utils';

function FormComponent({ formData, setFormData, setEssay, setIsLoading, essayRef }) {
  const [showTopicError, setShowTopicError] = useState(false);

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

    return valid;
  }


  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let generateEssayURL = getServerURL() + '/generate-essay';

    if (validateFormData(formData)) {
      const payload = {
        topic: formData.Topic,
      };

      try {
        const response = await axios.post(generateEssayURL, payload);
        const essay = response.data.essay;
        setEssay(essay);
      } catch (error) {
        console.error('Error generating essay:', error.message);
      }
      setIsLoading(false);

      essayRef.current.scrollIntoView({ behavior: 'smooth' });
    } else {
      setIsLoading(false);
      return;
    }
  };



  return (
    <Form onSubmit={handleSubmit} className="form">
      <h1>Bring Your Idea to Life</h1>
      {Object.keys(formData).map((key) => (
        <Form.Group key={key} className="form-group">
          <Form.Label className="form-label">Whats on your mind?</Form.Label>
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
        Submit
      </Button>
    </Form>
  );
}

export default FormComponent;
