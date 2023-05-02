const { handler } = require('../src/index'); // Update the import based on your project structure

const testEvent = {
  body: JSON.stringify({
    grade: '12',
    wordCount: '500',
    topic: 'The future of AI',
    language: 'en',
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
