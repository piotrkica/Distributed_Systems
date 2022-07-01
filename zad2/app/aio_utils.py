import asyncio
import aiohttp


async def fetch_archive(session, archive_url):
    for _ in range(10):
        try:
            async with session.get(archive_url) as resp:
                month_archive = await resp.json()
                return month_archive["games"]
        except aiohttp.ClientError:  # handle 429 - too many requests
            await asyncio.sleep(0.2)
    return []


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return {}
        try:
            result = response.json()
        except:
            result = response.json(content_type="text/plain")
        return await result


async def fetch_data(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        return await asyncio.gather(*[fetch(session, url, headers) for url, headers in urls])
