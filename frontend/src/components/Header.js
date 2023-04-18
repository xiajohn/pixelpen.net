import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import styles from '../css/Header.module.css';

function Header() {
    const navLinkStyle = {
        color: 'white',
    };

    return (
        <Navbar className={styles.navbar} expand>
            <Navbar.Brand className={styles.brand} as={Link} to="/">
                Pixel Pen
            </Navbar.Brand>
            <Nav className={styles.nav}>
                <Nav.Link as={Link} style={navLinkStyle} to="/about">About</Nav.Link>
                <Nav.Link as={Link} style={navLinkStyle} to="/contact">Contact</Nav.Link>
            </Nav>
        </Navbar>
    );
}

export default Header;
