import httpx
from bot.core.exceptions import SongWhipException

class SongWhipClient:
    def __init__(self):
        self.session = httpx.AsyncClient(timeout=15)

    async def get_url(self, url: str) -> str:
        data = {
            "url": url,
            "country": "US",
        }
        response = await self.session.post("https://songwhip.com/api/songwhip/create?v=2", json=data)
        if response.status_code != 200:
            raise SongWhipException(f"Failed to get url from {url}")
        json = response.json()
        return "https://songwhip.com" + json["data"]["item"]["url"]