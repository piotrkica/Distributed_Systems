from collections import Counter, defaultdict
import requests
import asyncio
import aiohttp
import json

from aio_utils import fetch_archive, fetch_data
from utils import get_opening

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

LICHESS_KEY = "lip_SPisFQ92fR7emosWDb52"
LICHESS_HEADER = {"Authorization": f"Bearer {LICHESS_KEY}"}


def request_user_data(user_name):
    urls = [(f"https://lichess.org/api/user/{user_name}", LICHESS_HEADER),
            (f"https://api.chess.com/pub/player/{user_name}", {}),
            (f"https://api.chess.com/pub/player/{user_name}/stats", {})]

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    lichess_user, chesscom_user_info, chesscom_user_stats = loop.run_until_complete(fetch_data(urls, loop))

    if lichess_user.get("disabled", False):
        lichess_user = None

    chesscom_user = None
    if chesscom_user_info.get("code", 1) != 0 and chesscom_user_stats.get("code", 1) != 0:  # code 0 == not found
        for field in ["chess_bullet", "chess_blitz", "chess_rapid"]:
            if field not in chesscom_user_stats:
                chesscom_user_stats[field] = {"last": {"rating": "missing"}}
        chesscom_user = {**chesscom_user_info, **chesscom_user_stats}

    return lichess_user, chesscom_user


def lichess_mc_openings(user_name, n_games=20, mc=5):
    user_data_response = requests.get(f"https://lichess.org/api/user/{user_name}",
                                      headers=LICHESS_HEADER)

    games_response = requests.get(f"https://lichess.org/api/games/user/{user_name}?max={n_games}",
                                  headers={"Authorization": f"Bearer {LICHESS_KEY}",
                                           "Accept": "application/x-ndjson"})

    if user_data_response.status_code != 200 or games_response.status_code != 200:
        return "Couldn't download games, sorry"

    parsed_response = [json.loads(json_obj) for json_obj in games_response.content.decode().split('\n') if json_obj]
    openings = [" ".join(resp["moves"].split(" ")[:4]) for resp in parsed_response]
    openings_count = Counter(openings)

    return openings_count.most_common(mc)


async def chesscom_mc_openings(user_name, mc=5, n_months=12):
    response = requests.get(f"https://api.chess.com/pub/player/{user_name}/games/archives")
    if response.status_code != 200:
        return "Couldn't download games, sorry"

    openings = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for archive_url in response.json()["archives"][:n_months]:
            tasks.append(asyncio.ensure_future(fetch_archive(session, archive_url)))

        games_archive = await asyncio.gather(*tasks)
        for month_games in games_archive:
            for game in month_games:
                opening = get_opening(game)
                if opening:
                    openings[opening] += 1

    return Counter(openings).most_common(mc)
