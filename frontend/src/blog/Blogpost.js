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
      const folderName = blog_name.replace(/ /g, '_');

      if (process.env.NODE_ENV === 'development') {
        // Load content from a local folder
        const response = await fetch(`/local_testing/${folderName}/blog_post.md`);
        const localContent = await response.text();
        setBlogContent(localContent);
      } else {
        const response = await axios.get(`https://d3qz51rq344usc.cloudfront.net/blog/${folderName}/blog_post.md`);
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
      <ReactMarkdown>{blogContent}</ReactMarkdown>
    </div>
  );
};

export default BlogPost;
