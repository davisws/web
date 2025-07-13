
from flask import Flask, request, session, redirect, render_template_string, jsonify
import os, json, requests

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecret")

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("REDIRECT_URI")
DISCORD_API_BASE = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

@app.route("/")
def index():
    return render_template_string("""
    <html><head><title>Nova Bot Dashboard</title></head>
    <body style='background:#0d1117;color:white;text-align:center;padding-top:10%'>
        <h1>Nova Bot Dashboard</h1>
        <a href='/login' style='background:#5865F2;color:white;padding:10px 20px;border-radius:10px;text-decoration:none;'>Login with Discord</a>
    </body></html>
    """)

@app.route("/login")
def login():
    return redirect(f"{DISCORD_API_BASE}/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code: return "Missing code", 400

    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": OAUTH_SCOPE,
    }
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    r = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    tokens = r.json()

    res = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    session["user"] = res.json()
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user: return redirect("/")
    with open("custom_commands.json", "r") as f:
        commands = json.load(f)
    return render_template_string("""
    <html><body style='background:#0d1117;color:white;padding:2em;'>
    <h2>Welcome, {{user["username"]}}</h2>
    <form method='POST' action='/commands/add'>
      Command Name: <input name='name'> Response: <input name='response'>
      <button type='submit'>Add</button>
    </form>
    <ul>{% for cmd in commands %}<li><b>{{cmd}}:</b> {{commands[cmd]}}</li>{% endfor %}</ul>
    </body></html>
    """, user=user, commands=commands)

@app.route("/commands/add", methods=["POST"])
def add_command():
    name = request.form["name"]
    response = request.form["response"]
    with open("custom_commands.json", "r") as f:
        commands = json.load(f)
    commands[name] = response
    with open("custom_commands.json", "w") as f:
        json.dump(commands, f, indent=2)
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
