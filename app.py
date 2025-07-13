from flask import Flask, redirect, request, session, url_for, render_template_string
import os
import requests

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "super-secret")

# Load env vars properly (DO NOT hardcode values!)
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "https://novabot.info/callback")

DISCORD_API_BASE = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

# ---------- Homepage with Styled Login ----------
@app.route("/")
def index():
    return render_template_string("""
    <html>
    <head>
        <title>Nova Bot Dashboard</title>
        <style>
            body {
                background: #0d1117;
                color: #f0f6fc;
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 15%;
            }
            .button {
                background-color: #5865F2;
                color: white;
                padding: 15px 25px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                text-decoration: none;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
            .button:hover {
                background-color: #4752c4;
            }
        </style>
    </head>
    <body>
        <h1>Nova Bot Dashboard</h1>
        <a href="/login" class="button">Login with Discord</a>
    </body>
    </html>
    """)

# ---------- Login Redirect ----------
@app.route("/login")
def login():
    return redirect(
        f"{DISCORD_API_BASE}/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE.replace(' ', '%20')}"
    )

# ---------- OAuth Callback ----------
@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": OAUTH_SCOPE,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    response.raise_for_status()
    tokens = response.json()

    user_res = requests.get(
        f"{DISCORD_API_BASE}/users/@me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    user_res.raise_for_status()
    user = user_res.json()

    session["user"] = user
    return f"Welcome, {user['username']}!"

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
