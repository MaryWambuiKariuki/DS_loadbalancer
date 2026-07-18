import json
import matplotlib.pyplot as plt

with open("results.json") as f:
    data = json.load(f)

servers = list(data.keys())
counts = list(data.values())

plt.figure(figsize=(8,5))

plt.bar(servers, counts)

plt.title("10000 Requests on 3 Servers")

plt.xlabel("Server")

plt.ylabel("Requests")

plt.grid(axis="y")

plt.savefig("experiment1_bar.png")

plt.show()