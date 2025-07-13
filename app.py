import os
from flask import Flask

app = Flask(__name__)

HTML_STYLE = """
    <style>
        body {
            background-color: #0f0f0f;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            font-size: 3rem;
            text-align: center;
        }
    </style>
"""

HOME_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Nova Bot Dashboard</title>
    {HTML_STYLE}
</head>
<body>
    <h1>Welcome to Nova Bot Dashboard</h1>
</body>
</html>
"""

DASHBOARD_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    {HTML_STYLE}
</head>
<body>
    <h1>Dashboard Section</h1>
</body>
</html>
"""

MANAGER_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Manager</title>
    {HTML_STYLE}
</head>
<body>
    <h1>Manager Section</h1>
</body>
</html>
"""

@app.route("/")
def home():
    return HOME_HTML

@app.route("/dashboard")
def dashboard():
    return DASHBOARD_HTML

@app.route("/manager")
def manager():
    return MANAGER_HTML

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
