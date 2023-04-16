const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;

app.get('/', (req, res) => {
  res.send('Hello from the backend server!');
});

app.post('/generate-essay', async (req, res) => {
  const { grade, wordCount, topic, language } = req.body;

  if (!grade || !wordCount || !topic) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  try {
    // Set up OpenAI API call
    const openaiURL = 'https://api.openai.com/v1/completions';
    let prompt = `Write a grade ${grade} level essay on the topic "${topic}" in approximately ${wordCount} words. The essay should be written in ${language}.`;

    const response = await axios.post(
      openaiURL,
      {
        model: 'text-davinci-003', // Update this with the desired model name
        prompt,
        max_tokens: parseInt(wordCount) + 50,
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

    const essay = response.data.choices[0].text.trim();
    res.status(200).json({ essay });
  } catch (error) {
    console.error('Error generating essay:', error.message);
    res.status(500).json({ error: 'Error generating essay.' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
