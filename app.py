import os
import json
import requests
from flask import Flask, redirect, request, session, render_template_string, url_for

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecret")

DISCORD_CLIENT_ID = os.getenv("1392627972581621782")
DISCORD_CLIENT_SECRET = os.getenv("_-cFcAr3nZV8FEfRv7Mmiq48ShGq8o-5")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "https://novabot.info/callback")

DISCORD_API_BASE = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

def is_authed():
    return "user" in session

@app.route("/")
def index():
    user = session.get("user")
    return render_template_string("""
    <html>
    <head>
        <title>Nova Bot Dashboard</title>
        <style>
            body { background: #0d1117; color: white; font-family: sans-serif; text-align: center; padding-top: 100px; }
            .btn { background: #5865F2; padding: 12px 24px; border: none; border-radius: 8px; color: white; text-decoration: none; font-size: 16px; }
            .btn:hover { background: #4752c4; }
        </style>
    </head>
    <body>
        <h1>Nova Bot Dashboard</h1>
        {% if user %}
            <p>Welcome, {{ user['username'] }}!</p>
            <a class="btn" href="/servers">Manage Servers</a><br><br>
            <a class="btn" href="/logout">Logout</a>
        {% else %}
            <a class="btn" href="/login">Login with Discord</a>
        {% endif %}
    </body>
    </html>
    """, user=user)

@app.route("/login")
def login():
    if not DISCORD_CLIENT_ID or not DISCORD_CLIENT_SECRET:
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

    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    token_res = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    token_res.raise_for_status()
    access_token = token_res.json()["access_token"]

    user_res = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    user_res.raise_for_status()
    session["user"] = user_res.json()
    session["access_token"] = access_token
    return redirect("/")

@app.route("/servers")
def servers():
    if not is_authed():
        return redirect("/")

    try:
        guilds_res = requests.get(
            f"{DISCORD_API_BASE}/users/@me/guilds",
            headers={"Authorization": f"Bearer {session['access_token']}"}
        )
        guilds_res.raise_for_status()
        guilds = guilds_res.json()
    except Exception as e:
        return f"Failed to fetch servers: {e}", 500

    return render_template_string("""
    <html>
    <head><title>Servers</title></head>
    <body style="background:#0d1117; color:white; text-align:center;">
        <h2>Manage Servers</h2>
        {% for g in guilds %}
            <div><a class="btn" href="/dashboard/{{ g['id'] }}">{{ g['name'] }}</a></div><br>
        {% endfor %}
        <a class="btn" href="/">Home</a>
    </body>
    </html>
    """, guilds=guilds)

@app.route("/dashboard/<guild_id>", methods=["GET", "POST"])
def dashboard(guild_id):
    if not is_authed():
        return redirect("/")

    path = f"data/{guild_id}.json"
    if not os.path.exists("data"):
        os.makedirs("data")

    if request.method == "POST":
        command = request.form.get("command")
        response = request.form.get("response")
        if command and response:
            with open(path, "w") as f:
                json.dump({"command": command, "response": response}, f)

    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        data = {"command": "", "response": ""}

    return render_template_string("""
    <html><head>
    <title>Custom Command</title>
    <style>
        body { background: #0d1117; color: white; text-align: center; padding-top: 100px; font-family: sans-serif; }
        input, textarea { padding: 10px; margin: 10px; width: 300px; border-radius: 8px; border: none; }
        button { background: #5865F2; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
        button:hover { background: #4752c4; }
    </style>
    </head>
    <body>
        <h1>Edit Custom Command</h1>
        <form method="POST">
            <input name="command" value="{{ data['command'] }}" placeholder="Command">
            <br>
            <textarea name="response" placeholder="Response">{{ data['response'] }}</textarea>
            <br>
            <button type="submit">Save</button>
        </form>
        <br><a class="btn" href="/servers">Back</a>
    </body></html>
    """, data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
