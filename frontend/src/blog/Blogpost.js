import React, { useState, useEffect, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import '../css/Blog.css';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { fetchMetadata } from '../util/utils.js'

const BlogPost = () => {
  const { blog_name } = useParams();
  const [blogContent, setBlogContent] = useState('');
  const folderName = blog_name.replace(/ /g, '_');

  const fetchBlogContent = useCallback(async () => {
    try {
      if (process.env.NODE_ENV === 'development') {
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
  }, [blog_name]);

  useEffect(() => {
    fetchBlogContent();
    fetchMetadata()
      .then(meta => updateMetadata(meta))
      .catch(error => console.log(error));
  }, [blog_name, fetchBlogContent]);

  function updateMetadata(response) {
    var meta = response[folderName]['meta'];
    document.title = meta.title;
  
    const descriptionTag = document.querySelector('meta[name="description"]');
    descriptionTag.setAttribute('content', meta.description);
  
    const keywordsTag = document.querySelector('meta[name="keywords"]');
    keywordsTag.setAttribute('content', meta.keywords);
  }

  const replaceImagePlaceholders = (content) => {
    return content.replace(/{ImagePlaceholder(\d+)}/g, (match, number) => {
      const imagePath = process.env.NODE_ENV === 'development'
        ? `/local_testing/${folderName}/image_data_${number}.jpg`
        : `https://d3qz51rq344usc.cloudfront.net/blog/${folderName}/image_data_${number}.jpg`;
      return `![Description](${imagePath})`;
    });
  };

  const finalContent = replaceImagePlaceholders(blogContent);

  return (
    <div className="blog">
      <ReactMarkdown>{finalContent}</ReactMarkdown>
    </div>
  );
};

export default BlogPost;
