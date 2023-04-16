import React, { useState } from 'react';
import logo from './logo.svg';
import './Header.css'; // add this line to import the styles from the Header.css file
import { Navbar, Nav, Container, Form, Button } from 'react-bootstrap';
import axios from 'axios';


function App() {
  const [grade, setGrade] = useState('');
  const [wordCount, setWordCount] = useState('');
  const [topic, setTopic] = useState('');
  const [essay, setEssay] = useState('');
  const [isLoading, setIsLoading] = useState(false); // state to manage loading indicator
  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true); // set loading indicator to true
  
    try {
      const response = await axios.post('http://nodejs-example-express-rds.eba-hqmwcdh2.us-west-2.elasticbeanstalk.com/generate-essay', {
        grade,
        wordCount,
        topic,
      });
  
      const essay = response.data.essay;
      console.log('Generated Essay:', essay);
      setEssay(essay); // set essay state
    } catch (error) {
      console.error('Error generating essay:', error.message);
    }
    setIsLoading(false); // set loading indicator to false
  };
  

  return (
    <div className="App">
      
      {isLoading && <div className="loading-mask"></div>}
      <Navbar className="App-header" expand="lg">
        <Container>
          <Navbar.Brand href="#home">
            <img
              src={logo}
              height="30"
              className="d-inline-block align-top"
              alt="ChatGPT Logo"
            />
            {' John Xia'}
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#about">About</Nav.Link>
              <Nav.Link href="#contact">Contact</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <header className="App-header-text"></header>
      <div className="center-text">
        <h1>Finish your essay free</h1>
      </div>
      <div className="input-form">
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Grade Level</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter grade level"
              value={grade}
              onChange={(e) => setGrade(e.target.value)}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Word Count</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter word count"
              value={wordCount}
              onChange={(e) => setWordCount(e.target.value)}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Topic</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            Generate Essay
          </Button>
        </Form>
      </div>

      {/* Display generated essay */}
      <div className="center-text">
        <h2>Essay</h2>
        <p>{essay}</p>
      </div>
    </div>
  );
}

export default App;
