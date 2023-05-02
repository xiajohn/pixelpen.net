import requests

app_id = "1921741401531325"
app_secret = "5cd0a9a4b146e0dc560709195d168496"
short_lived_token = "EAAbT0EmWo70BABxXZAfpAZCaa4RvNoQqi1DSPc5DsYqyur46tL7OZCAX3ZBVdubAD9p5sR5h1mS7ifdhejgZBp2DFR5suqOLc9mZAbH2HZC7ALIkhKfm76ZBEDFHww2c0iCcDcJ09IRz0e7POuTxWZBsfqOYQ3xn67FZBWQlgyVTXaZCgqK02sxgV14dpCThDDFk8bQb5H5fOfDdmgW1OyNJscG"

url = f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=fb_exchange_token&fb_exchange_token={short_lived_token}"

response = requests.get(url)

if response.status_code == 200:
    long_lived_token = response.json()["access_token"]
    print("Long-lived token:", long_lived_token)
else:
    print("Error:", response.json())
