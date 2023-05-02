const { handler } = require('../src/index');

const testEvent = {
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john.doe@example.com',
    message: 'Hello, I have a question about your services.',
  }),
  path: '/send-email',
};

(async () => {
  try {
    const result = await handler(testEvent);
    console.log('Result:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error:', error);
  }
})();
