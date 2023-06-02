import React, { forwardRef } from 'react';
import styles from '../css/Essay.module.css';
import { Row, Col } from 'react-bootstrap';
const Essay = forwardRef(({ content }, ref) => {
  return (
    <div className={styles.essay} ref={ref}>
      
      <Row>
        <Col>
          <h2>Our Services</h2>
          <p>We provide a range of services to help you create high-quality content and grow your business:</p>
          <ul>
            <li><strong>Web Development:</strong> Custom website design and development to showcase your brand and products.</li>
            <li><strong>Blog Posts:</strong> Engaging and informative articles to attract visitors and boost your online presence.</li>
            <li><strong>Email Campaigns:</strong> Targeted email marketing campaigns to nurture leads and increase conversions.</li>
            <li><strong>Social Media Presence</strong> Automated high quality social media posts to showcase your brand and product</li>
          </ul>
          <p>Interested in our services? Get in touch with us to discuss your project requirements and explore how we can work together to bring your ideas to life. We're here to help and can't wait to hear from you!</p>
        </Col>
      </Row>
      <h3>Pixel Pen Preview</h3>
      <p dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br>') }}></p>
    </div>
  );
})

export default Essay;
