import logging
import random

import httpx

from bot.core.exceptions import SpotifyAPIException

logger = logging.getLogger(__name__)

SPOTIFY_API_URL = "https://charts-spotify-com-service.spotify.com/public/v0/charts"


class SpotifyAPIClient:
    def __init__(self):
        self.session = httpx.AsyncClient(verify=False)
        self.chart = []

    async def setup(self) -> None:
        logger.debug("Getting songs from Spotify API...")
        response = await self.session.get(SPOTIFY_API_URL)
        if response.status_code != 200:
            raise SpotifyAPIException(
                f"Failed to get songs from Spotify API. Status code: {response.status_code}"
            )
        json = response.json()
        for entry in json["chartEntryViewResponses"][0]["entries"]:
            self.chart.append(
                f"{entry['trackMetadata']['trackName']} {entry['trackMetadata']['artists'][0]['name']}"
            )

        logger.debug(f"Got {len(self.chart)} songs from Spotify API")

    async def get_random_song(self) -> str:
        return random.choice(self.chart).replace("\xa0", " ")
