from flask import Flask, jsonify, request
import requests
import docker
import threading
import time

from consistent_hash import ConsistentHash

# -------------------------------------------------------
# Flask Application
# -------------------------------------------------------

app = Flask(__name__)

# -------------------------------------------------------
# Docker Client
# -------------------------------------------------------

client = docker.from_env()

# -------------------------------------------------------
# Consistent Hash Ring
# -------------------------------------------------------

ring = ConsistentHash()

# -------------------------------------------------------
# Server Registry
# Stores server name and URL
# -------------------------------------------------------

servers = {}

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

BASE_PORT = 5001

INITIAL_SERVERS = 3

SERVER_IMAGE = "ds-server"

NETWORK_NAME = "distributed_systems_project_ds_network"


# -------------------------------------------------------
# Create Docker Container
# -------------------------------------------------------

def create_server(server_name, server_id, port):

    try:

        client.containers.run(
            image=SERVER_IMAGE,
            name=server_name,
            detach=True,

            environment={
                "SERVER_ID": server_name,
                "PORT": 5000
            },

            ports={
                "5000/tcp": port
            },

            network=NETWORK_NAME
        )

        servers[server_name] = {
            "id": server_id,
            "port": port
        }

        ring.add_server(server_name, server_id)

        print(f"{server_name} started on localhost:{port}")

    except Exception as e:

        print(e)


# -------------------------------------------------------
# Delete Docker Container
# -------------------------------------------------------

def delete_server(server_name):

    try:

        container = client.containers.get(server_name)

        container.stop()

        container.remove()

        ring.remove_server(server_name)

        del servers[server_name]

        print(f"{server_name} removed")

    except Exception as e:

        print(e)


# -------------------------------------------------------
# Start Initial Replicas
# -------------------------------------------------------

def initialize_servers():

    for i in range(1, INITIAL_SERVERS + 1):

        name = f"Server-{i}"

        port = BASE_PORT + i - 1

        create_server(
            name,
            i,
            port
        )

        # -------------------------------------------------------
# GET /rep
# Returns all active replicas
# -------------------------------------------------------

@app.route("/rep", methods=["GET"])
def get_replicas():

    return jsonify({
        "N": len(servers),
        "replicas": list(servers.keys())
    })


# -------------------------------------------------------
# POST /add
# Adds a new server replica
# -------------------------------------------------------

@app.route("/add", methods=["POST"])
def add_server():

    data = request.get_json()

    if not data or "hostname" not in data:

        return jsonify({
            "error": "hostname is required"
        }), 400

    hostname = data["hostname"]

    if hostname in servers:

        return jsonify({
            "error": "Server already exists"
        }), 400

    server_id = len(servers) + 1

    port = BASE_PORT + len(servers)

    create_server(
        hostname,
        server_id,
        port
    )

    return jsonify({
        "message": f"{hostname} added successfully",
        "total_servers": len(servers)
    }), 201


# -------------------------------------------------------
# DELETE /rm
# Removes a server replica
# -------------------------------------------------------

@app.route("/rm", methods=["DELETE"])
def remove_server():

    data = request.get_json()

    if not data or "hostname" not in data:

        return jsonify({
            "error": "hostname is required"
        }), 400

    hostname = data["hostname"]

    if hostname not in servers:

        return jsonify({
            "error": "Server does not exist"
        }), 404

    delete_server(hostname)

    return jsonify({
        "message": f"{hostname} removed successfully",
        "total_servers": len(servers)
    })

# -------------------------------------------------------
# Route Incoming Client Requests
# -------------------------------------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET"])
def route_request(path):

    if len(servers) == 0:

        return jsonify({
            "error": "No servers available"
        }), 503

    # Generate a request ID
    request_id = abs(hash(path))

    server = ring.get_server(request_id)

    if server is None:

        return jsonify({
            "error": "Hash ring is empty"
        }), 503

    server_name = server["name"]

    port = servers[server_name]["port"]

    url = f"http://{server_name.lower().replace('-', '')}:5000/{path}"
    
    try:

        response = requests.get(url, timeout=2)

        return jsonify(response.json())

    except Exception:

        return jsonify({
            "error": f"{server_name} is unavailable"
        }), 500

        # -------------------------------------------------------
# Heartbeat Monitor
# -------------------------------------------------------

def heartbeat_monitor():

    while True:

        time.sleep(5)

        failed_servers = []

        for server_name, info in list(servers.items()):

            try:

                url = f"http://localhost:{info['port']}/heartbeat"

                response = requests.get(
                    url,
                    timeout=2
                )

                if response.status_code != 200:

                    failed_servers.append(server_name)

            except Exception:

                failed_servers.append(server_name)

        for server_name in failed_servers:

            print(f"{server_name} has failed.")

            recover_server(server_name)


            # -------------------------------------------------------
# Recover Failed Server
# -------------------------------------------------------

def recover_server(server_name):

    if server_name not in servers:

        return

    info = servers[server_name]

    port = info["port"]

    server_id = info["id"]

    print(f"Recovering {server_name}...")

    try:

        delete_server(server_name)

    except Exception:
        pass

    time.sleep(2)

    create_server(
        server_name,
        server_id,
        port
    )

    print(f"{server_name} recovered.")

    # -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":

    initialize_servers()

    heartbeat_thread = threading.Thread(
        target=heartbeat_monitor,
        daemon=True
    )

    heartbeat_thread.start()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )