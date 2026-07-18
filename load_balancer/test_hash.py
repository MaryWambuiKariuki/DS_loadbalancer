from consistent_hash import ConsistentHash

ring = ConsistentHash()

ring.add_server("Server-1", 1)
ring.add_server("Server-2", 2)
ring.add_server("Server-3", 3)

print("===================================")
print("SERVERS ON THE HASH RING")
print("===================================")

for server, slots in ring.server_slots.items():
    print(server, "->", slots)

print()

print("===================================")
print("REQUEST MAPPING")
print("===================================")

requests = [
    100001,
    100002,
    100003,
    100004,
    100005,
    100006,
    100007,
    100008,
]

for request in requests:

    server = ring.get_server(request)

    print(f"Request {request} ---> {server}")

print()

print("===================================")
print("REMOVE SERVER-2")
print("===================================")

ring.remove_server("Server-2")

for request in requests:

    server = ring.get_server(request)

    print(f"Request {request} ---> {server}")