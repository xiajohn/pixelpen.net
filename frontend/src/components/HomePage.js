// components/HomePage.js
import React, { useState } from 'react';
import Body from './Body';
import FormComponent from './FormComponent';
import Essay from './Essay';
import '../css/HomePage.css'
function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    Topic: '',
  });
  const [essay, setEssay] = useState(
    "Title: The Legend of Pixel Pen\n\n" +
    "In a world of boundless creativity, there was a village called Pixellia, famous for its inhabitants' storytelling prowess. A young inventor named Penelope lived there, and she had created a device called 'Pixel Pen,' which could transform ideas into tangible forms.\n\n" +
    "Fast forward to modern society, advances in artificial intelligence have made it possible to bring the legend of Pixel Pen to life. This AI-driven platform harnesses the power of Penelope's mythical invention to help people transform their ideas into compelling narratives, engaging speeches, and captivating visuals.\n\n" +
    "In the digital age, where ideas travel at the speed of light, Pixel Pen has become an indispensable tool for creators and innovators. As it streamlines the creative process, it empowers individuals to focus on the essence of their ideas, while the AI handles the intricacies of expression.\n\n" +
    "The legend of Pixel Pen lives on, inspiring countless creators to tap into their imaginative potential, and in doing so, shape the future of human ingenuity.\n\n" +
    "So come, write down your idea with Pixel Pen and witness the magic of your vision coming to life! We believe that AI can be integrated into almost every type of business, unlocking new opportunities for growth and innovation. If you share our vision and passion for harnessing the power of AI, we invite you to join us as partners in our quest to reshape the future. Together, we can unleash the full potential of Pixel Pen, revolutionizing industries and redefining what's possible in the realm of human creativity. Reach out to us and let's embark on this exciting journey of partnership and success!"
  );


  return (
    <>
      {isLoading && (
        <div className="loading-mask">
          <div className="loader"></div>
        </div>
      )}
      <div className="greeting">
        <h1>Crafting excellence, one idea at a time</h1>
        <p>Enhance your marketing and advertising with AI-powered content. Fast, high-quality, and tailored to your needs.</p>
        <p>Unlock the potential of your brand – <a href="/about">Explore our services</a>.</p>
      </div>


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

export default HomePage;
