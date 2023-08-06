FROM nvidia/cuda:11.4.0-devel-ubuntu20.04
ARG DEBIAN_FRONTEND=noninteractive

# Update & install packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    make \
    build-essential \
    cmake \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    zlib1g-dev 

############### begin Python installation ############### 

RUN apt-get update && apt-get install -y python3 python3-pip
RUN mkdir -p /tmp/python
WORKDIR /tmp/python
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 

############### end Python installation ############### 

ENV LD_LIBRARY_PATH=/usr/local/lib64:$LD_LIBRARY_PATH