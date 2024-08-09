FROM resin/rpi-raspbian:buster-slim

RUN apt-get update && apt-get install -y vim libc6 libgcc1 libstdc++6 libcurl4-openssl-dev libssl-dev libjpeg-dev zlib1g-dev

RUN apt-get install -y libraspberrypi-bin

WORKDIR /app

ENV TERM=xterm

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev

COPY ./requirements.txt .

RUN pip install "fastapi[standard]"

RUN pip install --no-cache-dir --upgrade -r requirements.txt
