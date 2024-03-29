const AWS = require('aws-sdk');
const ses = new AWS.SES({ region: 'us-west-1' });
const { createLambdaResponse } = require('./utils');

async function sendEmail(event) {
  const { name, email, message } = JSON.parse(event.body);

  const params = {
    Destination: {
      ToAddresses: ['xiajohn@hotmail.com'],
    },
    Message: {
      Body: {
        Text: {
          Data: `Name: ${name}\nEmail: ${email}\nMessage: ${message}`,
        },
      },
      Subject: {
        Data: 'New message from your website',
      },
    },
    Source: 'no-reply@pixelpen.net',
  };

  try {
    await ses.sendEmail(params).promise();
    return createLambdaResponse(200, { message: 'Email sent successfully' });
  } catch (error) {
    console.error(error);
    return createLambdaResponse(500, { message: 'Error sending email' });
  }
}

module.exports = { sendEmail };
