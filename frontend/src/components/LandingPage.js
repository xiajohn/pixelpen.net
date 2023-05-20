import React, { useState, useRef } from 'react';
import FormComponent from './FormComponent';
import Body from './Body';
import Essay from './Essay';

const LandingPage = () => {
  const [formData, setFormData] = useState({ Topic: '' });
  const [essay, setEssay] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const essayRef = useRef();

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="greeting">
          <h1>Create content with Pixel Pen</h1>
          <p>Enhance your marketing and advertising with AI-powered content. Fast, high-quality, and tailored to your needs.</p>
          <p>Unlock the potential of your brand.</p>
          <FormComponent
            formData={formData}
            setFormData={setFormData}
            setEssay={setEssay}
            setIsLoading={setIsLoading}
            essayRef={essayRef}
          />
        </div>
      </div>
      <Body>
        <Essay ref={essayRef} content={essay} />
      </Body>
    </section>
  );
};

export default LandingPage;
