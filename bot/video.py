import asyncio

import httpx

from bot.core.config import video_height, video_width, wombo_style_id
from bot.core.exceptions import ImageException
from bot.core.files import FileStorage
from bot.modules import (
    DeezerAPIClient,
    Dream,
    SongWhipClient,
    SpotifyAPIClient,
    Track,
    TwitterClient,
    WomboAPIClient,
)
from bot.modules.chatgpt.client import generate_prompt


class VideoGenerator:
    def __init__(self) -> None:
        self.deezer_client = DeezerAPIClient()
        self.spotify_client = SpotifyAPIClient()
        self.wombo_client = WomboAPIClient()
        self.file_storage = FileStorage()
        self.session = httpx.AsyncClient(verify=False)
        self.twitter_client = TwitterClient()
        self.songwhip_client = SongWhipClient()

    async def _download_image(self, image_url: str) -> bytes:
        response = await self.session.get(image_url)
        if response.status_code != 200:
            raise ImageException(f"Failed to get image from {image_url}")
        return response.content

    async def get_song_data(self) -> None:
        await self.deezer_client.setup()
        await self.spotify_client.setup()
        for _ in range(len(self.spotify_client.chart)):
            song = await self.spotify_client.get_random_song()
            search_results = await self.deezer_client.search(song)
            if len(search_results) == 0:
                continue

            track = Track(self.deezer_client, search_results[0])
            if not track.has_lyrics:
                continue

            lyrics = await track.get_lyrics()
            if not lyrics.has_synced_lyrics:
                continue
            break

        self.track = track
        self.lyric = lyrics.get_random_lyric()

    async def create_dream(self) -> None:
        await self.wombo_client.start_dream(use_target_image=False)
        await self.wombo_client.put_dream_data(
            prompt=await generate_prompt(self.lyric.text),
            style=wombo_style_id,
            height=video_height,
            width=video_width,
            target_image_weight=0.0,
        )
        dream_data = None
        while dream_data is None:
            dream_data = await self.wombo_client.get_dream_data()
            await asyncio.sleep(1)
        self.dream_data = Dream(dream_data)

    async def download_track(self) -> None:
        track = await self.deezer_client.download_track(self.track)
        await self.file_storage.save("track", track)

    async def download_dream_images(self) -> None:
        await self.file_storage.save(
            "main_image", await self._download_image(self.dream_data.image)
        )

    def _calc_max_duration(self, duration: float) -> float:
        """
        Per US Fair Use law, the maximum amount of time music can be used is either 10% of the song length, or 15 seconds, whichever is lower.

        The duration parameter is in seconds.
        """
        return float(min(min(int(duration * 0.1), 15), self.lyric.duration + 3))

    def _calculate_music_start_time(self) -> float:
        """
        Return value is in seconds.
        """
        max_video_duration = self._calc_max_duration(self.track.duration)
        if self.lyric.duration > max_video_duration:
            self.music_start_time = self.lyric.start
        else:
            self.music_start_time = self.lyric.start - 1.5

        return max(self.music_start_time, 0)

    def _calcuate_time_for_creation_images(self) -> float:
        """
        Return value is in seconds.
        """
        return 1.5 / len(self.dream_data.creation_images)

    def _calculate_time_for_main_image(self) -> float:
        """
        Return value is in seconds.
        """
        return self._calc_max_duration(self.track.duration) - 1.5

    async def generate_video(self) -> None:
        path = await self.file_storage.store("video", ext="mp4")
        ffmpeg_command = [
            "ffmpeg",
            "-ss",
            str(self._calculate_music_start_time()),
            "-t",
            str(self._calc_max_duration(self.track.duration)),
            "-i",
            self.file_storage.get("track"),
            "-i",
            self.file_storage.get("main_image"),
            "-r",
            "30",
            "-vf",
            f"scale=w={video_width}:h={video_height}",
            path,
        ]
        p = await asyncio.create_subprocess_exec(*ffmpeg_command)
        await p.communicate()

    async def post(self):
        status = f'"{self.lyric.text[:100]}" - {self.track.artist[:50]}'
        await self.twitter_client.post(
            message=status,
            file_path=self.file_storage.get("video"),
            link=await self.songwhip_client.get_url(self.track.url),
        )
