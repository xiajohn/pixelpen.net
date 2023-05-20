import React from 'react';

import './css/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About';
import Contact from './components/Contact';
import CreativeShowcase from './blog/CreativeShowcase';
import BlogPost from './blog/Blogpost';
import NotFound from './components/NotFound';
import HomePage from './components/HomePage';
import Header from './components/Header';
import { useState, useRef } from 'react';
import FormComponent from './components/FormComponent';
function App() {
 
  return (
    <Router>
      <Header className="header" />
<Routes className="body">
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route exact path="/creative-showcase" element={<CreativeShowcase />} />
          <Route path="/blog/:blog_name" element={<BlogPost />} />
          {/* Add catch-all route here */}
          <Route path="*" element={<NotFound />} />

        </Routes>
      
    </Router>

  );
}

export default App;
