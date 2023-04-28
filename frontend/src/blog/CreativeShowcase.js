import React from 'react';
import { Link } from 'react-router-dom';

const CreativeShowcase = ({ blogs }) => {
  return (
    <div>
      <h1>Pixel Pen Creative Showcase</h1>
      <p>
        Welcome to the Pixel Pen Creative Showcase, where we promote our partners and their innovative ideas. Feel free to explore the featured products and stories from our current clients. These blogs serve as a powerful platform for generating attention and showcasing your idea to the world.
      </p>
      {Object.keys(blogs).map((key) => (
        <div key={key}>
          <Link to={`/blog/${key}`}>
            <h2>{blogs[key].title}</h2>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default CreativeShowcase;
