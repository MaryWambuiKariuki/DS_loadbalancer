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

SERVER_IMAGE = "distributed_systems_project-server"

NETWORK_NAME = "ds_network"


# -------------------------------------------------------
# Create Docker Container
# -------------------------------------------------------

def create_server(server_name, server_id):

    try:

        client.containers.run(
            image=SERVER_IMAGE,
            name=server_name,
            detach=True,
            network=NETWORK_NAME,
            environment={
                "SERVER_ID": server_name,
                "PORT": 5000
            },
        )

        servers[server_name] = {
            "id": server_id,
            "host": server_name,
            "port": 5000
        }

        ring.add_server(server_name, server_id)

        print(f"{server_name} created successfully")

    except Exception as e:

        print(f"Error creating {server_name}: {e}")


# -------------------------------------------------------
# Delete Docker Container
# -------------------------------------------------------

def delete_server(server_name):

    try:

        container = client.containers.get(server_name)

        container.stop()

        container.remove()

        ring.remove_server(server_name)

        servers.pop(server_name, None)

        print(f"{server_name} removed successfully")

    except Exception as e:

        print(f"Error removing {server_name}: {e}")


# -------------------------------------------------------
# Start Initial Replicas
# -------------------------------------------------------

def discover_servers():
    """
    Discover all running backend containers created by Docker Compose.
    """

    containers = client.containers.list()

    for container in containers:

        name = container.name

        if name.startswith("server"):

            server_id = int(name.replace("server", ""))

            servers[name] = {
                "id": server_id,
                "host": name,
                "port": 5000
            }

            ring.add_server(
                name,
                server_id
            )

            print(f"Discovered {name}")   

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
    server_id = 1
    
    while f"server{server_id}" in servers:
        server_id += 1
    
    server_name = f"server{server_id}"
    create_server(server_name, server_id)
    
    return jsonify({
     "message": f"{server_name} added successfully",
     "total_servers": len(servers),
     "replicas": list(servers.keys())
}), 201


# -------------------------------------------------------
# DELETE /rm
# Removes a server replica
# -------------------------------------------------------

@app.route("/rm", methods=["DELETE"])
def remove_server():

    if len(servers) <= 1:
        return jsonify( {
            "error": "Cannot remove the last server."
        }), 400
    
    # Remove the server with the highest ID
    server_name = sorted(
        servers.keys(),
        key=lambda x: int(x.replace("server", ""))
        )[-1]
    
    delete_server(server_name)
    return jsonify({
        "message": f"{server_name} removed successfully",
        "total_servers": len(servers),
        "replicas": list(servers.keys())
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

    # Generate request ID
    request_id = request.args.get("id", path)
    request_id = abs(hash(str(request_id)))

    # Get server from consistent hash ring
    server_name = ring.get_server(request_id)
    print("Selected:", server_name)
    print("Servers:", servers)

    if server_name is None:
        return jsonify({
            "error": "Hash ring is empty"
        }), 503

    server = servers.get(server_name)

    if server is None:
        return jsonify({
            "error": "Server not found"
        }), 503

    url = f"http://{server['host']}:{server['port']}/{path}"

    try:
        response = requests.get(url, timeout=2)

        return jsonify(response.json())

    except Exception as e:
        print(e)

        return jsonify({
            "error": str(e)
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

                url = f"http://{server_name}:5000/heartbeat"

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
    server_id = info["id"]

    print(f"Recovering {server_name}...")

    try:
        delete_server(server_name)
    except Exception:
        pass

    time.sleep(2)

    create_server(
        server_name,
        server_id
    )

    print(f"{server_name} recovered.")

# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":

    discover_servers()

    heartbeat_thread = threading.Thread(
        target=heartbeat_monitor,
        daemon=True
    )

    heartbeat_thread.start()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False, 
        threaded=True
    )