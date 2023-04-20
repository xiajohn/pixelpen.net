function createLambdaResponse(statusCode, body) {
    return {
      statusCode: statusCode,
      headers: {
        'Access-Control-Allow-Origin': '*', // Replace '*' with your specific origin if needed
        'Access-Control-Allow-Credentials': true,
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST'
      },
      body: JSON.stringify(body),
    };
  }
  module.exports = { createLambdaResponse };