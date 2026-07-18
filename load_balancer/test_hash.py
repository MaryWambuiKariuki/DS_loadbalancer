from consistent_hash import ConsistentHash

ring = ConsistentHash()

# Add the three servers
ring.add_server("Server-1", 1)
ring.add_server("Server-2", 2)
ring.add_server("Server-3", 3)

print("=" * 60)
print("SERVERS ON HASH RING")
print("=" * 60)

for server, slots in ring.server_slots.items():
    print(f"{server}: {slots}")

print()

print("=" * 60)
print("REQUEST MAPPING")
print("=" * 60)

requests = [
    123456,
    234567,
    345678,
    456789,
    567890,
    678901,
    789012,
    890123
]

for request in requests:
    server = ring.get_server(request)
    print(f"Request {request} ---> {server}")

print()

print("=" * 60)
print("REMOVING SERVER-2")
print("=" * 60)

ring.remove_server("Server-2")

for request in requests:
    server = ring.get_server(request)
    print(f"Request {request} ---> {server}")