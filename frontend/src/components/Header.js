import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import styles from '../css/Header.module.css';

function Header() {
    const navLinkStyle = {
        color: 'white',
    };

    return (
        <Navbar className={styles.navbar} expand>
            <Navbar.Brand className={styles.brand} href="#home">
                Pixel Pen
            </Navbar.Brand>
            <Nav className={styles.nav}>
                <Nav.Link style={navLinkStyle} href="#about">About</Nav.Link>
                <Nav.Link style={navLinkStyle} href="#contact">Contact</Nav.Link>
            </Nav>
        </Navbar>
    );
}

export default Header;
