import React, { useState, useEffect, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import '../css/Blog.css';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const BlogPost = (props) => {
  const { blog_name } = useParams();
  const [blogContent, setBlogContent] = useState('');

  const fetchBlogContent = useCallback(async () => {
    try {
      const filename = props.blogs[blog_name].filename;
      const response = await axios.get(`https://d3qz51rq344usc.cloudfront.net/blog/${filename}`);
      setBlogContent(response.data);
    } catch (error) {
      console.log(error);
    }
  }, [blog_name, props.blogs]);

  useEffect(() => {
    fetchBlogContent();
  }, [fetchBlogContent]);

  const renderers = {
    image: (props) => <img src={props.src} alt={props.alt} />,
  };

  return (
    <div className="blog">
      <ReactMarkdown renderers={renderers}>{blogContent}</ReactMarkdown>
    </div>
  );
};

export default BlogPost;
