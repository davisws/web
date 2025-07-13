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

def load_commands():
    if not os.path.exists("commands.json"):
        return {}
    with open("commands.json") as f:
        return json.load(f)

def save_commands(cmds):
    with open("commands.json", "w") as f:
        json.dump(cmds, f, indent=4)

@app.route("/")
def index():
    return render_template_string("""
    <html><head><title>Nova Bot Dashboard</title>
    <style>
        body { background: #0d1117; color: white; font-family: Arial; text-align: center; padding-top: 10%; }
        .btn { background: #5865F2; color: white; padding: 10px 20px; font-size: 18px; border-radius: 8px; text-decoration: none; }
    </style>
    </head>
    <body>
        <h1>Nova Bot Dashboard</h1>
        <a href="/login" class="btn">Login with Discord</a>
    </body></html>
    """)

@app.route("/login")
def login():
    return redirect(
        f"{DISCORD_API_BASE}/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE}"
    )

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
    response = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    response.raise_for_status()
    tokens = response.json()
    user_res = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={ "Authorization": f"Bearer {tokens['access_token']}" })
    user_res.raise_for_status()
    user = user_res.json()
    session["user"] = user
    return redirect("/dashboard")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        cmds = request.json
        save_commands(cmds)
        return jsonify({"status": "success"})

    cmds = load_commands()
    return render_template_string("""
    <html><head><title>Command Manager</title>
    <style>
        body { background: #0d1117; color: white; font-family: Arial; padding: 20px; }
        input, button { padding: 10px; font-size: 16px; margin: 5px; }
        .command { margin-bottom: 10px; }
        .btn { background: #5865F2; color: white; border: none; border-radius: 6px; }
        .btn:hover { background: #4752c4; }
    </style>
    <script>
        async function saveCommands() {
            const cmds = {};
            document.querySelectorAll('.command').forEach(div => {
                const name = div.querySelector('.name').value;
                const resp = div.querySelector('.response').value;
                if (name && resp) cmds[name] = resp;
            });
            await fetch("/dashboard", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(cmds)
            });
            alert("Commands saved!");
        }

        function addField(name='', response='') {
            const div = document.createElement("div");
            div.className = "command";
            div.innerHTML = `<input class='name' placeholder='!command' value="\${name}">
                             <input class='response' placeholder='Bot response' value="\${response}">
                             <button onclick='this.parentElement.remove()'>❌</button>`;
            document.getElementById("cmds").appendChild(div);
        }

        window.onload = function() {
            const data = {{ cmds|tojson }};
            for (let cmd in data) addField(cmd, data[cmd]);
        }
    </script>
    </head><body>
        <h2>Welcome {{ session['user']['username'] }}</h2>
        <div id="cmds"></div>
        <button class="btn" onclick="addField()">➕ Add Command</button>
        <button class="btn" onclick="saveCommands()">💾 Save</button>
        <a href="/logout" style="margin-left:20px;color:#999;">Logout</a>
    </body></html>
    """, cmds=cmds)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
