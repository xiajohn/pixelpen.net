import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebookSquare, faYoutube } from '@fortawesome/free-brands-svg-icons';  // Import YouTube icon
import '../css/Footer.css';

function Footer() {
  return (
    <div className="footer">
      <div className="left">
        <a href="https://www.facebook.com/pixelpenAI" target="_blank" rel="noreferrer">
          <FontAwesomeIcon icon={faFacebookSquare} size="2x" className="facebook" />
        </a>
        <a href="https://www.youtube.com/channel/UCSEGGNe3H8534_1YUgDR7QA" target="_blank" rel="noreferrer">
          <FontAwesomeIcon icon={faYoutube} size="2x" className="social-icon" />  {/* Add YouTube icon */}
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
