import asyncio
import functools

import tweepy

from bot.core.config import (twitter_access_token, twitter_access_token_secret,
                             twitter_api_key, twitter_api_secret)


class TwitterClient:
    def __init__(self):
        auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        self.api = tweepy.API(auth)

    async def post(self, *, message: str, file_path: str, link: str):

        loop = asyncio.get_event_loop()

        media = await loop.run_in_executor(
            None, functools.partial(self.api.media_upload, file_path)
        )
        status = await loop.run_in_executor(
            None,
            functools.partial(
                self.api.update_status, status=message, media_ids=[media.media_id]
            ),
        )
        await loop.run_in_executor(
            None,
            functools.partial(
                self.api.update_status, status=link, in_reply_to_status_id=status.id
            ),
        )
