import httpx

from bot.core.exceptions import ImageException


async def get_image(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise ImageException(f"Failed to get image from {url}")
        return response.content
