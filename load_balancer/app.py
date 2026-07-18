from flask import Flask, jsonify
import requests

from consistent_hash import ConsistentHash

app = Flask(__name__)

# ----------------------------------------
# Create the Consistent Hash Ring
# ----------------------------------------

ring = ConsistentHash()

servers = {
    "Server-1": "http://localhost:5000",
    "Server-2": "http://localhost:5001",
    "Server-3": "http://localhost:5002"
}

for server in servers:
    ring.add_server(server)

# ----------------------------------------
# Home Endpoint
# ----------------------------------------

@app.route("/")
def index():
    return jsonify({
        "message": "Distributed Systems Load Balancer"
    })


# ----------------------------------------
# Forward Requests
# ----------------------------------------

@app.route("/home/<request_id>")
def home(request_id):

    server = ring.get_server(request_id)

    try:
        response = requests.get(
            f"{servers[server]}/home"
        )

        return response.json()

    except Exception:

        return jsonify({
            "error": f"{server} is unavailable"
        }), 500


# ----------------------------------------
# View Active Replicas
# ----------------------------------------

@app.route("/rep")
def replicas():

    return jsonify({
        "replicas": list(servers.keys())
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)