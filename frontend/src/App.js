import React, { useState } from 'react';
import Header from './components/Header';
import Body from './components/Body';
import FormComponent from './components/FormComponent';
import Essay from './components/Essay';
import './css/App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    Grade: '',
    Word_Count: '',
    Topic: '',
    Language: '',
  });
  const [essay, setEssay] = useState('');

  return (
    <div className="App">
      {isLoading && (
        <div className="loading-mask">
          <div className="loader"></div>
        </div>
      )}
      <Header />
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
    </div>
  );
}

export default App;
