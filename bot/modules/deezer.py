import hashlib
import logging
from typing import Optional

import httpx
from Crypto.Cipher import Blowfish

from bot.core.config import deezer_master_key
from bot.core.exceptions import DeezerAPIException

logger = logging.getLogger(__name__)


class DeezerAPIClient:
    def __init__(self) -> None:
        self.session = httpx.AsyncClient()
        self.token = ""

    async def _api_request(self, method: str, data: Optional[dict] = {}) -> dict:
        params = {
            "method": method,
            "input": 3,
            "api_version": "1.0",
            "api_token": self.token,
        }
        logger.debug(
            f"Sending POST request to Deezer API | Parameters: {str(params)} | Data: {str(data)}"
        )
        r = await self.session.post(
            f"https://www.deezer.com/ajax/gw-light.php?",
            params=params,
            json=data,
        )
        logger.debug(
            f"Received response from Deezer API | Status: {r.status_code} | Response: {r.text}"
        )
        if r.status_code != 200:
            raise DeezerAPIException
        return r.json()

    async def setup(self) -> None:
        logger.debug("Deezer API Client: Setting up...")
        r = await self._api_request("deezer.getUserData")

        self.token = r["results"]["checkForm"]
        self.license_token = r["results"]["USER"]["OPTIONS"]["license_token"]
        logger.debug(
            f"Deezer API Client: Set token ({self.token}) & license token ({self.license_token})"
        )

    async def search(self, query: str) -> dict:
        data = {"query": query, "start": 0, "nb": 25, "top_tracks": True}
        r = await self._api_request("deezer.pageSearch", data)

        search_results = r["results"]["TRACK"]["data"]
        return search_results

    async def get_lyrics(self, id: int) -> dict:
        data = {"sng_id": id}
        r = await self._api_request("song.getLyrics", data)

        return r["results"]

    def _decrypt_chunk(self, data: bytes, blowfish_key: bytes) -> bytes:
        cipher = Blowfish.new(
            blowfish_key, Blowfish.MODE_CBC, bytes([i for i in range(8)])
        )
        return cipher.decrypt(data)

    def _generate_blowfish_key(self, track_id: int) -> bytes:
        logger.debug(f"Generating blowfish key for track {track_id}")
        m = hashlib.md5()
        m.update(bytes([ord(x) for x in track_id]))
        id_md5 = m.hexdigest()

        blowfish_key = bytes(
            (
                [
                    (ord(id_md5[i]) ^ ord(id_md5[i + 16]) ^ ord(deezer_master_key[i]))
                    for i in range(16)
                ]
            )
        )
        logger.debug(f"Blowfish key: {blowfish_key}")
        return blowfish_key

    async def download_track(self, track_info: dict) -> bytes:
        data = {
            "license_token": self.license_token,
            "media": [
                {
                    "type": "FULL",
                    "formats": [{"cipher": "BF_CBC_STRIPE", "format": "MP3_128"}],
                }
            ],
            "track_tokens": [track_info["TRACK_TOKEN"]],
        }
        logger.debug(f"Sending POST request to get track URL | Data: {str(data)}")
        resp = await self.session.post("https://media.deezer.com/v1/get_url", json=data)
        logger.debug(
            f"Received response from get track URL | Status: {resp.status_code} | Response: {resp.text}"
        )
        if resp.status_code != 200:
            raise DeezerAPIException
        json = resp.json()

        url = json["data"][0]["media"][0]["sources"][0]["url"]
        logger.debug(f"Downloading track from {url}")
        data = await self.session.get(url)
        logger.debug(
            f"Received response from download track | Status: {data.status_code} | Response size: {len(data.content)}"
        )
        if data.status_code != 200:
            raise DeezerAPIException

        decryption_key = self._generate_blowfish_key(track_info["SNG_ID"])

        iterations = 0
        virtual_file = b""

        for chunk in data.iter_bytes(chunk_size=2048):
            if (
                iterations % 3 == 0 and len(chunk) == 2048
            ):  # Every third chunk of 2048 bytes is encrypted
                virtual_file += self._decrypt_chunk(chunk, decryption_key)
            else:
                virtual_file += chunk
            iterations += 1
        return virtual_file
