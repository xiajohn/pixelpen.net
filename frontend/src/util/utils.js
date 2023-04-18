// urlHelper.js
export function getServerURL() {
    let generateEssayURL;
  
    if (!process.env.REACT_APP_IS_DEV_ENV) {
        console.log(process.env.IS_DEV_ENV);
      generateEssayURL = 'http://nodejs-example-express-rds.eba-hqmwcdh2.us-west-2.elasticbeanstalk.com';
    } else {
      generateEssayURL = 'http://localhost:3001';
    }
  
    return generateEssayURL;
  }
  