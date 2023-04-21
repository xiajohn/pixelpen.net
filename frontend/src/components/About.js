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
                    <h3>Our Mission</h3>
                    <p>
                        Our mission is to craft excellence, one idea at a time
                    </p>
                </Col>
            </Row>
        </Container>
    );
}

export default About;