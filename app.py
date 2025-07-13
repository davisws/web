from flask import Flask, Response

app = Flask(__name__)

# 🏠 Home route (main dashboard)
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
        html {
          scroll-behavior: smooth;
        }

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
        <a href="/">Home</a>
        <a href="/manager">Manager</a>
        <a href="/settings">Settings</a>
      </nav>

      <section id="overview">
        <h1>NovaBot Dashboard 🚀</h1>
        <p>Manage your server settings, create custom commands, and control NovaBot like a pro.</p>
      </section>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')


# ⚙️ /manager route
@app.route("/manager")
def manager():
    html = """
    <html>
    <head>
      <title>Manager Panel</title>
      <style>
        body {
          background-color: #0a0a0a;
          color: #ffffff;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          text-align: center;
          padding: 100px;
        }
        a {
          color: #00aaff;
          text-decoration: none;
          font-weight: bold;
        }
      </style>
    </head>
    <body>
      <h1>🧠 Manager Panel</h1>
      <p>Custom command editor coming soon...</p>
      <br><br>
      <a href="/">← Back to Dashboard</a>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


# ⚙️ /settings route
@app.route("/settings")
def settings():
    html = """
    <html>
    <head>
      <title>Settings</title>
      <style>
        body {
          background-color: #0a0a0a;
          color: #ffffff;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          text-align: center;
          padding: 100px;
        }
        a {
          color: #00aaff;
          text-decoration: none;
          font-weight: bold;
        }
      </style>
    </head>
    <body>
      <h1>⚙️ Settings</h1>
      <p>Server preferences, logging, and bot behavior settings coming soon.</p>
      <br><br>
      <a href="/">← Back to Dashboard</a>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
