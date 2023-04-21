const axios = require('axios');
const { createLambdaResponse } = require('./utils');

async function generateEssay(event) {
  const { grade, wordCount, topic, language } = JSON.parse(event.body);

  if (!topic) {
    return createLambdaResponse(400, { error: 'Topic is required.' });
  }

  try {
    const openaiURL = 'https://api.openai.com/v1/completions';
    let prompt = `Write a grade ${grade} level essay on the topic "${topic}" in approximately ${wordCount} words. The essay should be written in ${language}. Use a single html new line character to separate paragraphs Include a title`;

    const response = await axios.post(
      openaiURL,
      {
        model: 'text-davinci-003',
        prompt,
        max_tokens: parseInt(wordCount) + 100,
        n: 1,
        stop: null,
        temperature: 0.7,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer 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`,
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
