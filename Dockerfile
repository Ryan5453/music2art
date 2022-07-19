FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg

COPY requirements.txt /mta/requirements.txt
RUN pip install -r /mta/requirements.txt

COPY ./bot /mta/bot

WORKDIR /mta

ENTRYPOINT python3 -m bot