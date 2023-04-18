import React, { useState } from 'react';
import { getServerURL } from '../util/utils';
import styles from '../css/Contact.module.css';
const Contact = () => {
    const [emailData, setEmailData] = useState({
        name: '',
        email: '',
        subject: '',
        message: '',
    });
    const Input = ({ type, name, placeholder, value, onChange }) => {
        if (type === 'textarea') {
            return (
                <textarea
                    name={name}
                    placeholder={placeholder}
                    value={value}
                    onChange={onChange}
                    required
                />
            );
        }
    
        return (
            <input
                type={type}
                name={name}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                required
            />
        );
    };
    const renderInput = (type, name, placeholder) => (
        <Input
          type={type}
          name={name}
          placeholder={placeholder}
          value={emailData[name]}
          onChange={handleChange}
        />
      );
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
                    subject: '',
                    message: '',
                });
            }
        } catch (error) {
            setResponseMessage('Error sending email, please try again later.');
        }
    };

    return (
        <div className={styles.container}>
          <h2>Contact Us</h2>
          <p>Please use the form below to send us a message.</p>
    
          {responseMessage && <p>{responseMessage}</p>}
    
          <form onSubmit={handleSubmit}>
            {renderInput('text', 'name', 'Name')}
            {renderInput('email', 'email', 'Email')}
            {renderInput('text', 'subject', 'Subject')}
            {renderInput('textarea', 'message', 'Message')}
            <button type="submit">Send Message</button>
          </form>
        </div>
      );
};


export default Contact;
