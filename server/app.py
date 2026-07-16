from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get the server ID from an environment variable.
# If none is provided, use "Server-1" by default.
SERVER_ID = os.getenv("SERVER_ID", "Server-1")


@app.route("/home", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Distributed Systems Server",
        "server": SERVER_ID
    })


@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return jsonify({
        "status": "healthy",
        "server": SERVER_ID
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)