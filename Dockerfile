FROM ubuntu:focal

LABEL maintainer="michal.magun@icloud.com"

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive \
    TZ=Europe/Warsaw

RUN apt-get update && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y wget mono-runtime libsqlite3-dev screen python3.6 python3.6-dev python3-pip python3.6-venv portaudio19-dev libcurl4-openssl-dev libssl-dev && \
	mkdir /mfbot

RUN wget https://www.mfbot.de/Download/latest/MFBot_Konsole_x86_64 && \
    chmod a+x MFBot_Konsole_x86_64 && \
    ln -sf /MFBot_Konsole_x86_64 /mfbot/MFBot_Konsole_x86_64

WORKDIR /mfbot

COPY Acc.ini .
COPY ./Web/ ./Web/
COPY entrypoint.sh .

RUN chmod a+x ./entrypoint.sh

WORKDIR /mfbot/Web

RUN python3.6 --version && \
    python3.6 -m venv venv && \ 
    source venv/bin/activate && \
    pip install -r requirements.txt

# CMD [ "/mfbot/entrypoint.sh" ]

ENTRYPOINT [ "/mfbot/entrypoint.sh" ]