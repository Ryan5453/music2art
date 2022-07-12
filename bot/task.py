import asyncio
import hashlib
import random

from bot.modules import DeezerAPIClient, Dream, GeniusAPIClient
from bot.utils import get_image


async def run_art_task():
    genius_client = GeniusAPIClient()
    deezer_client = DeezerAPIClient()
    await deezer_client.setup()

    while True:
        song = await genius_client.get_random_song()
        search_results = await deezer_client.search(song)
        if len(search_results) == 0:
            continue

        search_result = search_results[0]
        if not search_result["HAS_LYRICS"]:
            continue

        lyrics = await deezer_client.get_lyrics(search_result["SNG_ID"])
        if not lyrics.get("LYRICS_SYNC_JSON"):
            continue
        break

    lyric = ""
    while lyric == "":
        lyric_data = random.choice(lyrics["LYRICS_SYNC_JSON"])
        lyric = lyric_data["line"]

    dream = Dream()
    await dream.start_dream_task(use_target_image=False)
    await dream.put_dream_data(
        prompt=lyric,
        style=7,  # 7 is the style of the "HD" style
        height=1000,
        width=1000,
        target_image_weight=0.0,
    )

    data = None
    while data is None:
        data = await dream.get_dream_data()
        await asyncio.sleep(1)

    music = await deezer_client.download_track(search_result)
    music_hash = hashlib.sha256(music).hexdigest()

    with open(f"/tmp/{music_hash}", "wb") as f:
        f.write(music)

    main_image_data = await get_image(data.image_url)
    main_image_hash = hashlib.sha256(main_image_data).hexdigest()

    with open(f"/tmp/{main_image_hash}", "wb") as f:
        f.write(main_image_data)

    creation_images = []
    for image_url in data.creation_images:
        image_data = await get_image(image_url)
        image_hash = hashlib.sha256(image_data).hexdigest()
        with open(f"/tmp/{image_hash}", "wb") as f:
            f.write(image_data)
        creation_images.append(f"/tmp/{image_hash}")

    start_of_lyric = int(lyric_data["milliseconds"]) - 1500
    if start_of_lyric < 0:
        start_of_lyric = 0

    end_of_lyric = start_of_lyric + int(lyric_data["duration"]) + 1500

    mid_file_dir = 1.5 / len(creation_images)

    CONCAT_TXT = f"file /tmp/{main_image_hash}\nduration 0.0001\n"
    for image in creation_images:
        CONCAT_TXT += f"file {image}\nduration {mid_file_dir}\n"
    CONCAT_TXT += f"file /tmp/{main_image_hash}\nduration {str((end_of_lyric - start_of_lyric) / 1000)}\n"

    text_hash = hashlib.sha256(CONCAT_TXT.encode("utf-8")).hexdigest()

    with open(f"/tmp/{text_hash}", "w") as f:
        f.write(CONCAT_TXT)

    ffmpeg_command = [
        "ffmpeg",
        "-ss",
        str(start_of_lyric / 1000),
        "-t",
        str((end_of_lyric - start_of_lyric) / 1000),
        "-i",
        f"/tmp/{music_hash}",
        "-f",
        "concat",
        "-safe",
        "false",
        "-i",
        f"/tmp/{text_hash}",
        "-r",
        "30",
        "-vf",
        "scale=w=1000:h=1000",
        f"/tmp/pussyjuice{text_hash}.mp4",
    ]
    p = await asyncio.create_subprocess_exec(*ffmpeg_command)
    await p.communicate()  # Don't ask me why this is necessary, but it is.
    print(lyric)
