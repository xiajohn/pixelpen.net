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
      <div className={styles.left}></div>
      <div className={styles.center}>
        <Navbar.Brand className={styles.brand} as={Link} to="/">
          Pixel Pen
        </Navbar.Brand>
      </div>
      <div className={styles.right}>
        <Nav className={styles.nav}>
          {renderNavLink('/creative-showcase', 'Creative Showcase')}
          {renderNavLink('/about', 'About')}
          {renderNavLink('/contact', 'Contact')}
        </Nav>
      </div>
    </Navbar>
  );
  
  
}

export default Header;
