from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "NovaBot dashboard coming soon!"

if __name__ == "__main__":
    app.run()
