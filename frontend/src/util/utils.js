export const isDev = () => {
  return process.env.NODE_ENV !== 'production';
};

export function getServerURL() {
  return 'https://npl5znk8j4.execute-api.us-west-1.amazonaws.com/prod';
}
// utils.js
export const fetchMetadata = async () => {
  try {
    let response;
    if (process.env.NODE_ENV === 'development') {
      response = await fetch('/local_testing/blogs.json');
    } else {
      response = await fetch('https://d3qz51rq344usc.cloudfront.net/blog/blogs.json');
    }
    const metadata = await response.json();
    return metadata;
  } catch (error) {
    console.log(error);
    return null;
  }
};
