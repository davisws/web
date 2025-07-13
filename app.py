import os
import json
import requests
from flask import Flask, session, redirect, request, url_for, render_template_string

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "changeme")  # secure this for production

DISCORD_CLIENT_ID = os.getenv("1392627972581621782")
DISCORD_CLIENT_SECRET = os.getenv("_-cFcAr3nZV8FEfRv7Mmiq48ShGq8o-5")
DISCORD_REDIRECT_URI = os.getenv("https://novabot.info/callback")  # should be https://yourdomain.com/callback

API_BASE_URL = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

# Simulated storage
custom_commands = {}

@app.route("/")
def home():
    if "user" in session:
        return redirect("/servers")
    return f'<a href="{url_for("login")}">Login with Discord</a>'

@app.route("/login")
def login():
    return redirect(f"{API_BASE_URL}/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": OAUTH_SCOPE
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{API_BASE_URL}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    tokens = r.json()
    session["token"] = tokens["access_token"]

    # Get user info
    headers = {"Authorization": f"Bearer {session['token']}"}
    user = requests.get(f"{API_BASE_URL}/users/@me", headers=headers).json()
    session["user"] = user

    return redirect("/servers")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/servers")
def servers():
    if "token" not in session:
        return redirect("/login")

    headers = {"Authorization": f"Bearer {session['token']}"}
    guilds = requests.get(f"{API_BASE_URL}/users/@me/guilds", headers=headers).json()

    html = "<h2>Your Servers</h2><ul>"
    for guild in guilds:
        html += f'<li><a href="/dashboard/{guild["id"]}">{guild["name"]}</a></li>'
    html += "</ul><a href='/logout'>Logout</a>"
    return html

@app.route("/dashboard/<guild_id>")
def dashboard(guild_id):
    commands = custom_commands.get(guild_id, [])
    html = f"<h2>Dashboard for Guild {guild_id}</h2>"
    html += "<h3>Custom Commands</h3><ul>"
    for cmd in commands:
        html += f"<li><b>{cmd['name']}</b>: {cmd['response']}</li>"
    html += "</ul>"
    html += f"""
        <form method="POST" action="/dashboard/{guild_id}/add">
            <input name="name" placeholder="Command name" required>
            <input name="response" placeholder="Response" required>
            <button type="submit">Add Command</button>
        </form>
        <br><a href="/servers">Back to servers</a>
    """
    return html

@app.route("/dashboard/<guild_id>/add", methods=["POST"])
def add_command(guild_id):
    name = request.form["name"]
    response = request.form["response"]
    if guild_id not in custom_commands:
        custom_commands[guild_id] = []
    custom_commands[guild_id].append({"name": name, "response": response})
    return redirect(f"/dashboard/{guild_id}")

# Run on Render (use gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
