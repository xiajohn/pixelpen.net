const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());
const bodyParser = require('body-parser');
const AWS = require('aws-sdk');
const PORT = process.env.PORT || 3001;
const ses = new AWS.SES({ region: 'us-west-2' });
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
    res.status(200).json({ essay });
  } catch (error) {
    console.error('Error generating essay:', error.message);
    res.status(500).json({ error: 'Error generating essay.' });
  }
});

app.post('/send-email', async (req, res) => {
  const { name, email, message } = req.body;

  const params = {
    Destination: {
      ToAddresses: ['xiajohn@hotmail.com', 'meszter.17@gmail.com'],
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
    res.status(200).json({ message: 'Email sent successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error sending email' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
