// CreativeShowcase.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchMetadata } from '../util/utils.js';
import '../css/CreativeShowcase.css'; // Import the CSS file
import {Helmet} from "react-helmet";
const CreativeShowcase = () => {
  const [blogs, setBlogs] = useState({});

  function removeEdgeQuotes(str) {
    if (str.startsWith('"') && str.endsWith('"')) {
      return str.substring(1, str.length - 1);
    }
    return str;
  }
  
  useEffect(() => {
    const fetchBlogs = async () => {
      const blogData = await fetchMetadata();
      if (blogData) {
        setBlogs(blogData);
      }
    };

    fetchBlogs();
  }, []);
  return (
    <div className="CreativeShowcase">
      <Helmet>
                <link rel="canonical" href="https://pixelpen.net/creative-showcase" />
            </Helmet>
      <h1>Pixel Pen Creative Showcase</h1>
      <p>
        Welcome to the Pixel Pen Creative Showcase, where we promote our
        partners and their innovative ideas. Feel free to explore the featured
        products and stories from our blogs. These blogs serve as a
        powerful platform for generating attention and showcasing your idea to
        the world.
      </p>
      {Object.keys(blogs).map((key) => (
        <Link key={key} to={`/blog/${key}`} className="blog-link">
          <h2>{removeEdgeQuotes(blogs[key].title)}</h2>
        </Link>
      ))}
    </div>
  );
};


export default CreativeShowcase;
