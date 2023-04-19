export function createLambdaResponse(statusCode, body) {
    return {
      statusCode: statusCode,
      headers: {
        'Access-Control-Allow-Origin': '*', // Replace '*' with your specific origin if needed
        'Access-Control-Allow-Credentials': true,
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify(body),
    };
  }
  