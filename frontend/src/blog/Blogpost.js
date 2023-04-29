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
      if (process.env.NODE_ENV === 'development') {
        // Load content from a local file (replace 'path/to/local/file.md' with the actual path)
        const response = await fetch('/blog_post.md');
        const localContent = await response.text();
        setBlogContent(localContent);
      } else {
        const filename = props.blogs[blog_name].filename;
        const response = await axios.get(`https://d3qz51rq344usc.cloudfront.net/blog/${filename}`);
        setBlogContent(response.data);
      }
      
    } catch (error) {
      console.log(error);
    }
  }, [blog_name, props.blogs]);

  useEffect(() => {
    fetchBlogContent();
  }, [fetchBlogContent]);


  return (
    <div className="blog">
      <ReactMarkdown >{blogContent}</ReactMarkdown>
    </div>
  );
};

export default BlogPost;
