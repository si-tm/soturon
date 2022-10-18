FROM ubuntu:20.04
  
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y build-essential cmake clang python3-dev vim
RUN apt update -y
RUN apt install git -y
WORKDIR code
RUN git clone --depth 1 https://github.com/si-tm/oxDNA.git
RUN mkdir oxDNA/build
RUN cd oxDNA && rm -rf CMakeCache.txt
RUN cd oxDNA/build && cmake .. && make -j4
