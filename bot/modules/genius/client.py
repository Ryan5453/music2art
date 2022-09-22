import logging
import random

import httpx

from bot.core.exceptions import GeniusAPIException

logger = logging.getLogger(__name__)

GENIUS_API_URL = "https://genius.com/api/songs/chart"


class GeniusAPIClient:
    def __init__(self):
        self.session = httpx.AsyncClient(verify=False)
        self.chart = []

    # This function is internal to the class
    # It is NOT required to be called from outside the class
    async def _get_data(self, page: int, per_page: int) -> dict:
        headers = {
            'Host': 'genius.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
            'sec-ch-ua-platform': '"macOS"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://genius.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        params = {
            "page": page,
            "per_page": per_page,
        }
        logger.debug(f"Sending GET request to Genius API | Parameters: {str(params)}")
        r = await self.session.get(GENIUS_API_URL, params=params, headers=headers)
        logger.debug(
            f"Received response from Genius API | Status: {r.status_code} | Response: {r.text}"
        )
        json = r.json()
        if json["meta"]["status"] != 200:
            raise GeniusAPIException
        return json

    async def setup(self) -> None:
        logger.debug("Getting songs from Genius API...")
        for x in range(1, 5):
            data = await self._get_data(x, 50)
            for song in data["response"]["chart_items"]:
                self.chart.append(
                    f"{song['item']['title']} {song['item']['primary_artist']['name']}"
                )
        logger.debug(f"Got {len(self.chart)} songs from Genius API")

    async def get_random_song(self) -> str:
        return random.choice(self.chart).replace("\xa0", " ")
