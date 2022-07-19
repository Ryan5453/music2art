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
        params = {
            "page": page,
            "per_page": per_page,
        }
        logger.debug(f"Sending GET request to Genius API | Parameters: {str(params)}")
        r = await self.session.get(GENIUS_API_URL, params=params)
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
