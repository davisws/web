import os
import json
import requests
from flask import Flask, redirect, request, session, url_for, render_template_string

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecret")

DISCORD_CLIENT_ID = os.getenv("1392627972581621782")
DISCORD_CLIENT_SECRET = os.getenv("_-cFcAr3nZV8FEfRv7Mmiq48ShGq8o-5")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "https://novabot.info/callback")
DISCORD_API_BASE = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

# HTML Templates
LOGIN_TEMPLATE = '''
<html>
<head><title>Login</title></head>
<body>
    <h1>Nova Bot Dashboard</h1>
    <a href="/login">Login with Discord</a>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<html>
<head><title>Dashboard</title></head>
<body>
    <h1>Welcome, {{user['username']}}</h1>
    <h3>Your Servers</h3>
    <ul>
    {% for guild in guilds %}
        <li><a href="/dashboard/{{guild['id']}}">{{guild['name']}}</a></li>
    {% endfor %}
    </ul>
    <a href="/logout">Logout</a>
</body>
</html>
'''

COMMANDS_TEMPLATE = '''
<html>
<head><title>Custom Commands</title></head>
<body>
    <h1>Custom Commands for {{guild_id}}</h1>
    <ul>
    {% for cmd, response in commands.items() %}
        <li><b>{{cmd}}</b>: {{response}}</li>
    {% endfor %}
    </ul>
    <form method="post">
        <input name="command" placeholder="Command name" required />
        <input name="response" placeholder="Response" required />
        <button type="submit">Add/Update</button>
    </form>
    <br><a href="/dashboard">Back</a>
</body>
</html>
'''

# Routes
@app.route("/")
def index():
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/login")
def login():
    if not all([DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET]):
        return "Missing environment variables"
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
    response = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    response.raise_for_status()
    tokens = response.json()

    user_res = requests.get(
        f"{DISCORD_API_BASE}/users/@me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    user = user_res.json()

    guilds_res = requests.get(
        f"{DISCORD_API_BASE}/users/@me/guilds",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    guilds = guilds_res.json()

    session["user"] = user
    session["guilds"] = guilds
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template_string(DASHBOARD_TEMPLATE, user=session["user"], guilds=session["guilds"])

@app.route("/dashboard/<guild_id>", methods=["GET", "POST"])
def custom_commands(guild_id):
    if "user" not in session:
        return redirect("/")

    commands_path = f"commands/{guild_id}.json"
    os.makedirs("commands", exist_ok=True)

    if request.method == "POST":
        command = request.form.get("command")
        response = request.form.get("response")
        with open(commands_path, "r+" if os.path.exists(commands_path) else "w+") as f:
            try:
                cmds = json.load(f)
            except:
                cmds = {}
            cmds[command] = response
            f.seek(0)
            f.write(json.dumps(cmds))
            f.truncate()

    if os.path.exists(commands_path):
        with open(commands_path) as f:
            commands = json.load(f)
    else:
        commands = {}

    return render_template_string(COMMANDS_TEMPLATE, guild_id=guild_id, commands=commands)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
