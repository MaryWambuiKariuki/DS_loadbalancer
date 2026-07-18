from flask import Flask, jsonify
import os

app = Flask(__name__)

# Read environment variables
SERVER_ID = os.getenv("SERVER_ID", "Server-1")
PORT = int(os.getenv("PORT", 5000))


@app.route("/")
def index():
    return jsonify({
        "message": "Distributed Systems Server",
        "server": SERVER_ID
    })


@app.route("/home")
def home():
    return jsonify({
        "message": "Welcome to the Distributed Systems Server",
        "server": SERVER_ID
    })


@app.route("/heartbeat")
def heartbeat():
    return jsonify({
        "status": "healthy",
        "server": SERVER_ID
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False
    )