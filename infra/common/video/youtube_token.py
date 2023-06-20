from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Set up OAuth 2.0 credentials
client_secrets_file = 'youtube.json'
scopes = ['https://www.googleapis.com/auth/youtube']

# Set up the OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
print(authorization_url)
# Redirect the user to the authorization URL and obtain the authorization code

# Once you have the authorization code, exchange it for an access token
authorization_code = 'YOUR_AUTHORIZATION_CODE'
flow.fetch_token(authorization_response='https://localhost:8080/?code=' + authorization_code)

# Obtain the access token
credentials = flow.credentials
access_token = credentials.token
refresh_token = credentials.refresh_token

# Now you can use the access token to authenticate API requests
# Include the access token in the Authorization header of your requests: 'Authorization: Bearer {access_token}'
