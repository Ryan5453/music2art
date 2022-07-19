from bot.video import VideoGenerator


async def generate_art():
    generator = VideoGenerator()
    await generator.get_song_data()
    await generator.create_dream()
    await generator.download_track()
    await generator.download_dream_images()
    await generator.generate_video()
    await generator.post()
    await generator.file_storage.clear()
