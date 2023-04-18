import React, { useState } from 'react';
import Header from './components/Header';
import Body from './components/Body';
import FormComponent from './components/FormComponent';
import Essay from './components/Essay';
import './css/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About';
import Contact from './components/Contact';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </Router>
  );
}

function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    Topic: '',
    Grade: '12',
    Word_Count: '100',
    Language: 'English',
  });
  const [essay, setEssay] = useState('');

  return (
    <>
      {isLoading && (
        <div className="loading-mask">
          <div className="loader"></div>
        </div>
      )}
      <Body>
        <div className="input-form">
          <FormComponent
            formData={formData}
            setFormData={setFormData}
            setEssay={setEssay}
            setIsLoading={setIsLoading}
          />
        </div>
        <Essay content={essay} />
      </Body>
    </>
  );
}

export default App;
