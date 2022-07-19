<h1 align="center">
    MusicToArt Twitter Bot
</p>

<p align="center">
    <a href="https://twitter.com/musictoart">
        <img src="https://img.shields.io/twitter/follow/musictoart?style=social">
    </a>
    <a href="https://github.com/ryan5453/musictoart/stargazers">
        <img src="https://img.shields.io/github/stars/ryan5453/musictoart?style=social">
    </a>
    <a href="https://github.com/ryan5453/musictoart/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/ryan5453/musictoart">
    </a>
    <a href="https://python.org/">
        <img src="https://img.shields.io/badge/python-3.9-blue">
    </a>
    <a href="https://github.com/ambv/black">
        <img src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
    <a href="https://github.com/PyCQA/isort">
        <img src="https://img.shields.io/badge/imports-isort-black.svg">
    </a>
</p>

## What does it do?
Every hour, the bot will post a video of art generated from a random song from the Genius charts.

## What services does it use?
- [Genius API](https://docs.genius.com/), for getting the top 200 songs from the Genius daily charts
- [Deezer](https://www.deezer.com/), for downloading the song and the line-by-line lyrics of the song
- [WOMBO API](https://w.ai/), for generating art based on the lyrics
- [FFmpeg](https://www.ffmpeg.org/), for grabbing the correct part of the audio and adding the art on top
- [Twitter API](https://developer.twitter.com/en/docs/basics/authentication/overview), for posting the video to Twitter