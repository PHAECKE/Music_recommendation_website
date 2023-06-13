import requests
from urllib.parse import urlencode
import base64
import webbrowser

client_id = "e2bfaf6e3a984beb857b404eb229901a"
client_secret = "02125e4dfdbd49d693f977ab6e5c71ab"

# encodes the client_id and the client_secret using base64 and then decode to utf-8
encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}

token_data = {
    "grant_type": "authorization_code", # 
    "code": code,
    "redirect_uri": "http://localhost:5000/search"
}

r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
token = r.json()["access_token"]

print(token)
