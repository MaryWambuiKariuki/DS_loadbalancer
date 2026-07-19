import asyncio
import aiohttp
import requests
import json
from collections import Counter

BASE_URL = "http://localhost:5000"

TOTAL_REQUESTS = 10000

counter = Counter()


async def fetch(session, request_id):
    try:
        async with session.get(f"{BASE_URL}/home?id={request_id}") as response:
            data = await response.json()

            if "server" in data:
                counter[data["server"]] += 1

    except Exception:
        pass


async def send_requests():

    counter.clear()

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch(session, i)
            for i in range(TOTAL_REQUESTS)
        ]

        await asyncio.gather(*tasks)


def set_number_of_servers(target):

    current = requests.get(f"{BASE_URL}/rep").json()["N"]

    while current < target:
        requests.post(f"{BASE_URL}/add")
        current += 1

    while current > target:
        requests.delete(f"{BASE_URL}/rm")
        current -= 1


results = {}

for n in range(2, 7):

    print(f"\nTesting with {n} servers...")

    set_number_of_servers(n)

    asyncio.run(send_requests())

    average = sum(counter.values()) / n

    results[n] = average

    print(counter)
    print("Average =", average)


with open("experiment2_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nDone.")