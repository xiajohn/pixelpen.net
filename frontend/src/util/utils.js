export const isDev = () => {
    return process.env.NODE_ENV !== 'production';
  };
  
  export function getServerURL() {
    let generateEssayURL;
  
    if (!isDev()) {
      generateEssayURL = 'https://oajkssts69.execute-api.us-west-2.amazonaws.com/production';
    } else {
      generateEssayURL = 'https://oajkssts69.execute-api.us-west-2.amazonaws.com/production';
    }
  
    return generateEssayURL;
  }
  