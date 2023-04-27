export const isDev = () => {
    return process.env.NODE_ENV !== 'production';
  };
  
  export function getServerURL() {
    return 'https://npl5znk8j4.execute-api.us-west-1.amazonaws.com/prod';
  }
  