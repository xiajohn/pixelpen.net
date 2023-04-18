import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import styles from '../css/About.module.css';

function About() {
    return (
        <Container className={styles.aboutContainer}>
            <Row>
                <Col>
                    <h2>About Pixel Pen</h2>
                    <p>
                        Ideas are powerful. With the invention of the internet, transfer of ideas globally became possible through text images and video. But it takes a lot of work to create those things. With the invention of AI, pixel pen can do it for you. From idea to text or speech or video, pixel pen will do it for you so you can focus on the idea.
                    </p>
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
