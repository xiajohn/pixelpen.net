from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "youtube.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    return build('youtube', 'v3', credentials=flow.run_local_server())

def initialize_upload(youtube, file, metadata):
    request = youtube.videos().insert(
        part="snippet,status",
        body=metadata,
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )
    return request

def upload_video(file, metadata):
    youtube = get_authenticated_service()
    request = initialize_upload(youtube, file, metadata)
    response = request.execute()

    print(response)

