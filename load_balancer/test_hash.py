from consistent_hash import ConsistentHash

ring = ConsistentHash()

ring.add_server("Server-1")
ring.add_server("Server-2")
ring.add_server("Server-3")

print("Before removing Server-2")
requests = [
    "Request-A",
    "Request-B",
    "Request-C",
    "Request-D",
    "Request-E"
]

for request in requests:
    print(f"{request} -> {ring.get_server(request)}")

print("\nRemoving Server-2...\n")

ring.remove_server("Server-2")

print("After removing Server-2")

for request in requests:
    print(f"{request} -> {ring.get_server(request)}")