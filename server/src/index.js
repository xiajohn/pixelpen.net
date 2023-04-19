const { handler: generateEssayHandler } = require('./generateEssay');
const { handler: sendEmailHandler } = require('./sendEmail');

exports.handler = async (event) => {
  const path = event.path.toLowerCase();
  if (path === '/generate-essay') {
    return await generateEssayHandler(event);
  } else if (path === '/send-email') {
    return await sendEmailHandler(event);
  } else {
    return {
      statusCode: 404,
      body: JSON.stringify({ message: 'Endpoint not found' }),
    };
  }
};
