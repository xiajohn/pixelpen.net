import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import styles from '../css/About.module.css';

function About() {
    return (
        <Container className={styles.aboutContainer}>
            <Row>
                <Col>
                    <h2>About Pixel Pen</h2>
                    <p>At Pixel Pen, we believe in the transformative power of ideas. In today's interconnected world, the internet has revolutionized the way ideas are shared and communicated through text, images, and video. However, crafting these mediums can be time-consuming and labor-intensive. This is where Pixel Pen comes in.</p>
                    <p>Leveraging state-of-the-art AI technology, Pixel Pen streamlines the creative process, seamlessly bringing your ideas to life in the form of compelling text, engaging speech, or captivating video. Our mission is to empower you to focus on what matters most - the idea itself - while our intelligent platform handles the rest.</p>
                    <p>Join us on our journey to revolutionize the way ideas are shared and let Pixel Pen be the catalyst that amplifies your creativity and propels your vision into reality.</p>
                </Col>
            </Row>
            <Row>
                <Col>
                    <h3>Our Services</h3>
                    <p>We provide a range of services to help you create high-quality content and grow your business:</p>
                    <ul>
                        <li><strong>Web Development:</strong> Custom website design and development to showcase your brand and products.</li>
                        <li><strong>Blog Posts:</strong> Engaging and informative articles to attract visitors and boost your online presence.</li>
                        <li><strong>Email Campaigns:</strong> Targeted email marketing campaigns to nurture leads and increase conversions.</li>
                    </ul>
                    <p>Interested in our services? Get in touch with us to discuss your project requirements and explore how we can work together to bring your ideas to life. We're here to help and can't wait to hear from you!</p>
                </Col>
            </Row>

            <Row>
                <Col>
                    <h2>About the Author</h2>
                    <p>Hello, I'm John, the driving force behind Pixel Pen. Unlike large corporations, my aim isn't to build an empire, but rather to make an honest living by doing what I love - helping others bring their creative visions to life.</p>
                    <p>I cherish the one-on-one relationships I build with my clients, treating them not just as customers but as individuals with unique ideas and goals. To me, business isn't just about transactions, it's about understanding, respect, and shared objectives.</p>
                    <p>Whether it's designing a custom website, crafting an engaging blog post, or creating a targeted email campaign, I use every tool at my disposal - including state-of-the-art AI technology when it fits - to deliver top-notch services and help your business grow.</p>
                    <p>If you're ready to transform your ideas into reality, I'm here to help. Let's discuss your projects, your vision, and how we can collaborate to create something exceptional. I can't wait to start this journey with you!</p>
                    <p>Best, John</p>
                </Col>
            </Row>
            <Row>
                <Col>
                    <h3>Our Mission</h3>
                    <p>Our mission is to craft excellence, one idea at a time</p>
                </Col>
            </Row>

            <Row>
                <Col>
                    <h3>Privacy Policy</h3>
                    <p>We do not collect any data from you</p>
                </Col>
            </Row>
        </Container>
    );
}

export default About;

