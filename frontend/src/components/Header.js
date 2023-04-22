import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import styles from '../css/Header.module.css';
import logo from '../assets/logo.png'; // Import the logo image

function Header() {
  const navLinkStyle = {
    color: 'white',
  };

  const renderNavLink = (path, label) => (
    <Nav.Link as={Link} style={navLinkStyle} to={path}>
      {label}
    </Nav.Link>
  );

  return (
    <Navbar className={styles.navbar} expand>
      <Navbar.Brand className={styles.brand} as={Link} to="/">
        <img
          src={logo}
          alt="Logo"
          className={styles.logo} // Add a new class for logo styling
        />
        Pixel Pen
      </Navbar.Brand>
      <Nav className={styles.nav}>
        {renderNavLink('/blog', 'Blog')}
        {renderNavLink('/about', 'About')}
        {renderNavLink('/contact', 'Contact')}
      </Nav>
    </Navbar>
  );
}

export default Header;
