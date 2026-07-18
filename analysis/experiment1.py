import asyncio
import aiohttp
from collections import Counter

URL = "http://localhost:5000/home"

counter = Counter()

TOTAL_REQUESTS = 10000


async def fetch(session):

    async with session.get(URL) as response:

        data = await response.json()

        counter[data["server"]] += 1


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch(session)
            for _ in range(TOTAL_REQUESTS)
        ]

        await asyncio.gather(*tasks)


asyncio.run(main())

print(counter)