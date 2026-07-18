from consistent_hash import ConsistentHash

ring = ConsistentHash()

# Add three physical servers
ring.add_server("Server-1", 1)
ring.add_server("Server-2", 2)
ring.add_server("Server-3", 3)

print("=" * 60)
print("HASH RING")
print("=" * 60)

ring.display_ring()

print()

print("=" * 60)
print("SERVER SLOTS")
print("=" * 60)

for server, slots in ring.server_slots.items():
    print(server, "->", slots)

print()

print("=" * 60)
print("REQUEST ROUTING")
print("=" * 60)

requests = [
    101,
    202,
    303,
    404,
    505,
    606,
    707,
    808
]

for request in requests:

    server = ring.get_server(request)

    print(f"Request {request} ---> {server['name']}")

print()

print("=" * 60)
print("REMOVE SERVER-2")
print("=" * 60)

ring.remove_server("Server-2")

for request in requests:

    server = ring.get_server(request)

    print(f"Request {request} ---> {server['name']}")