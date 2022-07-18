import random
from typing import Optional

from bot.modules.deezer.client import DeezerAPIClient


class Lyric:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    @property
    def text(self) -> str:
        return self.payload["line"]

    @property
    def duration(self) -> float:
        return int(self.payload["duration"]) / 1000

    @property
    def start(self) -> float:
        return int(self.payload["milliseconds"]) / 1000


class Lyrics:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    @property
    def has_synced_lyrics(self) -> bool:
        return bool(self.payload.get("LYRICS_SYNC_JSON")) and not all(
            lyric["line"] == "" for lyric in self.payload["LYRICS_SYNC_JSON"]
        )

    def get_random_lyric(self) -> Lyric:
        while True:
            lyric_data = random.choice(self.payload["LYRICS_SYNC_JSON"])
            lyric = lyric_data["line"]
            if lyric != "":
                break
        return Lyric(lyric_data)


class Track:
    def __init__(self, deezer_client: DeezerAPIClient, payload: dict) -> None:
        self.deezer_client = deezer_client
        self.payload = payload

    @property
    def has_lyrics(self) -> bool:
        return self.payload["HAS_LYRICS"]

    @property
    def track_token(self) -> str:
        return self.payload["TRACK_TOKEN"]

    @property
    def track_id(self) -> str:
        return self.payload["SNG_ID"]

    @property
    def duration(self) -> int:
        return int(self.payload["DURATION"])  # The API returns this value in seconds

    async def get_lyrics(self) -> Lyrics:
        payload = await self.deezer_client.get_lyrics(self.track_id)
        return Lyrics(payload)
