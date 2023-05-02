import requests
import os
from dotenv import load_dotenv
load_dotenv()
page_id = "121834987557525"
access_token = os.getenv("FACEBOOK_ACCESS_KEY")
print(access_token)
message = "Your random text here"

url = f"https://graph.facebook.com/{page_id}/feed"
payload = {
    "message": message,
    "access_token": access_token
}

response = requests.post(url, data=payload)
print(response.json())
