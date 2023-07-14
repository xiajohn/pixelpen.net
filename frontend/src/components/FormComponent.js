import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import '../css/Form.css';
import { getServerURL } from '../util/utils';
import styles from '../css/Essay.module.css';

function FormComponent({ formData, setFormData, setEssay, setIsLoading, essayRef }) {
  const [showTopicError, setShowTopicError] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setShowTopicError(false);
  };

  function validateFormData(formData) {
    let valid = true;

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
        essayRef.current.classList.add(styles.highlight);
        if (essayRef.current) {
          essayRef.current.classList.add(styles.highlight);
          setTimeout(() => {
            if (essayRef.current) {
              essayRef.current.classList.remove(styles.highlight);
            }
          }, 3000);
        }
      } catch (error) {
        console.error('Error generating essay:', error.message);
      }
      setIsLoading(false);
      window.scrollTo(0, document.body.scrollHeight);

    } else {
      setIsLoading(false);
      return;
    }
  };

  return (
    <Form onSubmit={handleSubmit} className="form-container">
      <div className="input-group">
        <Form.Control
          className="form-input"
          type="text"
          name="Topic"
          placeholder="Your idea"
          value={formData.Topic}
          onChange={handleChange}
        />
        <Button variant="primary" type="submit" className="form-button">
          See Preview
        </Button>
      </div>
      {showTopicError && (
        <div className="form-error" style={{ color: 'red' }}>
          Please enter a topic
        </div>
      )}
    </Form>
  );
  
}

export default FormComponent;
