import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import './css/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from './components/About';
import Contact from './components/Contact';
import CreativeShowcase from './blog/CreativeShowcase'; 
import BlogPost from './blog/Blogpost'; 
import NotFound from './components/NotFound';
import HomePage from './components/HomePage'; 

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route exact path="/creative-showcase" element={<CreativeShowcase />} /> 
          <Route path="/blog/:blog_name" element={<BlogPost />} />
          {/* Add catch-all route here */}
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
