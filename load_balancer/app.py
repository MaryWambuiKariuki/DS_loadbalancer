import docker
from flask import Flask, jsonify, request
import requests
from consistent_hash import ConsistentHash

app = Flask(__name__)
client = docker.from_env()

# -----------------------------------
# Consistent Hash Ring
# -----------------------------------

ring = ConsistentHash()

servers = {}

# Default replicas
for i in range(1, 4):

    name = f"Server-{i}"

    servers[name] = f"http://server{i}:5000"

    ring.add_server(name, i)

# -----------------------------------
# GET /rep
# -----------------------------------

@app.route("/rep", methods=["GET"])
def get_replicas():

    return jsonify({

        "N": len(servers),

        "replicas": list(servers.keys())

    })

# -----------------------------------
# POST /add
# -----------------------------------

@app.route("/add", methods=["POST"])
def add_server():

    data = request.get_json()

    hostname = data["hostname"]

    server_id = len(servers) + 1

    servers[hostname] = f"http://{hostname}:5000"

    ring.add_server(hostname, server_id)

    return jsonify({

        "message": f"{hostname} added",

        "N": len(servers)

    }), 201

# -----------------------------------
# DELETE /rm
# -----------------------------------

@app.route("/rm", methods=["DELETE"])
def remove_server():

    data = request.get_json()

    hostname = data["hostname"]

    if hostname not in servers:

        return jsonify({

            "error": "Server not found"

        }), 404

    ring.remove_server(hostname)

    del servers[hostname]

    return jsonify({

        "message": f"{hostname} removed",

        "N": len(servers)

    })

# -----------------------------------
# Route Client Requests
# -----------------------------------

@app.route("/<path:path>", methods=["GET"])
def route_request(path):

    request_id = abs(hash(path))

    server = ring.get_server(request_id)

    url = f"{servers[server]}/{path}"

    try:

        response = requests.get(url)

        return jsonify(response.json())

    except Exception:

        return jsonify({

            "error": f"{server} unavailable"

        }), 500

# -----------------------------------

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )