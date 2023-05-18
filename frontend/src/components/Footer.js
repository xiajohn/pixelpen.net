import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebookSquare } from '@fortawesome/free-brands-svg-icons';
import '../css/Footer.css';  // Assuming you have a separate CSS file for Footer

function Footer() {
  return (
    <div className="footer">
      <div className="left">
        <a href="https://www.facebook.com/pixelpenAI" target="_blank" rel="noreferrer">
          <FontAwesomeIcon icon={faFacebookSquare} size="2x" className="social-icon" />
        </a>
      </div>
      <div className="center">
        <p>&copy; 2023 PixelPen</p>
      </div>
      <div className="right">

      </div>
    </div>
  );
}

export default Footer;
