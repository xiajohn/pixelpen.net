
const { generateEssay } = require('./generateEssay');
const { sendEmail } = require('./sendEmail');

exports.handler = async (event) => {
    console.log('Received event: and is latest change', JSON.stringify(event, null, 2));
  const path = event.path.toLowerCase();
  if (path === '/generate-essay') {
    return await generateEssay(event);
  } else if (path === '/send-email') {
    return await sendEmail(event);
  } else {
    return {
      statusCode: 404,
      body: JSON.stringify({ message: 'Endpoint not found' }),
    };
  }
};
