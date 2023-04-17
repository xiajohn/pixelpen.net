import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import '../css/Form.css';
function FormComponent({ formData, setFormData, setEssay, setIsLoading }) {
  

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let generateEssayURL = '';
    if(process.env.IS_DEV_ENV === 'true') {
      generateEssayURL = 'http://nodejs-example-express-rds.eba-hqmwcdh2.us-west-2.elasticbeanstalk.com/generate-essay'
    }
    else{
      generateEssayURL = 'http://localhost:3001/generate-essay'
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
            type="text"
            placeholder={`Enter ${key}`}
            name={key}
            value={formData[key]}
            onChange={handleChange}
          />
        </Form.Group>
      ))}
      <Button variant="primary" type="submit">
        Generate Essay
      </Button>
    </Form>
  );
}

export default FormComponent;