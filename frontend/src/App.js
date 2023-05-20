import React from 'react';
import Header from './components/Header';
import Body from './components/Body';
import Essay from './components/Essay';
import Footer from './components/Footer';

import './css/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About';
import Contact from './components/Contact';
import CreativeShowcase from './blog/CreativeShowcase';
import BlogPost from './blog/Blogpost';
import NotFound from './components/NotFound';
import HomePage from './components/HomePage';
import { useState, useRef } from 'react';
import FormComponent from './components/FormComponent';
function App() {
  const [isLoading, setIsLoading] = useState(false);
  const essayRef = useRef(null);
  const [essay, setEssay] = useState(
    "Title: The Legend of Pixel Pen\n\n" +
    "In a world of boundless creativity, there was a village called Pixellia, famous for its inhabitants' storytelling prowess. A young inventor named Penelope lived there, and she had created a device called 'Pixel Pen,' which could transform ideas into tangible forms.\n\n" +
    "Fast forward to modern society, advances in artificial intelligence have made it possible to bring the legend of Pixel Pen to life. This AI-driven platform harnesses the power of Penelope's mythical invention to help people transform their ideas into compelling narratives, engaging speeches, and captivating visuals.\n\n" +
    "In the digital age, where ideas travel at the speed of light, Pixel Pen has become an indispensable tool for creators and innovators. As it streamlines the creative process, it empowers individuals to focus on the essence of their ideas, while the AI handles the intricacies of expression.\n\n" +
    "The legend of Pixel Pen lives on, inspiring countless creators to tap into their imaginative potential, and in doing so, shape the future of human ingenuity.\n\n" +
    "So come, write down your idea with Pixel Pen and witness the magic of your vision coming to life! We believe that AI can be integrated into almost every type of business, unlocking new opportunities for growth and innovation. If you share our vision and passion for harnessing the power of AI, we invite you to join us as partners in our quest to reshape the future. Together, we can unleash the full potential of Pixel Pen, revolutionizing industries and redefining what's possible in the realm of human creativity. Reach out to us and let's embark on this exciting journey of partnership and success!"
  );
  const [formData, setFormData] = useState({
    Topic: '',
  });
  return (
    <Router>
      {isLoading && (
        <div className="loading-mask">
          <div className="loader"></div>
        </div>
      )}

      <div className="App">
        <Header className="header" />
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
        </section>
        <Routes className="body">
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route exact path="/creative-showcase" element={<CreativeShowcase />} />
          <Route path="/blog/:blog_name" element={<BlogPost />} />
          {/* Add catch-all route here */}
          <Route path="*" element={<NotFound />} />

        </Routes>
        <Body>
          <Essay ref={essayRef} content={essay} />
        </Body>
        <Footer />
      </div>
    </Router>

  );
}

export default App;
