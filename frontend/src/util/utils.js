export const isDev = () => {
    return process.env.NODE_ENV !== 'production';
  };
  
  export function getServerURL() {
    let generateEssayURL;
  
    if (!isDev()) {
      generateEssayURL = 'http://nodejs-example-express-rds.eba-hqmwcdh2.us-west-2.elasticbeanstalk.com';
    } else {
      generateEssayURL = 'http://localhost:3001';
    }
  
    return generateEssayURL;
  }
  