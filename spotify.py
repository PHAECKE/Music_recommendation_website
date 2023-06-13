from flask import Flask, request
import webbrowser
from urllib.parse import urlencode

app = Flask(__name__)


@app.route("/search")
def search():
    code = request.args.get("code")
    if code:
        # You can perform further actions with the obtained code here
        print("Authorization code:", code)
    else:
        print("Authorization code not found in redirect URL.")

    return "Code received successfully."


if __name__ == "__main__":
    client_id = "e2bfaf6e3a984beb857b404eb229901a"
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:5000/search",
        "scope": "user-library-read"
    }

    auth_url = "https://accounts.spotify.com/authorize?" + \
        urlencode(auth_headers)
    webbrowser.open_new_tab(auth_url)

    app.run(port=8000)
