const path = require('path');
const webpack = require('webpack');
const dotenv = require('dotenv');

const env = dotenv.config().parsed;

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'index.js',
    libraryTarget: 'commonjs'
  },
  target: 'node',
  mode: 'production',
  plugins: [
    new webpack.EnvironmentPlugin(['OPENAI_API_KEY']),
  ],
};
