import os
import requests
from flask import Flask, redirect, request, session, render_template_string

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecret")

DISCORD_CLIENT_ID = os.getenv("1392627972581621782")
DISCORD_CLIENT_SECRET = os.getenv("_-cFcAr3nZV8FEfRv7Mmiq48ShGq8o-5")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "https://novabot.info/callback")

DISCORD_API_BASE = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

@app.route("/")
def index():
    return render_template_string("""
    <html><head><title>Nova Bot</title></head>
    <body style='background:#0d1117;color:white;text-align:center;padding-top:20%;font-family:sans-serif;'>
        <h1>Nova Bot Dashboard</h1>
        <a href="/login" style='padding:15px 30px; background:#5865F2; color:white; border:none; border-radius:10px; text-decoration:none;'>Login with Discord</a>
    </body></html>
    """)

@app.route("/login")
def login():
    if not DISCORD_CLIENT_ID or not DISCORD_REDIRECT_URI:
        return "Missing environment variables", 500
    return redirect(
        f"{DISCORD_API_BASE}/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE}"
    )

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

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        token_response = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")

        user_response = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        user_response.raise_for_status()
        user = user_response.json()

        session["user"] = user
        return f"<h1>Welcome, {user['username']}!</h1>"

    except Exception as e:
        return f"OAuth error: {str(e)}", 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
