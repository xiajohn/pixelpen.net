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
    Topic: 'Pixel Pen',
    Grade: '12',
    Word_Count: '100',
    Language: 'English',
  });
  const [essay, setEssay] = useState(
    "Title: The Legend of Pixel Pen\n\n" +
    "In a world of boundless creativity, there was a village called Pixellia, famous for its inhabitants' storytelling prowess. A young inventor named Penelope lived there, and she had created a device called 'Pixel Pen,' which could transform ideas into tangible forms.\n\n" +
    "Fast forward to modern society, advances in artificial intelligence have made it possible to bring the legend of Pixel Pen to life. This AI-driven platform harnesses the power of Penelope's mythical invention to help people transform their ideas into compelling narratives, engaging speeches, and captivating visuals.\n\n" +
    "In the digital age, where ideas travel at the speed of light, Pixel Pen has become an indispensable tool for creators and innovators. As it streamlines the creative process, it empowers individuals to focus on the essence of their ideas, while the AI handles the intricacies of expression.\n\n" +
    "The legend of Pixel Pen lives on, inspiring countless creators to tap into their imaginative potential, and in doing so, shape the future of human ingenuity.\n\n" +
    "So come, write down your idea with Pixel Pen and witness the magic of your vision coming to life!"
  );

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
