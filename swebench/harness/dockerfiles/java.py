_DOCKERFILE_BASE_JAVA = r"""
FROM --platform={platform} maven:3.9-eclipse-temurin-{java_version}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
wget \
git \
build-essential \
ant \
unzip \
&& rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o mvnd.zip https://downloads.apache.org/maven/mvnd/1.0.2/maven-mvnd-1.0.2-linux-amd64.zip && \
    unzip mvnd.zip -d /tmp && \
    mv /tmp/maven-mvnd-1.0.2-linux-amd64 /usr/local/mvnd && \
    rm mvnd.zip && \
    rm -rf /tmp/maven-mvnd-1.0.2-linux-amd64

ENV MVND_HOME=/usr/local/mvnd
ENV PATH=$MVND_HOME/bin:$PATH

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_JAVA = r"""FROM --platform={platform} {env_image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install Python 3.11.8 if not already installed
RUN apt update && apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y python3.11 python3.11-venv python3.11-dev python3-pip && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    rm -rf /var/lib/apt/lists/* && \
    python3 --version

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
