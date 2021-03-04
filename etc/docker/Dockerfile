FROM python:3.7

RUN apt-get update \
    \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    \
    autoconf \
    automake \
    libtool \
    nasm \
    make \
    \
    gettext \
    ffmpeg \
    \
    && rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/mozilla/mozjpeg/archive/v3.3.1.tar.gz && tar -xvzf v3.3.1.tar.gz && cd mozjpeg-3.3.1/ && autoreconf -fiv && mkdir build && cd build && sh ../configure && make install
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
# docker rmi $(docker images -q -f dangling=true)
