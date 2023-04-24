const path = require('path');

module.exports = {
  entry: {
    main: './src/index.js',
    blog: './src/blog/blog.js',
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
  },
  target: 'node',
  mode: 'production',
};
