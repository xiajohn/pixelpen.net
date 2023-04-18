import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import '../css/Form.css';
import {getServerURL} from '../util/utils';

function FormComponent({ formData, setFormData, setEssay, setIsLoading }) {
  const [showTopicError, setShowTopicError] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setShowTopicError(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let generateEssayURL = getServerURL() + '/generate-essay';

    // Check if the topic field is empty
    if (!formData.Topic) {
      setShowTopicError(true);
      setIsLoading(false);
      return;
    }

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
