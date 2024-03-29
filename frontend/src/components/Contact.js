import React, { useState } from 'react';
import { Form, FormGroup, FormControl, Button } from 'react-bootstrap';
import { getServerURL } from '../util/utils';
import '../css/Contact.css';
import { Container } from 'react-bootstrap';
import {Helmet} from "react-helmet";
const Contact = () => {
  const [emailData, setEmailData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    setEmailData({ ...emailData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(getServerURL() + '/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(emailData),
      });

      const result = await response.json();
      setResponseMessage(result.message);

      if (response.ok) {
        setEmailData({
          name: '',
          email: '',
          message: '',
        });
      }
    } catch (error) {
      setResponseMessage('Error sending email, please try again later.');
    }
  };
  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  return (
    <Container className="contact-container"> {/* Additional class here */}
    <Helmet>
                <link rel="canonical" href="https://pixelpen.net/contact" />
            </Helmet>
      <h2>Contact Us</h2>
      <p>Please use the form below to send us a message.</p>

      {responseMessage && <p>{responseMessage}</p>}

      <Form onSubmit={handleSubmit} className="contact-form">
        {Object.keys(emailData).map((key) => (
          <FormGroup key={key}>
            <Form.Label>{capitalizeFirstLetter(key)}</Form.Label>
            <FormControl
              as={key === 'message' ? 'textarea' : 'input'}
              type={key === 'email' ? 'email' : 'text'}
              name={key}
              className="input"
              value={emailData[key]}
              onChange={handleChange}
              required
            />
          </FormGroup>
        ))}
        <Button type="submit" className="button">Send Message</Button>
      </Form>
    </Container>
  );
};

export default Contact;
