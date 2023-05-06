const { handler } = require('../src/index'); // Update the import based on your project structure

const testEvent = {
  body: JSON.stringify({
    topic: 'The future of AI',
  }),
  path: '/generate-essay', // Update the path to match the one in your project
};

(async () => {
  try {
    const result = await handler(testEvent); // Update the function name if necessary
    console.log('Result:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error:', error);
  }
})();
