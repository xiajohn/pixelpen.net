import requests

app_id = "1921741401531325"
app_secret = ""
short_lived_token = ""

url = f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=fb_exchange_token&fb_exchange_token={short_lived_token}"

response = requests.get(url)

if response.status_code == 200:
    long_lived_token = response.json()["access_token"]
    print("Long-lived token:", long_lived_token)
else:
    print("Error:", response.json())
