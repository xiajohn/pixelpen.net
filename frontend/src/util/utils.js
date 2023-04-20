export const isDev = () => {
    return process.env.NODE_ENV !== 'production';
  };
  
  export function getServerURL() {
    let generateEssayURL;
  
    if (!isDev()) {
      generateEssayURL = 'https://oajkssts69.execute-api.us-west-2.amazonaws.com/prod';
    } else {
      generateEssayURL = 'https://oajkssts69.execute-api.us-west-2.amazonaws.com/prod';
    }
  
    return generateEssayURL;
  }
  