const axios = require('axios');
const { createLambdaResponse } = require('./utils');
require('dotenv').config({ path: '../.env' });

async function generateEssay(event) {
  const { topic } = JSON.parse(event.body);

  if (!topic) {
    return createLambdaResponse(400, { error: 'Topic is required.' });
  }

  try {
    const openaiURL = 'https://api.openai.com/v1/completions';
    let prompt = `Write a interesting story on the topic "${topic}" in approximately 500 words. Use a single html new line character to separate paragraphs Include a title`;

    const response = await axios.post(
      openaiURL,
      {
        model: 'text-davinci-002',
        prompt,
        max_tokens: 1000,
        n: 1,
        stop: null,
        temperature: 0.7,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        },
      }
    );

    const essay = response.data.choices[0].text;
    return createLambdaResponse(200, { essay: essay });

  } catch (error) {
    console.error('Error generating essay:', error.message);
    return createLambdaResponse(500, { error: 'Error generating essay.' });
  }
}

module.exports = { generateEssay };
