import asyncio
import aiohttp
import json
from collections import Counter

BASE_URL = "http://localhost:5000/home"

TOTAL_REQUESTS = 10000

counter = Counter()


async def fetch(session, request_id):
    try:
        async with session.get(
            URL,
            params={"id": request_id}
        ) as response:

            data = await response.json()

            if "server" in data:
                counter[data["server"]] += 1

    except Exception as e:
        print(f"Request {request_id} failed: {e}")


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch(session, i)
            for i in range(TOTAL_REQUESTS)
        ]

        await asyncio.gather(*tasks)

    print("\nRequests handled by each server:")
    for server, count in sorted(counter.items()):
        print(f"{server}: {count}")

    with open("results.json", "w") as f:
        json.dump(dict(counter), f, indent=4)

    print("\nResults saved to results.json")


if __name__ == "__main__":
    asyncio.run(main())