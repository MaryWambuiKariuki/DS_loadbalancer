import asyncio
import aiohttp
import json
from collections import Counter

URL = "http://localhost:5000/home"

counter = Counter()

TOTAL_REQUESTS = 10000


async def fetch(session):
    try:
        async with session.get(URL) as response:
            data = await response.json()

            if "server" in data:
                counter[data["server"]] += 1

    except Exception:
        pass


async def main():
    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch(session)
            for _ in range(TOTAL_REQUESTS)
        ]

        await asyncio.gather(*tasks)

    print(counter)

    with open("results.json", "w") as f:
        json.dump(counter, f, indent=4)


asyncio.run(main())