import React, { useState, useEffect, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import '../css/Blog.css';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { fetchMetadata } from '../util/utils.js';
import {Helmet} from "react-helmet";
const BlogPost = () => {
  const { blog_name } = useParams();
  const [blogContent, setBlogContent] = useState('');
  const folderName = blog_name.replace(/ /g, '-');

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
    const fetchData = async () => {
      await fetchBlogContent();
      
      try {
        const meta = await fetchMetadata();
        updateMetadata(meta[folderName]['meta']);
      } catch (error) {
        console.log(error);
      }
    };

    fetchData();
  }, [blog_name, fetchBlogContent]);

  function updateMetadata(meta) {
    document.title = meta.title;

    const descriptionTag = document.querySelector('meta[name="description"]');
    descriptionTag.setAttribute('content', meta.description);

    const keywordsTag = document.querySelector('meta[name="keywords"]');
    keywordsTag.setAttribute('content', meta.keywords);

    
  }

  const replaceImagePlaceholders = (content) => {
    return content.replace(/ImagePlaceholder(\d+)/g, (match, number) => {
      const imagePath = process.env.NODE_ENV === 'development'
        ? `/local_testing/${folderName}/image_data_${number}.jpg`
        : `https://d3qz51rq344usc.cloudfront.net/blog/${folderName}/image_data_${number}.jpg`;

      // You can replace 'Your Alt Text Here' with a relevant description for your image
      const altText = folderName;

      return `![${altText}](${imagePath})`;
    });
  };

  const finalContent = replaceImagePlaceholders(blogContent);

  return (
    <div className='blog-cont'>
      <Helmet>
                <link rel="canonical" href={`https://www.pixelpen.net/blog/${folderName}`} />
            </Helmet>
    <div className="blog">
      <ReactMarkdown>{finalContent}</ReactMarkdown>
    </div>
    </div>
  );
};

export default BlogPost;
