// components/HomePage.js
import React, { useState, useRef } from 'react';


import FormComponent from './FormComponent';

import Essay from './Essay';

import Body from './Body';

import Footer from './Footer';

import '../css/HomePage.css'
function HomePage() {

  const [isLoading, setIsLoading] = useState(false);
  const essayRef = useRef(null);
  const [essay, setEssay] = useState(
    "In a world of boundless creativity, there was a village called Pixellia, famous for its inhabitants' storytelling prowess. A young inventor named Penelope lived there, and she had created a device called 'Pixel Pen,' which could transform ideas into tangible forms.\n\n" +
    "Fast forward to modern society, advances in artificial intelligence have made it possible to bring the legend of Pixel Pen to life. This AI-driven platform harnesses the power of Penelope's mythical invention to help people transform their ideas into compelling narratives, engaging speeches, and captivating visuals.\n\n" +
    "In the digital age, where ideas travel at the speed of light, Pixel Pen has become an indispensable tool for creators and innovators. As it streamlines the creative process, it empowers individuals to focus on the essence of their ideas, while the AI handles the intricacies of expression.\n\n" +
    "So come, write down your idea with Pixel Pen and witness the magic of your vision coming to life! Together, we can unleash the full potential of Pixel Pen, revolutionizing industries and redefining what's possible in the realm of human creativity!"
  );
  const [formData, setFormData] = useState({
    Topic: '',
  });




  return (
    <>
      {isLoading && (
              <div className="loading-mask">
                <div className="loader"></div>
              </div>
            )}

      <section className="hero">
        <div className="hero-container">
          <div className="greeting">
            <h1>AI Marketting Solutions</h1>
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
      </section>

     
        <Essay ref={essayRef} content={essay} />
     
    </>

  );
}

export default HomePage;
