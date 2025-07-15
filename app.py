import os
import json
import glob
import requests
from flask import Flask, redirect, request, session, render_template_string, url_for

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecret")

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "https://novabot.info/callback")

DISCORD_API_BASE = "https://discord.com/api"
OAUTH_SCOPE = "identify guilds"

COMMANDS_FOLDER = "data"
GLOBAL_COMMANDS_FILE = "commands.json"

def is_authed():
    return "user" in session

def load_commands_file(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_commands_file(path, commands):
    with open(path, "w") as f:
        json.dump(commands, f, indent=4)

def sync_guilds_to_global():
    all_commands = {}
    if not os.path.exists(COMMANDS_FOLDER):
        os.makedirs(COMMANDS_FOLDER)
    for filename in glob.glob(os.path.join(COMMANDS_FOLDER, "*.json")):
        guild_commands = load_commands_file(filename)
        # Merge, allowing later guilds to overwrite same commands if any
        all_commands.update(guild_commands)
    save_commands_file(GLOBAL_COMMANDS_FILE, all_commands)

@app.route("/")
def index():
    user = session.get("user")
    return render_template_string("""
    <html><head><title>Nova Bot Dashboard</title><style>
        body { background: #0d1117; color: white; font-family: sans-serif; text-align: center; padding-top: 100px; }
        .btn { background: #5865F2; padding: 12px 24px; border: none; border-radius: 8px; color: white; text-decoration: none; font-size: 16px; }
        .btn:hover { background: #4752c4; }
    </style></head><body>
        <h1>Nova Bot Dashboard</h1>
        {% if user %}
            <p>Welcome, {{ user['username'] }}!</p>
            <a class="btn" href="/servers">Manage Servers</a><br><br>
            <a class="btn" href="/logout">Logout</a>
        {% else %}
            <a class="btn" href="/login">Login with Discord</a>
        {% endif %}
    </body></html>
    """, user=user)

@app.route("/login")
def login():
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
    token_res = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    token_res.raise_for_status()
    access_token = token_res.json()["access_token"]

    user_res = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    session["user"] = user_res.json()
    session["access_token"] = access_token
    return redirect("/")

@app.route("/servers")
def servers():
    if not is_authed():
        return redirect("/")

    guilds_res = requests.get(
        f"{DISCORD_API_BASE}/users/@me/guilds",
        headers={"Authorization": f"Bearer {session['access_token']}"}
    )
    guilds = guilds_res.json()
    return render_template_string("""
    <html><head><title>Servers</title><style>
        body { background:#0d1117; color:white; text-align:center; font-family:sans-serif; padding-top:100px; }
        .btn { background: #5865F2; padding: 12px 24px; border: none; border-radius: 8px; color: white; text-decoration: none; font-size: 16px; }
        .btn:hover { background: #4752c4; }
    </style></head><body>
        <h2>Manage Servers</h2>
        {% for g in guilds %}
            <div><a class="btn" href="/dashboard/{{ g['id'] }}">{{ g['name'] }}</a></div><br>
        {% endfor %}
        <a class="btn" href="/">Home</a>
    </body></html>
    """, guilds=guilds)

@app.route("/dashboard/<guild_id>", methods=["GET", "POST"])
def dashboard(guild_id):
    if not is_authed():
        return redirect("/")

    if not os.path.exists(COMMANDS_FOLDER):
        os.makedirs(COMMANDS_FOLDER)
    path = os.path.join(COMMANDS_FOLDER, f"{guild_id}.json")

    commands = load_commands_file(path)

    if request.method == "POST":
        # Add or update command
        command = request.form.get("command")
        response = request.form.get("response")
        if command and response:
            commands[command.lower()] = response
            save_commands_file(path, commands)
            sync_guilds_to_global()  # Sync all guilds to global commands.json

    # Delete command
    delete_cmd = request.args.get("delete")
    if delete_cmd:
        if delete_cmd.lower() in commands:
            del commands[delete_cmd.lower()]
            save_commands_file(path, commands)
            sync_guilds_to_global()

    return render_template_string("""
    <html><head><title>Custom Commands - {{ guild_id }}</title><style>
        body { background: #0d1117; color: white; text-align: center; padding-top: 30px; font-family: sans-serif; }
        input, textarea { padding: 10px; margin: 10px 0; width: 300px; border-radius: 8px; border: none; }
        button, a.btn { background: #5865F2; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px 5px; }
        button:hover, a.btn:hover { background: #4752c4; }
        table { margin: 0 auto; border-collapse: collapse; width: 80%; }
        th, td { padding: 12px; border-bottom: 1px solid #444; }
        th { text-align: left; }
        a.delete { color: #e74c3c; cursor: pointer; text-decoration: none; }
    </style></head><body>
        <h1>Custom Commands for Guild: {{ guild_id }}</h1>

        <form method="POST">
            <input name="command" placeholder="Command name" required>
            <textarea name="response" placeholder="Response text" required></textarea><br>
            <button type="submit">Add / Update Command</button>
        </form>

        {% if commands %}
            <h2>Existing Commands</h2>
            <table>
                <tr><th>Command</th><th>Response</th><th>Delete</th></tr>
                {% for cmd, resp in commands.items() %}
                    <tr>
                        <td>{{ cmd }}</td>
                        <td>{{ resp }}</td>
                        <td><a class="delete" href="{{ url_for('dashboard', guild_id=guild_id) }}?delete={{ cmd }}">Delete</a></td>
                    </tr>
                {% endfor %}
            </table>
        {% else %}
            <p>No commands set yet.</p>
        {% endif %}

        <br><a class="btn" href="/servers">Back to servers</a>
    </body></html>
    """, guild_id=guild_id, commands=commands)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

