import json
import matplotlib.pyplot as plt

with open("experiment2_results.json") as f:
    data = json.load(f)

servers = list(map(int, data.keys()))
averages = list(data.values())

plt.figure(figsize=(8,5))

plt.plot(
    servers,
    averages,
    marker="o",
    linewidth=2
)

plt.title("Average Requests per Server")
plt.xlabel("Number of Servers")
plt.ylabel("Average Requests")

plt.grid(True)

plt.savefig("experiment2_line.png")

plt.show()