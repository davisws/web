from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>NovaBot Dashboard</title>
      <style>
        body {
          background-color: #0a0a0a;
          color: #ffffff;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 0;
        }

        nav {
          background-color: #111;
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-around;
          position: sticky;
          top: 0;
          border-bottom: 1px solid #222;
        }

        nav a {
          color: white;
          text-decoration: none;
          font-weight: bold;
        }

        section {
          padding: 80px 20px;
          text-align: center;
          border-bottom: 1px solid #222;
        }

        h1 {
          font-size: 3rem;
          margin-bottom: 20px;
        }

        h2 {
          font-size: 2rem;
          margin-bottom: 10px;
        }

        p {
          font-size: 1.2rem;
          max-width: 800px;
          margin: 0 auto;
          line-height: 1.6;
        }
      </style>
    </head>
    <body>
      <nav>
        <a href="#overview">Overview</a>
        <a href="#commands">Custom Commands</a>
        <a href="#settings">Settings</a>
      </nav>

      <section id="overview">
        <h1>NovaBot Dashboard 🚀</h1>
        <p>Manage your server settings, create custom commands, and control NovaBot.</p>
      </section>

      <section id="commands">
        <h2>🛠️ Custom Commands</h2>
        <p>Here you’ll be able to create and manage custom bot commands for your server.</p>
      </section>

      <section id="settings">
        <h2>⚙️ Settings</h2>
        <p>Customize NovaBot’s behavior, connect your Discord server, and more settings coming soon!</p>
      </section>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=True)
